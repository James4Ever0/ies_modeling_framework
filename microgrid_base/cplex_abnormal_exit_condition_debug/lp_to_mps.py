# either pyomo model to mps or lp to mps (cplex)

# method = "docplex"
method = "pyomo"


print("using method:", method)
temp_input_file_name = "E:\\works\\jubilant-adventure2\\microgrid_base\\logs\\pyomo_2023_08_08_17_15_44_141633+08_00\\model.lp"

if method == "docplex":
    from docplex.mp.model import Model
    from docplex.mp.model_reader import ModelReader


    mdl:Model = ModelReader.read(temp_input_file_name, model_name="InfeasibleLP")

    mdl.export_as_mps("converted.mps") # required for lp-analysis
elif method =="pyomo":
    from pyomo.environ import *
    model = ConcreteModel()
    # model.load("converted.mps")
    # lp & mps unsupported.
    # print(dir(model))
    model.x = Var(bounds=(-1,1))
    model.obj = Objective(expr=model.x, sense=minimize)
    model.write("exported.mps", 'mps') # working!
else:
    raise Exception("Unknown mps export method: %s" % method)