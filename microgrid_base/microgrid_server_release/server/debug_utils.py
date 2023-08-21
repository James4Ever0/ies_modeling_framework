# TODO: assign debug/error id and separate logger/folder for error logging.

from log_utils import logger_print

# input: model, objective, etc.
# output: multiple diagnostics
from pyomo.environ import *
from ies_optim import ModelWrapper

import flashtext
import os
from beartype import beartype
# import subprocess
# from typing import TypedDict
from pydantic import BaseModel
# from typing import Literal, TypedDict

normalSSs = [SolverStatus.ok, SolverStatus.warning]
normalTCs = [
    TerminationCondition.globallyOptimal,
    TerminationCondition.locallyOptimal,
    TerminationCondition.feasible,
    TerminationCondition.optimal,
]
IOUTerminationConditions = [
    TerminationCondition.infeasible,
    TerminationCondition.infeasibleOrUnbounded,
]


class SolverReturnStatus(BaseModel):
    terminationCondition: TerminationCondition
    solverStatus: SolverStatus


class CheckSolverReturnValResult(BaseModel):
    success: bool
    status: SolverReturnStatus


def checkIfSolverHasSolvedModel(solver_result) -> CheckSolverReturnValResult:
    TC = solver_result.solver.termination_condition
    SS = solver_result.solver.status
    solved = TC in normalTCs and SS in normalSSs
    return CheckSolverReturnValResult(
        success=solved,
        status=SolverReturnStatus(terminationCondition=TC, solverStatus=SS),
    )

# TODO: gluecode automation (maybe metaclass?)
# ref: https://github.com/gwenzek/func_argparse
# ref: https://github.com/Acellera/func2argparse (py3.9+)
# ref: https://github.com/pseeth/argbind
# @beartype
# def conflict_refiner(
#     model_path: str,
#     output: str,
#     config: Literal["cplex", "docplex"],
#     timeout: float = 5,
# ):
from shared_datamodels import ConflictRefinerParams
from argparse_utils import conflictRefinerManager

@conflictRefinerManager.call
def conflict_refiner(params: ConflictRefinerParams):
# def conflict_refiner(param):
    # cmd = "conda run -n docplex --live-stream --no-capture-output python conflict_utils.py"
    # arguments = [
    #     "--model_path",
    #     model_path,
    #     "--config",
    #     config,
    #     "--timeout",
    #     timeout,
    #     "--output",
    #     output,
    # ]
    # proc = subprocess.run(cmd.split() + arguments)
    # logger_print("process output:", proc.stdout.decode())
    # logger_print("process stderr:", proc.stderr.decode())
    # # logger_print("process return code", proc.returncode)
    # if proc.returncode != 0:
    #     logger_print("invalid process return code:", proc.returncode)
    output = params.output
    if os.path.exists(output):
        with open(output, "r") as f:
            output_content = f.read()
        return output_content
    else:
        logger_print("output file not found:", output)

from typing import Dict


def convertSymbolMapToTranslationTable(symbol_map: SymbolMap):
    translationTable = {}
    # get alias from symbol map.
    full_map = {**symbol_map.bySymbol, **symbol_map.aliases}
    for numeric_name, object_weakref in full_map.items():
        obj = object_weakref()
        if obj is not None:
            object_name = getattr(obj, "name", None)
            if isinstance(object_name, str):
                translationTable[numeric_name] = object_name
            else:
                raise Exception(f"Cannot retrieve name from symbol '{obj}'")
        else:
            raise Exception(
                f"Numeric symbol name '{numeric_name}' does not have reference to model."
            )
    return translationTable


from contextlib import contextmanager


@contextmanager
def getKeywordProcessorFromTranslationTable(translationTable: Dict[str, str]):
    keyword_processor = flashtext.KeywordProcessor(case_sensitive=True)
    try:
        for replaced_item, wanted_item in translationTable.items():
            keyword_processor.add_keyword(replaced_item, wanted_item)
        yield keyword_processor
    finally:
        del keyword_processor


def translateTextUsingTranslationTable(
    text: str, translationTable: Dict[str, str]
) -> str:
    with getKeywordProcessorFromTranslationTable(translationTable) as keyword_processor:
        translatedText = keyword_processor.replace_keywords(text)
        return translatedText


