from log_utils import logger_print, pretty

# from pydantic import BaseModel
import argparse
from typing import TypeVar, Generic, Callable, Any
from beartype import beartype
from error_utils import ErrorManager
import subprocess

pydantic_type_to_pytype = {
    "integer": int,
    "number": float,
    "string": str,
    "boolean": bool,
}

prop_translation_as_is = ["default"]
prop_translation_table = {
    "enum": "choices",
    "title": "help",
    **{e: e for e in prop_translation_as_is},
}

T = TypeVar("T")


@beartype
# class ExternalFunctionManager:
class ExternalFunctionManager(Generic[T]):
    def __init__(self, dataModel: T, cmd: str):
        self.dataModel = dataModel
        self.cmd = cmd
        self.schema = self.dataModel.schema()
        self.properties = self.schema["properties"]
        self.fields = self.properties.keys()
        self.cli_arguments = {}
        self.required = self.schema["required"]
        with ErrorManager(
            default_error=f"error on processing schema:\n{pretty(self.schema)}\ndataModel: {repr(self.dataModel)}"
        ) as ex:
            for field, prop in self.properties.items():
                args = {"required": field in self.required}
                pydantic_type = prop.pop("type")
                pytype = pydantic_type_to_pytype.get(pydantic_type, None)
                if pytype is not None:
                    args["type"] = pytype
                else:
                    ex.append(
                        f"pydantic type '{pydantic_type}' does not have corresponding python type"
                    )
                for prop_name, prop_value in prop.items():
                    translated_prop_name = prop_translation_table.get(prop_name, None)
                    if translated_prop_name:
                        args[translated_prop_name] = prop_value
                    else:
                        ex.append(
                            f"property key '{prop_name}' does not have translation."
                        )
                self.cli_arguments[field] = args

    def answer(self, func: Callable[[T], Any]):
        def decorated_func():
            argparser = argparse.ArgumentParser()
            for argName, cli_arg in self.cli_arguments.items():
                argparser.add_argument(f"--{argName}", **cli_arg)
            arguments = argparser.parse_args()
            arguments_serialized = {}
            for field in self.fields:
                arguments_serialized[field] = getattr(arguments, field)
            param = self.dataModel(**arguments_serialized)
            return func(param)

        return decorated_func

    def call(self, func: Callable[[T], Any]):
        def decorated_func(param: T):
            assert isinstance(
                param, self.dataModel
            ), f"Invalid parameter: {param}\nShould be of type {self.dataModel}"
            arguments = []
            for argName, argVal in param.dict().items():
                arguments.extend([f"--{argName}", argVal])
            proc = subprocess.run(self.cmd.split() + arguments)
            logger_print("process output:", proc.stdout.decode())
            logger_print("process stderr:", proc.stderr.decode())
            if proc.returncode != 0:
                logger_print("invalid process return code:", proc.returncode)
            return func(param)

        return decorated_func


from shared_datamodels import ConflictRefinerParams

conflictRefinerManager = ExternalFunctionManager(
    dataModel=ConflictRefinerParams,
    cmd="conda run -n docplex --live-stream --no-capture-output python conflict_utils.py",
)
