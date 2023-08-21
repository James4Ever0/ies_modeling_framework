# TODO: assign debug/error id and separate logger/folder for error logging.

from log_utils import logger_print

# input: model, objective, etc.
# output: multiple diagnostics
# from pyomo.environ import *
from pyomo_environ import *
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


# deprecated.
# def buildWordCounterFromModelWrapper(mw: ModelWrapper):
#     keyword_processor = flashtext.KeywordProcessor()
#     for varName in mw.varNameToSubmodelName.keys():
#         keyword_processor.add_keyword(varName)

#     def word_counter(text: str) -> Dict[str, int]:
#         keywords_found = keyword_processor.extract_keywords(text)

#         keyword_counts = {}
#         for keyword in keywords_found:
#             keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

#         return keyword_counts

#     return word_counter


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

from typing import Dict, Any


class DecomposedExpression(BaseModel):
    constant: float
    varNameToVarObject: Dict[str, Any]
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
        # breakpoint()
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
    valueList: List[Tuple[str, float]],
    mw: ModelWrapper,
    banner: str,
    head_count=10,
    reverse=False,
):
    output = []
    output.append(f"SORT BY {banner}".center(70, "="))  # to be commented out
    valueList.sort(key=lambda x: x[1], reverse=reverse)
    head_count = min(len(valueList), head_count)
    message = [f"reversed: {reverse}", ""]
    for i in range(head_count):
        varName, val = valueList[i]
        message.append(
            "%s\t%s\t%s<%s>"
            % (
                varName,
                val,
                mw.varNameToSubmodelName[varName],
                mw.varNameToSubmodelClassName[varName],
            )
        )
    output.append("\n".join(message))
    logger_print(*output)
    return output


