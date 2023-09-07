from log_utils import logger_print

"""
Reserved shell env keyword:
    DOTENV
Reserved commandline argument:
    --dotenv
Reserved config file env keyword:
    IMPORT

Description:
    Provide tools for parsing shell and config file environment variables.
"""

import os
import Levenshtein  # to detect suspicious mistypings
from pydantic import BaseModel
from exception_utils import ExceptionManager
from typing import Union
from argparse_utils import ArgumentTransformer

suspicous_threshold = 3
# for names in between environ attribute name definitions, this would be suspicious_threshold*2

# raise exception for any shell env var that is not present but similar to predefined vars, with hints of suspected predefined var name.
# raise exception for any shell/file config env var that is not present in the predefined vars, with hints of suspected predefined var name.

min_envname_length_threshold = 6


def getBaseModelPropertyKeys(bm: BaseModel):
    return list(bm.schema()["properties"].keys())


class EnvBaseModel(BaseModel):
    def diff(self):
        """
        Returns a dictionary which contains all properties with non-default values
        """
        return {k: v for k, v in self.dict().items() if v != self.__fields__[k].default}

    def __new__(cls, *args, **kwargs):
        upper_prop_keys = set()

        with ExceptionManager() as exc_manager:
            for key in getBaseModelPropertyKeys(cls):
                upper_key = key.upper()
                if upper_key != key:
                    exc_manager.append("Key %s is not upper case." % key)
                elif upper_key in upper_prop_keys:
                    exc_manager.append(
                        "Duplicate property %s in definition of %s"
                        % (upper_prop_keys, cls.__name__)
                    )
                elif (keylen := len(key)) < min_envname_length_threshold:
                    exc_manager.append(
                        "Key %s (length: %d) is too short.\nMinimum length: %d"
                        % (key, keylen, min_envname_length_threshold)
                    )
                else:
                    for uk in upper_prop_keys:
                        edit_distance = Levenshtein.distance(uk, upper_key)
                        if edit_distance < (
                            min_upper_prop_key_st := suspicous_threshold * 2
                        ):
                            exc_manager.append(
                                "Key %s has too little distance to another key %s.\nMinimum distance: %d"
                                % (upper_key, uk, min_upper_prop_key_st)
                            )
                    upper_prop_keys.add(upper_key)
        return super().__new__(cls)


class DotEnvBaseModel(EnvBaseModel):
    DOTENV: Union[str, None] = None


class ArgumentEnv(DotEnvBaseModel):
    @classmethod
    def load(cls):
        trans = ArgumentTransformer(cls)
        param = trans.parse()
        return param


class ShellEnv(DotEnvBaseModel):
    @classmethod
    def load(cls):
        pks = getBaseModelPropertyKeys(cls)
        shellenvs = os.environ
        envs = {}
        with ExceptionManager() as exc_manager:
            for k, v in shellenvs.items():
                if len(pks) == 0:
                    break
                uk = k.upper()
                pks.sort(key=lambda pk: Levenshtein.distance(pk, uk))
                fpk = pks[0]
                if fpk == uk:
                    envs[fpk] = v
                    pks.remove(fpk)
                elif (ed := Levenshtein.distance(fpk, uk)) < suspicous_threshold:
                    exc_manager.append(
                        f"Suspicious shell env var found.\n'{k}' (upper case: '{uk}') is similar to '{fpk}' (edit distance: {ed})"
                    )
                else:
                    continue  # do nothing. just ignore excessive shell environment vars.
        return cls(**envs)


from dotenv import dotenv_values


