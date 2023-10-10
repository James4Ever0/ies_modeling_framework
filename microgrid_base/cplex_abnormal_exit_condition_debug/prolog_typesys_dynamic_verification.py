######## ERROR UTILS START ########

from typing import Union
import traceback
import sys


# @beartype
class ErrorManager:
    """
    Manage exceptions and errors.

    Can be used in `with` statements to automate such management, which behavior can be configured by setting `suppress_error` and `suppress_exception` arguments.

    Args:

    suppress_error:bool: If suppressed, don't raise exception if having error messages
    suppress_exception:bool: If suppressed, don't suppress exception raised by program
    default_error:str: The default error message to display if any error occurs during execution

    """

    def __init__(
        self,
        suppress_error: bool = False,
        suppress_exception: bool = False,
        default_error: Union[str, None] = None,
    ):
        self.errors = []
        self.suppress_error = suppress_error
        self.suppress_exception = suppress_exception
        self.default_error = default_error

    def __bool__(self):
        return len(self.errors) > 0

    @property
    def has_error(self):
        return bool(self)

    @property
    def has_exception(self):
        last_exc = sys.exc_info()
        return last_exc[0] is not None

    def append(self, error: str):
        self.errors.append(error)

    def clear(self):
        self.errors = []
        self.default_error = None

    def format_error(self, clear=True, join: str = "\n"):
        error_msg = join.join(
            self.errors
            + ([self.default_error] if (self and self.default_error) else [])
        )
        if clear:
            self.clear()
        return error_msg

    def raise_if_any(self):
        if self.errors:
            self.print_if_any()
            raise Exception(self.format_error())

    def print_if_any(self):
        if self.errors:
            print(self.format_error())
            return True
        return False

    def __enter__(self):
        self.raise_if_any()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self.suppress_error:
            self.raise_if_any()
        else:
            self.print_if_any()

        if self.has_exception:
            traceback_exc = traceback.format_exc()
            print(traceback_exc)
        return True if self.suppress_exception else None

    def __str__(self):
        return self.format_error(clear=False)

    def __repr__(self):
        return self.format_error(clear=False)

    def __len__(self):
        return len(self.errors)

    def __iter__(self):
        return iter(self.errors)


######## ERROR UTILS END ########

######## FAILSAFE UTILS START #####

from contextlib import contextmanager


@contextmanager
def chdir_context(dirpath: str):
    cwd = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(cwd)


######## FAILSAFE UTILS END #####

from swiplserver import PrologMQI, PrologThread
from pydantic import BaseModel
from typing import List, Dict

# from HashableDict.HashableDict import HashDict
from frozendict import frozendict
import rich
import os
import tempfile


banner = lambda title: print(title.center(60, "-"))


def query_result_from_prolog(prolog_script_content: str, adder_index_to_port_name):
    banner("querying")
    topology_status_dict = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        with chdir_context(temp_dir):
            prolog_file_path = "prolog_script.pro"
            prolog_file_path_abs = os.path.join(prolog_file_path)
            with open(prolog_file_path_abs, "w+") as f:
                f.write(prolog_script_content)
            with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    topology_status_dict = query_prolog_in_context(
                        topology_status_dict,
                        prolog_file_path,
                        prolog_thread,
                        adder_index_to_port_name,
                    )
    return topology_status_dict


def query_prolog_in_context(
    topology_status_dict, prolog_file_path, prolog_thread, adder_index_to_port_name
):
    adder_name_list = []
    adder_index_mapping = {}
    for i, k in enumerate(adder_index_to_port_name.keys()):
        adder_name_list.append("adder{}".format(str(k).replace('-','_')))
        adder_index_mapping[i] = k
    adder_names = ", ".join(adder_name_list)
    print('adder_names: ',adder_names)
    # breakpoint()
    prolog_thread.query(f'["{prolog_file_path}"].')
    result = prolog_thread.query(
        f"findall(STATUS, adder_port_status_list([{adder_names}], STATUS), STATUS_LIST)"
    )
    print(result)  # list, get first element
    STATUS_LIST = result[0]["STATUS_LIST"]
    for simutaneous_status in STATUS_LIST:
        adder_status_dict = {}
        port_status_dict = {}
        for _index, adder_simutaneous_status in enumerate(simutaneous_status):
            adder_index = adder_index_mapping[_index]
            adder_energy_type, adder_port_status = adder_simutaneous_status
            adder_status_dict[adder_index] = adder_energy_type
            print(f"adder #{adder_index}")
            print(f"\tenergy type: {adder_energy_type}")
            print(f"\tport_status:")
            port_index_to_port_name = adder_index_to_port_name[adder_index]
            for adder_port_index, port_status in enumerate(adder_port_status):
                port_name = port_index_to_port_name[adder_port_index]
                port_status_dict[port_name] = port_status
                print(f"\t\t{port_name}: {port_status}")
        key = frozendict(adder_status_dict)
        value = frozendict(port_status_dict)
        if key not in topology_status_dict.keys():
            topology_status_dict[key] = set()
        topology_status_dict[key].add(value)
        print("-" * 60)
    return topology_status_dict


