from pulp import *
from Default_Bandwidth import *
def Default_Scheduler(user_list, upper_speed, R1, R2, R3, U1, U2, U3, Window_size):
    USERCOUNT = user_list.shape[0]
    Hmax = 1000

    # Objective Function
    c = [0] * USERCOUNT + [-1] * USERCOUNT + [-1] * (3 * USERCOUNT)
    OBJSIZE = len(c)

    # Total assigned resources are limited with the available resources
    Tot_AssignedResources = [1] * USERCOUNT + [0] * (OBJSIZE - USERCOUNT)
    Val_AssignedResources = 1

    # Upper limit per user
    Tot_AssignedBandwidth = Default_Bandwidth(20, OBJSIZE, USERCOUNT, user_list)  # 20 MHz BW
    Val_AssignedBandwidth = [r * 20 for r in R3]  # Assuming 20 MHz BW

    # Sigmoid function design
    keys_constraint = key_function(USERCOUNT, OBJSIZE, user_list, R1, R2, R3)
    keys_lefthandside = [0] * (USERCOUNT * 3)

    # Utility function
    # Region 1
    reg1_const_left = reg1(USERCOUNT, OBJSIZE, U1, Hmax)
    reg1_const_right = reg1_right(USERCOUNT, U1)
    # Region 2
    reg2_const_left = reg2(USERCOUNT, OBJSIZE, user_list, R1, R2, U2, Hmax)
    reg2_const_right = reg2_right(USERCOUNT, Hmax)
    # Region 3
    reg3_const_left = reg3(USERCOUNT, OBJSIZE, user_list, U2, U3, R2, R3, Hmax)
    reg3_const_right = reg3_right(USERCOUNT, U2, Hmax)
    # Region 4
    reg4_const_left = reg4(USERCOUNT, OBJSIZE, Hmax, U3)
    reg4_const_right = reg4_right(USERCOUNT, Hmax)

    # OPTIMIZER
    model = LpProblem(name="Default_Scheduler", sense=LpMaximize)

    # Define decision variables
    x = [LpVariable(f"x_{i}", lowBound=0, upBound=1) for i in range(OBJSIZE)]

    # Add objective function
    model += lpSum(c[i] * x[i] for i in range(OBJSIZE))

    # Add constraints
    for j in range(USERCOUNT):
        model += lpSum(Tot_AssignedResources[j] * x[j] for j in range(USERCOUNT)) <= Val_AssignedResources
        model += lpSum(Tot_AssignedBandwidth[j] * x[j] for j in range(USERCOUNT)) <= Val_AssignedBandwidth[j]
        model += lpSum(keys_constraint[j] * x[j] for j in range(USERCOUNT * 3)) <= keys_lefthandside[j]
        model += lpSum(reg1_const_left[j] * x[j] for j in range(OBJSIZE)) <= reg1_const_right
        model += lpSum(reg2_const_left[j] * x[j] for j in range(OBJSIZE)) <= reg2_const_right
        model += lpSum(reg3_const_left[j] * x[j] for j in range(OBJSIZE)) <= reg3_const_right
        model += lpSum(reg4_const_left[j] * x[j] for j in range(OBJSIZE)) <= reg4_const_right

    # Solve the problem
    model.solve()

    res = [x[i].value() for i in range(USERCOUNT)]

    return res


