from pulp import *
import numpy as np
from Default_UtilityFunction_Edge import *
def default_edge_scheduler_limitted(B_pow, R3, R2, GAMMA, UserList_All, CellMatrix, price_list, Spectral_Resource_loc, Resource_Demand_loc, Is_Block_loc, Remaining_Time_loc, Demand_ServiceType_loc, bus):
    counter = 0
    UserList = []
    user_info = []
    """% If the user has spectral resources, it is considered for edge
    % computation else the demand is blocked
    % Bus computation capacity is considered to be fix and 1M it is in the
    % constraint itself"""
    for k in range(UserList_All.shape[0]):
        UserList_All[k, Is_Block_loc] = 1
        if (np.log2(1 + UserList_All[k, 0] / GAMMA) * UserList_All[k, Spectral_Resource_loc] >= 0 and UserList_All[k, Demand_ServiceType_loc] > 0):
            if (np.log2(1 + UserList_All[k, 0] / GAMMA) * UserList_All[k, Spectral_Resource_loc] >= 1.15 * R2[k]):
                UserList.append(UserList_All[k])
                user_info.append(k)
                counter += 1

    if counter == 0:
        return UserList_All

    USERCOUNT = len(UserList)
    UserList_All[:, Is_Block_loc] = 1

    # Objective Function
    c = np.concatenate((np.zeros(USERCOUNT), -np.ones(USERCOUNT)))
    OBJSIZE = len(c)

    # Utility Function Definition
    UtilityPerUser = Default_UtilityFunction_Edge(UserList, price_list, OBJSIZE, USERCOUNT, Resource_Demand_loc, Remaining_Time_loc, Demand_ServiceType_loc)
    Val_UtilityFunction = np.zeros((USERCOUNT, 1))

    # Total assigned resources are limited with the available resources
    Tot_AssignedResources = np.concatenate((UserList[:, Resource_Demand_loc], np.zeros(OBJSIZE - USERCOUNT)))
    Val_AssignedResources = CellMatrix[0, 1] + len(bus) * B_pow

    # Create a new LP problem
    model = LpProblem(name="Edge_Scheduler_Limitted", sense=LpMaximize)

    # Define decision variables
    x = [LpVariable(f"x_{i}", cat=LpBinary) for i in range(OBJSIZE)]

    # Add objective function
    model += lpSum(c[i] * x[i] for i in range(OBJSIZE))

    # Add constraints
    for j in range(USERCOUNT):
        model += lpSum(Tot_AssignedResources[j] * x[j] for j in range(USERCOUNT)) <= Val_AssignedResources
        model += lpSum(UtilityPerUser[j] * x[j] for j in range(USERCOUNT)) <= Val_UtilityFunction[j]

    # Solve the problem
    model.solve()

    # Update UserList_All based on the result of optimization
    for j in range(USERCOUNT):
        if x[j].value() == 1:
            UserList_All[user_info[j], Is_Block_loc] = 0

    return UserList_All