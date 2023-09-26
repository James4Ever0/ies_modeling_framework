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

from swiplserver import PrologMQI, PrologThread
from pydantic import BaseModel
from typing import List, Dict
# from HashableDict.HashableDict import HashDict
from frozendict import frozendict
import rich

topology_status_dict = {}

# class TopologyStatus(BaseModel):
#     adder_energy_types: Dict[int, str]
#     port_status: List[Dict[str, str]]

# {adder_index: {adder_port_index: port_name}}
adder_index_to_port_name = {0: {0: "bat_port1", 1: "generator_port1", 2: "load_port1"}}

port_verifiers = {
    "bat_port1": lambda conds: "input" in conds,
    "load_port1": lambda conds: "input" in conds,
}

# {set_of_port_names: lambda cond1, cond2: ...}
conjugate_port_verifiers = {}

banner = lambda title: print(title.center(60, "-"))
banner("querying")

with PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        prolog_thread.query('["prolog_gen.pro"].') # shall be identical.
        # prolog_thread.query('["test_prolog.pro"].')
        result = prolog_thread.query(
            "findall(STATUS, adder_port_status_list([adder1], STATUS), STATUS_LIST)"
        )
        print(result)  # list, get first element
        STATUS_LIST = result[0]["STATUS_LIST"]
        for simutaneous_status in STATUS_LIST:
            adder_status_dict = {}
            port_status_dict = {}
            for adder_index, adder_simutaneous_status in enumerate(simutaneous_status):
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

    for topo_status_frames in topo_status:
        for topo_status_frame_index, (port_name, port_status) in enumerate(topo_status_frames.items()):
            if port_name not in topo_status_frame_flatten.keys():
                topo_status_frame_flatten[port_name] = set()
            _conjugate_verified = True
            with ErrorManager(suppress_error=True) as em:
                for (
                    conjugate_ports,
                    conjugate_verifier,
                ) in conjugate_port_verifiers.items():
                    conds = [port_status[port_name] for port_name in conjugate_ports]
                    conjugate_verified = conjugate_verifier(*conds)
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

possible_adder_energy_type_set_counts = len(verified_topology_status_dict)
print("possible adder energy type set counts:", possible_adder_energy_type_set_counts)

can_proceed = False
if possible_adder_energy_type_set_counts == 0:
    print("no adder energy type set")
elif possible_adder_energy_type_set_counts > 1:
    print("multiple adder energy type sets found")
else:
    can_proceed = True
if not can_proceed:
    print("cannot proceed")
else:
    print("clear to proceed")