class DotEnv(EnvBaseModel):
    IMPORT: str = ""

    @property
    def import_fpaths(self):
        imp_fpaths = self.IMPORT.strip().split()
        imp_fpaths = [(new_fp := fp.strip()) for fp in imp_fpaths if len(new_fp) > 0]
        return imp_fpaths

    def resolve_import_graph(self):
        import_fpaths = self.import_fpaths
        resolv = []

        for fpath in import_fpaths:
            subdot = self.preload(fpath, envs={}, _cls=DotEnv)
            resolv.append(fpath)
            subresolv = subdot.resolve_import_graph()
            resolv.extend(subresolv)

        resolv.reverse()
        ret = []
        for res in resolv:
            if res not in ret:
                ret.append(res)
        ret.reverse()

        return ret

    @classmethod
    def preload(cls, fpath: str, _cls=None):
        assert os.path.isfile(fpath), "File %s does not exist" % fpath
        envs = {}

        if _cls is None:
            _cls = cls

        vals = dotenv_values(fpath)
        prop_keys = getBaseModelPropertyKeys(cls)
        with ExceptionManager() as exc_manager:
            for k, v in vals.items():
                if len(prop_keys) == 0:
                    break
                uk = k.upper()
                if uk not in prop_keys:
                    exc_manager.append(
                        "No matching property '%s' in schema %s" % (uk, prop_keys)
                    )
                    for pk in prop_keys:
                        if Levenshtein.distance(uk, pk) <= suspicous_threshold:
                            exc_manager.append(f"'{uk}' could be: '{pk}'")
                else:
                    prop_keys.remove(uk)
                    envs[uk] = v
        return _cls(**envs)

    @classmethod
    def presolve_import_graph(cls, fpath: str):
        pre_inst = cls.preload(fpath, _cls=DotEnv)
        imp_graph = pre_inst.resolve_import_graph()
        return imp_graph

    @classmethod
    def load(cls, fpath: str):
        inst = cls.preload(fpath)
        inst_envs = inst.diff()
        envs = {}
        for imp_fpath in inst.resolve_import_graph():
            envs.update(cls.preload(imp_fpath).diff())
        envs.update(inst_envs)
        return cls(**envs)


class EnvManager:
    shellEnv: ShellEnv
    dotEnv: DotEnv
    argumentEnv: ArgumentEnv

    @classmethod
    def load(cls):
        cls.shellEnv: ShellEnv
        cls.dotEnv: DotEnv
        cls.argumentEnv: ArgumentEnv

        shellEnvInst = cls.shellEnv.load()
        params = shellEnvInst.dict()

        argumentEnvInst = cls.argumentEnv.load()
        params.update(argumentEnvInst.diff())

        if (_dotenv := shellEnvInst.DOTENV) is not None:
            dotEnvInst = cls.dotEnv.load(_dotenv)
            params.update(dotEnvInst.diff())
        return params


class EnvConfig:
    """
    This class is used to parse and store the environment variables from file or environment variables.

    Property names are case-insensitive.
    """

    manager_cls: EnvManager
    data_cls: EnvBaseModel

    @classmethod
    def load(cls):
        """
        Load environment variables.

        Load sequence:
            Environment variables from shell\n
            Commandline arguments\n
            Dotenv file and subsequent imported files
        """
        params = cls.manager_cls.load()
        data_inst = cls.data_cls(**params)
        logger_print(
            "Loaded environment variables:",
            *[f"{k}:\t{v}" for k, v in data_inst.dict().items()],
        )
        return data_inst


def getShellEnvClass(env_class: EnvBaseModel):
    class shell_env_class(ShellEnv, env_class):
        ...

    return shell_env_class


def getDotEnvClass(env_class: EnvBaseModel):
    class dot_env_class(DotEnv, env_class):
        ...

    return dot_env_class


def getArgumentEnvClass(env_class: EnvBaseModel):
    class argument_env_class(ArgumentEnv, env_class):
        ...

    return argument_env_class


def getEnvManagerClass(env_class: EnvBaseModel):
    class env_manager_class(EnvManager):
        shellEnv = getShellEnvClass(env_class)
        dotEnv = getDotEnvClass(env_class)
        argumentEnv = getArgumentEnvClass(env_class)

    return env_manager_class


def getEnvConfigClass(env_class: EnvBaseModel):
    class env_config_class(EnvConfig):
        manager_cls = getEnvManagerClass(env_class)
        data_cls = env_class

    return env_config_class
