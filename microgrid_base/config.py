import os
import Levenshtein  # to detect suspicious mistypings
from pydantic import BaseModel, confloat
from exception_utils import ExceptionManager
from typing import Union

suspicous_threshold = 3
# for names in between environ attribute name definitions, this would be suspicious_threshold*2
# raise exception for any shell env var that is not present but similar to predefined vars, with hints of suspected predefined var name.
# raise exception for any shell/file config env var that is not present in the predefined vars, with hints of suspected predefined var name.
min_envname_length_threshold = 6


def getBaseModelPropertyKeys(bm: BaseModel):
    return list(bm.schema()["properties"].keys())


class EnvBaseModel(BaseModel):
    def __new__(cls):
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


class ShellEnv(EnvBaseModel):
    DOTENV: Union[str, None] = None

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
                    pks.pop(fpk)
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
    def preload(cls, fpath: str, envs={}, _cls=None):
        assert os.path.isfile(fpath), "File %s does not exist" % fpath

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
                    prop_keys.pop(uk)
                    envs[uk] = v
        return _cls(**envs)

    @classmethod
    def presolve_import_graph(cls, fpath: str):
        pre_inst = cls.preload(fpath, envs={}, _cls=DotEnv)
        imp_graph = pre_inst.resolve_import_graph()
        return imp_graph

    @classmethod
    def load(cls, fpath: str):
        envs = {}
        envs = cls.preload(fpath, envs=envs).dict()
        for imp_fpath in cls.resolve_import_graph(fpath):
            envs = cls.preload(imp_fpath, envs).dict()
        return cls(**envs)


class EnvManager:
    shellEnv: ShellEnv
    dotEnv: DotEnv

    @classmethod
    def load(cls):
        cls.shellEnv: ShellEnv
        cls.dotEnv: DotEnv
        shellEnvInst = cls.shellEnv.load()
        params = shellEnvInst.dict()
        if (_dotenv := shellEnvInst.DOTENV) is not None:
            dotEnvInst = cls.dotEnv.load(_dotenv)
            params.update(dotEnvInst.dict())
        return params


class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO: bool = True
    UNIT_WARNING_AS_ERROR: bool = True
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1
    MOCK_TEST: Union[None, str] = None


class IESShellEnv(ShellEnv, IESEnv):
    ...


class IESDotEnv(DotEnv, IESEnv):
    ...


class IESEnvManager(EnvManager):
    shellEnv = IESShellEnv
    dotEnv = IESDotEnv


class EnvConfig:
    """
    This class is used to parse and store the environment variables from file or environment variables.

    Property names are case-insensitive.
    """

    manager_cls: EnvManager
    data_cls: EnvBaseModel

    def load(cls):
        """
        Load environment variables.

        Load sequence:
            Environment variables from os
            Dotenv file and subsequent imported files
        """
        params = cls.manager_cls.load()
        data_inst = cls.data_cls(**params)
        return data_inst

class IESEnvConfig(EnvConfig):
    manager_cls = IESEnvManager
    