@beartype
def translateFileUsingTranslationTable(filepath: str, translationTable: Dict[str, str]):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:  # unsure what the encoding is!
            content_before_translation = f.read()
            content_after_translation = translateTextUsingTranslationTable(
                content_before_translation, translationTable
            )
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(content_after_translation)
        logger_print("File %s translated." % filepath)
    else:
        raise Exception("Could not open file: %s" % filepath)


@beartype
def translateFileUsingSymbolMap(filepath: str, symbolMap: SymbolMap):
    translationTable = convertSymbolMapToTranslationTable(symbolMap)
    translateFileUsingTranslationTable(filepath, translationTable)


def solve_with_translated_log_and_statistics(
    model: ConcreteModel, solver, log_directory, label
):
    # def solve_with_translated_log_and_statistics(modelWrapper: ModelWrapper, solver, log_directory, label):
    # model = modelWrapper.model
    label = label.strip()
    assert " " not in label
    msg_label = label.replace("_", " ")
    ret = solver.solve(
        model,
        tee=True,
        logfile=(logfile := os.path.join(log_directory, f"{label}.log")),
    )
    # breakpoint()
    smap = model.solutions.symbol_map[solver._smap_id]

    translateFileUsingSymbolMap(logfile, smap)
    termination_condition = ret.solver.termination_condition
    logger_print(f"{msg_label} termination condition:", termination_condition)
    logger_print(f"{msg_label} logfile: %s" % logfile)
    checkResult = checkIfSolverHasSolvedModel(ret)
    solved = checkResult.success
    if not solved:
        logger_print("solver does not have solution.")
    # else:
    #     ...
    return solved


from pyomo.core.expr import current as EXPR

from typing import Dict


class DecomposedExpression(BaseModel):
    constant: float
    varNameToVarObject: Dict[str, str]
    varNameToVarCoefficient: Dict[str, float]


def decomposeExpression(expr):
    const = 0
    varNameToVarObject = {}
    varNameToVarCoefficient = {}
    is_linear, terms = EXPR.decompose_term(expr)
    if is_linear:
        for coef, var in terms:
            if var is None:
                const += coef
            else:
                varName = str(var)
                varNameToVarObject[varName] = var
                varNameToVarCoefficient[varName] = (
                    varNameToVarCoefficient.get(varName, 0) + coef
                )
        return DecomposedExpression(
            constant=const,
            varNameToVarObject=varNameToVarObject,
            varNameToVarCoefficient=varNameToVarCoefficient,
        )


from typing import List, Tuple


def getValueListFromValueDict(valueDict: Dict[str, float]):
    valueList = list(valueDict.items())
    return valueList


def sortAndDisplayVarValues(
    valueList: List[Tuple[str, float]], banner: str, head_count=10, reverse=False
):
    logger_print(f"SORT BY {banner}".center(70, "="))  # to be commented out
    valueList.sort(key=lambda x: x[1], reverse=reverse)
    head_count = min(len(valueList), head_count)
    message = [f"reversed: {reverse}", ""]
    for i in range(head_count):
        message.append("%s\t%s" % valueList[i])
    output = "\n".join(message)
    logger_print(output)


def sortAndDisplayVarValuesAndTermValues(
    varNameToVarValue: Dict[str, float],
    varNameToTermValue: Dict[str, float],
    submodelName: str = "",
):
    BANNER_VARNAME_TO_VAR_VALUE = (
        f"{submodelName if submodelName+' ' else ''}VAR NAME TO VAR VALUE",
    )
    BANNER_VARNAME_TO_TERM_VALUE = (
        f"{submodelName if submodelName+' ' else ''}VAR NAME TO TERM VALUE",
    )
    valueListOfVarNameToVarValue = getValueListFromValueDict(varNameToVarValue)
    valueListOfVarNameToTermValue = getValueListFromValueDict(varNameToTermValue)
    sortAndDisplayVarValues(valueListOfVarNameToVarValue, BANNER_VARNAME_TO_VAR_VALUE)
    sortAndDisplayVarValues(
        valueListOfVarNameToVarValue, BANNER_VARNAME_TO_VAR_VALUE, reverse=True
    )
    sortAndDisplayVarValues(valueListOfVarNameToTermValue, BANNER_VARNAME_TO_TERM_VALUE)
    sortAndDisplayVarValues(
        valueListOfVarNameToTermValue, BANNER_VARNAME_TO_TERM_VALUE, reverse=True
    )
    logger_print()


