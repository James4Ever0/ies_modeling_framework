from pyomo.environ import *

model = ConcreteModel()

model.I = Set(initialize=[1,2])
model.x = Var(model.I) # valid
# model.y = Var([2,3]) # invalid
model.y = Var([1,2]) # valid
# model.y = Var(model.I)

model.pw = Piecewise([1,2], model.y,model.x, pw_pts=[1,2], f_rule=[2,1], pw_constr_type='EQ',unbounded_domain_var=True) # valid
# model.pw = Piecewise(model.I, model.y,model.x, pw_pts=[1,2], f_rule=[2,1], pw_constr_type='EQ',unbounded_domain_var=True) # valid