def sortAndDisplayVarValuesAndTermValues(
    varNameToVarValue: Dict[str, float],
    varNameToTermValue: Dict[str, float],
    mw: ModelWrapper,
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
    sortAndDisplayVarValues(
        valueListOfVarNameToVarValue, mw, BANNER_VARNAME_TO_VAR_VALUE
    )
    sortAndDisplayVarValues(
        valueListOfVarNameToVarValue, mw, BANNER_VARNAME_TO_VAR_VALUE, reverse=True
    )
    sortAndDisplayVarValues(
        valueListOfVarNameToTermValue, mw, BANNER_VARNAME_TO_TERM_VALUE
    )
    sortAndDisplayVarValues(
        valueListOfVarNameToTermValue, mw, BANNER_VARNAME_TO_TERM_VALUE, reverse=True
    )
    logger_print()


def selectiveSortVarNames(
    keyToSelectedVarNames, varNameCountDict, mw, banner="SELECTIVE"
):
    output = []
    for key, selectedVarNames in keyToSelectedVarNames.items():
        if selectedVarNames != []:  # skip empty
            submodelVarNameCountList = [
                (varName, count)
                for varName, count in varNameCountDict.items()
                if varName in selectedVarNames
            ]
            output.extend(
                sortAndDisplayVarValues(
                    submodelVarNameCountList, mw, banner=f"{banner} <{key}>"
                )
            )
            output.extend(
                sortAndDisplayVarValues(
                    submodelVarNameCountList,
                    mw,
                    banner=f"{banner} <{key}> REVERSE",
                    reverse=True,
                )
            )
    return output


def cplex_refine_model_and_display_info(
    mw: ModelWrapper,
    lp_filepath,
    log_dir,
    smap,
    # word_counter,
    output_filename="cplex_conflict.txt",
    statistics_filename="cplex_conflict_statistics.txt",
):
    word_counter = mw.word_counter
    crp = ConflictRefinerParams(
        model_path=lp_filepath,
        output=(cplex_conflict_output_path := os.path.join(log_dir, output_filename)),
        timeout=7,
    )

    refine_log = conflict_refiner(crp)
    if refine_log:
        logger_print("cplex refine log:", refine_log)
        # translate_and_append(
        #     cplex_conflict_output_path, export_model_smap
        # )
        translateFileUsingSymbolMap(cplex_conflict_output_path, smap)

        # then you sort it by model.
        with open(cplex_conflict_output_path, "r") as f:
            content = f.read()
            varNameCountDict = word_counter(content)
            varNameCountList = [
                (varName, count) for varName, count in varNameCountDict.items()
            ]
        output = []

        output.extend(
            sortAndDisplayVarValues(varNameCountList, mw, banner="CONFLICT VAR COUNT")
        )

        output.extend(
            sortAndDisplayVarValues(
                varNameCountList,
                mw,
                banner="CONFLICT VAR COUNT REVERSE",
                reverse=True,
            )
        )

        output.extend(
            selectiveSortVarNames(
                mw.submodelNameToVarName,
                varNameCountDict,
                mw,
                banner="(CONFLICT) SUBMODEL NAME",
            )
        )
        output.extend(
            selectiveSortVarNames(
                mw.submodelClassNameToVarName,
                varNameCountDict,
                mw,
                banner="(CONFLICT) SUBMODEL CLASS NAME",
            )
        )

        with open(os.path.join(log_dir, statistics_filename), "w+") as f:
            f.write("\n".join(output))
        return True


def filterVarNameBySubModelVarNames(mDict, submodelVarNames):
    return {k: v for k, v in mDict.items() if k in submodelVarNames}


def groupBySubModelRelatedTranslationTable(
    varNameToVarValue: Dict[str, float],
    varNameToTermValue: Dict[str, float],
    translationTable: Dict[str, List[str]],
    label: str,
    mw: ModelWrapper,
):
    logger_print(f"grouping by submodel {label}:")

    for submodelNameOrClassName, varNames in translationTable.items():
        submodel_vn2v = filterVarNameBySubModelVarNames(varNameToVarValue, varNames)
        submodel_vn2t = filterVarNameBySubModelVarNames(varNameToTermValue, varNames)
        sortAndDisplayVarValuesAndTermValues(
            submodel_vn2v, submodel_vn2t, mw, submodelName=submodelNameOrClassName
        )


def decomposeAndAnalyzeObjectiveExpression(
    obj_expr,
    submodelNameToVarNames: Dict[str, List[str]],
    submodelClassNameToVarNames: Dict[str, List[str]],
    mw: ModelWrapper,
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
        sortAndDisplayVarValuesAndTermValues(varNameToVarValue, varNameToTermValue, mw)

        obj_val = value(obj_expr)
        obj_const = decomposedResult.constant

        # now we need to sort value by submodel name (grouping). don't count keywords here, because that is done in conflict report.

        groupBySubModelRelatedTranslationTable(
            varNameToVarValue, varNameToTermValue, submodelNameToVarNames, "name", mw
        )
        groupBySubModelRelatedTranslationTable(
            varNameToVarValue,
            varNameToTermValue,
            submodelClassNameToVarNames,
            "className",
            mw,
        )

        logger_print("(OBJ - OBJ_CONST)?", obj_val - obj_const)
        logger_print("OBJ?", obj_val)
        logger_print("OBJ_CONST?", obj_const)
    else:
        logger_print("objective expression is non-linear.")


def setBounds(varObject, bound):
    assert bound > 0, f"bound must be positive.\npassed: {bound}"
    varObject.setlb(-bound)
    varObject.setub(bound)


def solve_and_decompose(
    modelWrapper: ModelWrapper, solver, log_directory, banner, decompose=False
):
    cplex_log_dir = os.path.join(log_directory, f"{banner}_cplex_log")
    os.mkdir(cplex_log_dir)
    lp_filepath = os.path.join(log_directory, "model.lp")
    _, smap_id = modelWrapper.model.write(lp_filepath)
    smap = modelWrapper.model.solutions.symbol_map[smap_id]
    cplex_refine_model_and_display_info(modelWrapper, lp_filepath, cplex_log_dir, smap)
    model = modelWrapper.model
    obj_expr = modelWrapper.obj_expr
    solved = solve_with_translated_log_and_statistics(
        model, solver, log_directory, banner
    )
    if decompose:
        if solved:
            decomposeAndAnalyzeObjectiveExpression(
                obj_expr,
                modelWrapper.submodelNameToVarNames,
                modelWrapper.submodelClassNameToVarNames,
                modelWrapper,
            )


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
    # TODO: Constant objective detected, replacing with a placeholder to prevent solver failure.
    model_name = "null_objective"
    modelWrapper.submodelName = model_name
    modelWrapper.submodelClassName = model_name
    
    model.debug_null_objective = Objective(expr=0, sense=minimize)

    # solve_with_translated_log_and_statistics(
    #     model, solver, log_directory, "null_objective"
    # )  # we don't care about this solution. don't do analysis.
    solve_and_decompose(modelWrapper, solver, log_directory, model_name)

    # phase 2: limit range of objective expression
    model.debug_obj_expr_bound = Var()
    model.debug_obj_expr_bound_constraint = Constraint(
        expr=model.debug_obj_expr_bound == obj_expr
    )
    setBounds(model.debug_obj_expr_bound, max_bound)

    model.debug_null_objective.deactivate()
    obj.activate()

    solve_and_decompose(
        modelWrapper, solver, log_directory, "bounded_objective", decompose=True
    )

    # solved = solve_with_translated_log_and_statistics(
    #     model, solver, log_directory, "bounded_objective"
    # )
    # if solved:
    #     decomposeAndAnalyzeObjectiveExpression(
    #         obj_expr,
    #         modelWrapper.submodelNameToVarNames,
    #         modelWrapper.submodelClassNameToVarNames,
    #         modelWrapper,
    #     )

    # this is not a persistent solver.
    # ref: https://pyomo.readthedocs.io/en/stable/advanced_topics/persistent_solvers.html
    del model.debug_obj_expr_bound_constraint
    del model.debug_obj_expr_bound

    decomposed_obj_expr = decomposeExpression(obj_expr)
    for varName, varObject in decomposed_obj_expr.varNameToVarObject.items():
        setBounds(varObject, max_bound)

    solve_and_decompose(
        modelWrapper, solver, log_directory, "bounded_objective_vars", decompose=True
    )


# we need to change solver options to early abort execution.
