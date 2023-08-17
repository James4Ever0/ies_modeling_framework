# taking different approach.
# use flashtext to replace keywords
import sys

sys.path.append("../")
from debug_utils import *

# import flashtext
# import os

# from pyomo.environ import *

# from typing import Dict

# def convertSymbolMapToTranslationTable(symbol_map: SymbolMap):
#     translationTable = {}
#     # get alias from symbol map.
#     full_map = {**symbol_map.bySymbol, **symbol_map.aliases}
#     for numeric_name, object_weakref in full_map.items():
#         obj = object_weakref()
#         if obj is not None:
#             object_name = getattr(obj, "name", None)
#             if isinstance(object_name, str):
#                 translationTable[numeric_name] = object_name
#             else:
#                 raise Exception(f"Cannot retrieve name from symbol '{obj}'")
#         else:
#             raise Exception(
#                 f"Numeric symbol name '{numeric_name}' does not have reference to model."
#             )
#     return translationTable


# from contextlib import contextmanager


# @contextmanager
# def getKeywordProcessorFromTranslationTable(translationTable: Dict[str, str]):
#     keyword_processor = flashtext.KeywordProcessor(case_sensitive=True)
#     try:
#         for replaced_item, wanted_item in translationTable.items():
#             keyword_processor.add_keyword(replaced_item, wanted_item)
#         yield keyword_processor
#     finally:
#         del keyword_processor


# def translateTextUsingTranslationTable(
#     text: str, translationTable: Dict[str, str]
# ) -> str:
#     with getKeywordProcessorFromTranslationTable(translationTable) as keyword_processor:
#         translatedText = keyword_processor.replace_keywords(text)
#         return translatedText


# def translateFileUsingTranslationTable(filepath: str, translationTable: Dict[str, str]):
#     if os.path.exists(filepath):
#         with open(filepath, "r") as f:
#             content_before_translation = f.read()
#             content_after_translation = translateTextUsingTranslationTable(
#                 content_before_translation, translationTable
#             )
#         with open(filepath, "w+", encoding="utf-8") as f:
#             f.write(content_after_translation)
#         print("File %s translated." % filepath)
#     else:
#         raise Exception("Could not open file: %s" % filepath)

x_bounds = []

for sense in [minimize, maximize]:
    model = ConcreteModel()
    x = model.变量x = Var()
    y = model.变量y = Var()
    z = model.变量z = Var()
    h = model.变量h = Var()
    # z = model.z = Var()
    # x, y, z = symbols("x y z")
    # infeasible on y.
    # unbounded
    # expressions = [y >= z, y <= 20, y >= 10, z <= 0, z >= -10, x <= 100 - y]
    # feasible
    # expressions = [y >= z, y <= 20, y >= 10, z <= 0, z >= -10, x <= 100 - y, x >= y - z]
    # infeasible
    # expressions = [y >= z, y >= 20, y <= 10, z <= 0, z >= -10, x <= 100 - y, x >= y - z]
    # double infeasible (will not show both)
    expressions = [
        y >= z,
        y >= 20,
        y <= 10,
        h >= 20,
        h <= 10,
        z <= 0,
        z >= -10,
        x <= 100 - (h + y) / 2,
        x >= (h + y) / 2 - z,
    ]
    # Bound infeasibility column '变量y'.
    # check if is unbounded or infeasible.
    # try to comment that out, see if it can solve
    # red = reduce_inequalities(expresssions, [x])
    for i, _expr in enumerate(expressions):
        model.__setattr__(f"expr_{i}", Constraint(expr=_expr))
    # print(red)
    obj = model.obj = Objective(expr=x, sense=sense)
    # io_options = dict(symbolic_solver_labels=True)
    model_filename, model_smap_id = model.write(filename="your_model_name.lp")

    solver = SolverFactory("cplex")
    # 求解器变量乱码,影响求解
    # solver.options["read fileencoding"] = 'utf-8'
    # TODO: get solver log.
    solver_log = os.path.join(os.curdir, "solver.log")
    result = solver.solve(model, tee=True, logfile=solver_log)
    solver_smap_id = solver._smap_id
    model_smaps = model.solutions.symbol_map
    # print(dir(result))
    print(model_smaps)  # {symbol_map_id: symbol_map}
    print("MODEL SYMBOL MAP ID:", model_smap_id)
    print("SOLVER SYMBOL MAP ID:", solver_smap_id)
    # breakpoint()
    model_smap = model_smaps[model_smap_id]
    model_translation_table = convertSymbolMapToTranslationTable(model_smap)
    translateFileUsingTranslationTable(model_filename, model_translation_table)

    solver_smap = model_smaps[solver_smap_id]
    solver_translation_table = convertSymbolMapToTranslationTable(solver_smap)
    translateFileUsingTranslationTable(solver_log, solver_translation_table)
    # breakpoint()

    TC = result.solver.termination_condition
    import rich

    rich.print(result)
    normalTCs = [
        TerminationCondition.globallyOptimal,
        TerminationCondition.locallyOptimal,
        TerminationCondition.feasible,
        TerminationCondition.optimal,
    ]
    if TC == TerminationCondition.infeasible:
        raise Exception("infeasible constraint found. please check expression")
    elif TC == TerminationCondition.unbounded:
        raise Exception("unbounded constraint found. please check expression")
    elif TC not in normalTCs:
        raise Exception(f"abnormal solver exit condition: {TC}")
    print("val? %s, sense? %s" % (val_x := value(x), sense))
    x_bounds.append(val_x)

print("x bounds:", x_bounds)
