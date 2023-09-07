from log_utils import logger_print
from log_utils import pretty

# from pydantic import BaseModel
import argparse
from typing import TypeVar, Generic, Callable, Any

# from beartype import beartype
from error_utils import ErrorManager
import subprocess

pydantic_type_to_pytype = {
    "integer": int,
    "number": float,
    "string": str,
    "boolean": bool,
    # fallback type: string
}

prop_translation_as_is = ["default"]
prop_translation_table = {
    "enum": "choices",
    "title": "help",
    **{e: e for e in prop_translation_as_is},
}

T = TypeVar("T")


# @beartype
# class ExternalFunctionManager:
class ArgumentTransformer(Generic[T]):
    def __init__(self, dataModel: T):
        self.dataModel = dataModel
        self.schema = self.dataModel.schema()
        self.properties = self.schema["properties"]
        self.fields = self.properties.keys()
        self.cli_arguments = {}
        self.required = self.schema.get("required",[])
        
        with ErrorManager(
            default_error=f"error on processing schema:\n{pretty(self.schema)}\ndataModel: {repr(self.dataModel)}"
        ) as ex:
            for field, prop in self.properties.items():
                field_lower = field.lower()
                args = {"required": field in self.required}
                pydantic_type = prop.pop("type")
                pytype = pydantic_type_to_pytype.get(pydantic_type, None)
                annotated_type = self.dataModel.__annotations__.get(field)

                for prop_name, prop_value in prop.items():
                    if prop_name == "default":
                        
                        args["help"] = f'(default: {prop_value}) {args.get("help","")}'
                    translated_prop_name = prop_translation_table.get(prop_name, None)
                    if translated_prop_name:
                        args[translated_prop_name] = prop_value
                    else:
                        msg = f"property key '{prop_name}' of field '{field}' does not have translation. skipping..."
                        logger_print(msg)
                        # ex.append(msg)
                if pytype is not None:
                    args["type"] = pytype
                else:
                    msg = f"pydantic type '{pydantic_type}' does not have corresponding python type. falling back to str"
                    args["help"] = f'(actual type: {annotated_type}) {args.get("help","")}'
                    logger_print(msg)
                    # ex.append(msg)
                    args["type"] = str
                if field_lower in self.cli_arguments.keys():
                    ex.append(f"Field '{field}' is possibly duplicated in the sense of lower case '{field_lower}' within existing fields")
                    continue
                self.cli_arguments[field_lower] = args

    def parse(self):
        argparser = argparse.ArgumentParser()
        for argName, cli_arg in self.cli_arguments.items():
            argparser.add_argument(f"--{argName}", **cli_arg)
        arguments = argparser.parse_args()
        arguments_serialized = {}
        for field in self.fields:
            arguments_serialized[field] = getattr(arguments, field.lower())
        param = self.dataModel(**arguments_serialized)
        return param


class ExternalFunctionManager(ArgumentTransformer[T]):
    def __init__(self, dataModel: T, cmd: str):
        super().__init__(dataModel)
        self.cmd = cmd.strip()

    def answer(self, func: Callable[[T], Any]):
        def decorated_func():
            param = self.parse()
            return func(param)

        return decorated_func

    def call(self, func: Callable[[T], Any]):
        def decorated_func(param: T):
            assert isinstance(
                param, self.dataModel
            ), f"Invalid parameter: {param}\nShould be of type {self.dataModel}"
            arguments = []
            for argName, argVal in param.dict().items():
                argNameLower = argName.lower()
                pytype = self.cli_arguments[argName]["type"]
                argVal = pytype(argVal)
                if not isinstance(argVal, str):
                    argVal = str(argVal)
                arguments.extend([f"--{argNameLower}", argVal])
            proc_cmd = self.cmd.split() + arguments
            logger_print("calling:", proc_cmd, " ".join(proc_cmd))
            proc = subprocess.run(
                proc_cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )
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
