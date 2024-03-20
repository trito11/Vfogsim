def Default_UtilityFunction_Edge(UserList, price_list, OBJSIZE, USERCOUNT, Resource_Demand_loc, Remaining_Time_loc, Demand_ServiceType_loc):
    const = [[0] * OBJSIZE for _ in range(USERCOUNT)]
    
    for k in range(USERCOUNT):
        if UserList[k][Remaining_Time_loc - 1] > 0:
            const[k][k] = -price_list[UserList[k][Demand_ServiceType_loc - 1]] * UserList[k][Resource_Demand_loc - 1] * 1 / math.log(UserList[k][Remaining_Time_loc - 1])
        else:
            const[k][k] = -price_list[UserList[k][Demand_ServiceType_loc - 1]] * UserList[k][Resource_Demand_loc - 1] * 15
        const[k][USERCOUNT + k] = 1
    
    return const
