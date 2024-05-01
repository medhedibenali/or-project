from gurobipy import *

from src.pl.read_files import load_products, load_resources

products = load_products()
resources = load_resources()

# TODO: Change this to read from file
nb_employees = 160
nb_machines = 50

model = Model("Production Model")
x = []
for i in products:
    x.append(model.addVar(lb=0, vtype=GRB.CONTINUOUS, name='x' + str(i)))

model.setObjective((quicksum(products[i]["selling_price"] * x[i] for i in range(len(products)))), GRB.MAXIMIZE)

# TODO: See how to add the ressources constraint
# model.addConstrs((quicksum(products[i]["ressources_needed"])))


model.addConstr((quicksum(products[i]["human_work_time"] * x[i] for i in range(len(products)))) <= 8 * nb_employees,
                "Main d'oeuvre")
model.addConstr((quicksum(products[i]["machine_time"] * x[i] for i in range(len(products)))) <= 16 * 60 * nb_machines,
                "Machines")

model.optimize()

for var in model.getVars():
    print(var.varName, '=', var.x)
print('Objective value = ', model.objVal)
