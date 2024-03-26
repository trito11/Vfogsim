import numpy as np
from  Default_Scheduler import Default_Scheduler
from  Default_EdgeScheduler_Limitted import Default_EdgeScheduler_Limitted

def Scheduler(UserMatrix, CellMatrix, CellID, price_list, CellID_loc, Spectral_Resource_loc, GAMMA, Resource_Demand_loc, Is_Block_loc, Remaining_Time_loc, Demand_ServiceType_loc, bus, app_type, ServiceRequirements, ServiceUtilities, W, B_pow):
    count = 0
    upper_speed = 50
    UserList = []
    Info_User = []
    R1 = []
    R2 = []
    R3 = []
    U1 = []
    U2 = []
    U3 = []
    Window_size = []
    for user in range(UserMatrix.shape[0]):
        a=UserMatrix[user, CellID_loc]
        if a == CellID:
            UserList.append(UserMatrix[user, :])
            Info_User.append(user+1)
            if UserList[count][app_type] == 0:   # No request so we are using the default
                UserList[count][app_type] = 1
                R1.append(ServiceRequirements[0][0])
                R2.append(ServiceRequirements[0][1])
                R3.append(ServiceRequirements[0][2])
                U1.append(ServiceUtilities[0][0])
                U2.append(ServiceUtilities[0][1])
                U3.append(ServiceUtilities[0][2])
            else:
                UserList[count][app_type] += 1
                R1.append(ServiceRequirements[int(UserList[count][app_type]-1)][0])
                R2.append(ServiceRequirements[int(UserList[count][app_type]-1)][1])
                R3.append(ServiceRequirements[int(UserList[count][app_type]-1)][2])
                U1.append(ServiceUtilities[int(UserList[count][app_type]-1)][0])
                U2.append(ServiceUtilities[int(UserList[count][app_type]-1)][1])
                U3.append(ServiceUtilities[int(UserList[count][app_type]-1)][2])
            Window_size.append(W[int(UserList[count][app_type])-1])
            count += 1

    if count == 0: # No user in the cell
        return UserMatrix, CellMatrix

    # Scheduler for the radio resources
    SpectralResources = Default_Scheduler(np.log2(1+np.array(UserList)[:,0]/GAMMA), upper_speed, R1, R2, R3, U1, U2, U3, Window_size)
    SpectralResources = np.round(SpectralResources*10000)/10000
    for k in range(len(Info_User)): # Updating the user matrix
       UserMatrix[Info_User[k]-1, Spectral_Resource_loc] = SpectralResources[k]
       UserList[k][Spectral_Resource_loc] = SpectralResources[k]
       UserMatrix[Info_User[k]-1, app_type] = UserList[k][app_type]

    # Scheduler for the edge resources
    UserList = Default_EdgeScheduler_Limitted(B_pow, R3, R2, GAMMA, UserList, CellMatrix, price_list, Spectral_Resource_loc, Resource_Demand_loc, Is_Block_loc, Remaining_Time_loc, Demand_ServiceType_loc, bus)

    # Rearranging the user matrix
    for k in range(len(UserList)):
        UserMatrix[Info_User[k]-1, Is_Block_loc] = UserList[k][Is_Block_loc]
    CellMatrix[0]= sum(np.array(UserList)[:, Is_Block_loc] * np.array(UserList)[:, Resource_Demand_loc])
    
    

    return UserMatrix, CellMatrix