def verify_topology_status_dict(
    topology_status_dict,
    port_verifiers,
    conjugate_port_verifiers,
    adder_index_to_port_name,
):
    banner("unverified topo status")
    rich.print(topology_status_dict)
    banner("verifying")

    verified_topology_status_dict = {}
    for topo_status_index, (adder_status, topo_status) in enumerate(
        topology_status_dict.items()
    ):
        topo_status_frame_flatten = {}
        port_verified = {}
        conjugate_port_verified = {}

        port_name_to_energy_type = {
            v_v: adder_status[k]
            for k, v in adder_index_to_port_name.items()
            for v_k, v_v in v.items()
        }

        for topo_status_frames in topo_status:
            for topo_status_frame_index, (port_name, port_status) in enumerate(
                topo_status_frames.items()
            ):
                # breakpoint()
                if port_name not in topo_status_frame_flatten.keys():
                    topo_status_frame_flatten[port_name] = set()
                _conjugate_verified = True
                with ErrorManager(suppress_error=True) as em:
                    for (
                        conjugate_ports,
                        conjugate_verifier,
                    ) in conjugate_port_verifiers.items():
                        conds = [
                            topo_status_frames[port_name] for port_name in conjugate_ports
                        ]
                        energytypes = [port_name_to_energy_type[port_name] for port_name in conjugate_ports]
                        conjugate_verified = conjugate_verifier(*conds, *energytypes)
                        # conjugate_verified = conjugate_verifier(*conds)
                        if not conjugate_verified:
                            em.append(
                                f"conjugate verification failed for conjugate ports '{conjugate_ports}' at topo status frame #{topo_status_frame_index}"
                            )
                            if _conjugate_verified:
                                _conjugate_verified = False
                if _conjugate_verified:
                    topo_status_frame_flatten[port_name].add(port_status)
                else:
                    print(
                        f"skipping topo status frame #{topo_status_frame_index} due to failed conjugate ports verification"
                    )
        for port_name, verifier in port_verifiers.items():
            conds = topo_status_frame_flatten[port_name]
            verified = verifier(conds)
            port_verified[port_name] = verified
            if not verified:
                print(f"verifier failed for port '{port_name}'")

        all_ports_verified = all(port_verified.values())
        all_conjugate_ports_verified = all(conjugate_port_verified.values())
        topo_verified = all_ports_verified and all_conjugate_ports_verified

        if not all_ports_verified:
            print("not all port vaildations have passed")

        if not all_conjugate_ports_verified:
            print("not all conjugate port vaildations have passed")

        if not topo_verified:
            print(f"topo verification failed for topo status #{topo_status_index}")
        else:
            if len(topo_status) > 0:
                verified_topology_status_dict[adder_status] = topo_status
            else:
                print("skipping due to empty topo status")
        banner(f"processed topo status #{topo_status_index}")

    banner("verified topo status")
    rich.print(verified_topology_status_dict)
    return verified_topology_status_dict


def isomorphicTopologyStatusCombinator(topology_status_dict: dict):
    topo_status_to_adder_status_dict: Dict[frozenset, set] = {}
    for adder_index_to_energy_type, topo_status in topology_status_dict.items():
        topo_status_frozen = frozenset(topo_status)
        if topo_status_frozen not in topo_status_to_adder_status_dict.keys():
            topo_status_to_adder_status_dict[topo_status_frozen] = set()
        topo_status_to_adder_status_dict[topo_status_frozen].add(
            adder_index_to_energy_type
        )
    return topo_status_to_adder_status_dict


def check_if_can_proceed(verified_topology_status_dict):
    possible_adder_energy_type_set_counts = len(verified_topology_status_dict)
    print(
        "possible adder energy type set counts:", possible_adder_energy_type_set_counts
    )

    isomorphic_topo_status = isomorphicTopologyStatusCombinator(
        verified_topology_status_dict
    )

    banner("isomorphic topo status")
    rich.print(isomorphic_topo_status)
    isomorphic_topo_status_counts = len(isomorphic_topo_status.keys())
    print("isomorphic topo status counts:", isomorphic_topo_status_counts)

    can_proceed = False
    if isomorphic_topo_status_counts == 0:
        print("no adder energy type set")
    elif isomorphic_topo_status_counts > 1:
        print("multiple adder energy type sets found")
    else:
        can_proceed = True
    if not can_proceed:
        print("cannot proceed")
    else:
        print("clear to proceed")
    return can_proceed


def execute_prolog_script_and_check_if_can_proceed(
    prolog_script_content,
    adder_index_to_port_name,
    port_verifiers,
    conjugate_port_verifiers,
):
    topology_status_dict = query_result_from_prolog(
        prolog_script_content, adder_index_to_port_name
    )
    verified_topology_status_dict = verify_topology_status_dict(
        topology_status_dict,
        port_verifiers,
        conjugate_port_verifiers,
        adder_index_to_port_name,
    )
    can_proceed = check_if_can_proceed(verified_topology_status_dict)
    return can_proceed


if __name__ == "__main__":
    with open("prolog_gen.pro", "r") as f:
        prolog_script_content = f.read()

    adder_index_to_port_name = {
        1: {0: "bat_port1", 1: "generator_port1", 2: "load_port1"}
    }

    port_verifiers = {
        "bat_port1": lambda conds: "input" in conds,
        "load_port1": lambda conds: "input" in conds,
    }

    # {tuple_of_port_names: lambda cond1, cond2, etype1, etype2: ...}
    conjugate_port_verifiers = {}

    execute_prolog_script_and_check_if_can_proceed(
        prolog_script_content,
        adder_index_to_port_name,
        port_verifiers,
        conjugate_port_verifiers,
    )