def filterVarNameBySubModelVarNames(mDict, submodelVarNames):
    return {k: v for k, v in mDict.items() if k in submodelVarNames}


def groupBySubModelRelatedTranslationTable(
    varNameToVarValue: Dict[str, float],
    varNameToTermValue: Dict[str, float],
    translationTable: Dict[str, List[str]], label: str
):
    logger_print(f"grouping by submodel {label}:")

    for submodelNameOrClassName, varNames in translationTable.items():
        submodel_vn2v = filterVarNameBySubModelVarNames(varNameToVarValue, varNames)
        submodel_vn2t = filterVarNameBySubModelVarNames(varNameToTermValue, varNames)
        sortAndDisplayVarValuesAndTermValues(
            submodel_vn2v, submodel_vn2t, submodelName=submodelNameOrClassName
        )


def decomposeAndAnalyzeObjectiveExpression(
    obj_expr,
    submodelNameToVarNames: Dict[str, List[str]],
    submodelClassNameToVarNames: Dict[str, List[str]],
):
    decomposedResult = decomposeExpression(obj_expr)
    if decomposedResult:
        logger_print(decomposedResult)
        varNameToVarValue = {}
        varNameToTermValue = {}
        for varName, varObj in decomposedResult.varNameToVarObject.items():
            varValue = value(varObj)
            coef = decomposedResult.varNameToVarCoefficient[
                varName
            ]  # seems to be no typeddict type checking in pyright
            termValue = coef * varValue
            varNameToVarValue[varName] = varValue
            varNameToTermValue[varName] = termValue

        # sort and display
        sortAndDisplayVarValuesAndTermValues(varNameToVarValue, varNameToTermValue)

        obj_val = value(obj_expr)
        obj_const = decomposedResult.constant

        # now we need to sort value by submodel name (grouping). don't count keywords here, because that is done in conflict report.

        groupBySubModelRelatedTranslationTable(varNameToVarValue, varNameToTermValue,submodelNameToVarNames, "name")
        groupBySubModelRelatedTranslationTable(varNameToVarValue, varNameToTermValue,submodelClassNameToVarNames, "className")

        logger_print("(OBJ - OBJ_CONST)?", obj_val - obj_const)
        logger_print("OBJ?", obj_val)
        logger_print("OBJ_CONST?", obj_const)
    else:
        logger_print("objective expression is non-linear.")


# TODO: put "obj" & "obj_expr" into modelWrapper.
def checkInfeasibleOrUnboundedModel(
    modelWrapper: ModelWrapper,
    # obj,
    # obj_expr,
    solver,
    log_directory: str,
    timelimit: float = 30,
    max_bound: float = 1e8,
):
    model = modelWrapper.model
    obj = modelWrapper.obj
    obj_expr = modelWrapper.obj_expr
    solver.options["timelimit"] = timelimit
    # phase 1: check if infeasible.
    obj.deactivate()
    model.debug_null_objective = Objective(expr=0, sense=minimize)

    solve_with_translated_log_and_statistics(
        model, solver, log_directory, "null_objective"
    )  # we don't care about this solution. don't do analysis.

    # phase 2: limit range of objective expression
    model.debug_obj_expr_bound = Var()
    model.debug_obj_expr_bound_constraint = Constraint(
        expr=model.debug_obj_expr_bound == obj_expr
    )
    model.debug_obj_expr_bound.setlb(-max_bound)
    model.debug_obj_expr_bound.setub(max_bound)

    model.debug_null_objective.deactivate()
    obj.activate()

    solved = solve_with_translated_log_and_statistics(
        model, solver, log_directory, "bounded_objective"
    )
    if solved:
        decomposeAndAnalyzeObjectiveExpression(
            obj_expr,
            modelWrapper.submodelNameToVarNames,
            modelWrapper.submodelClassNameToVarNames,
        )


# we need to change solver options to early abort execution.