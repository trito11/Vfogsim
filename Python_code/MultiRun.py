import numpy as np
import os
import scipy.io as sio
from Functions import Acceptance_ratio, ResourceDistribution, QoS_Cell_based, QoS_Total_Delay, QoE_Achieved_rate, plotting_general
# from Main_File import  USERCOUNT, SINR_loc, SpectralResources_loc, UserMatrix, Unserved, events, IsBlocked_loc, Cell_ID_loc, Ttr, Tmig, Texec, Cell_Change_loc, Demand_Time_loc, Queue_Delay_loc, ServiceRequirements, ServiceUtilities
from Main_File import *
GAMMA = 0.000001
UPBOUND = 10
print(f"Will be run for {UPBOUND} instances")

for mircolo in range(1, UPBOUND + 1):
    print(f"Step {mircolo} in progress")
    main()
    filename = f"{mircolo}.mat"
    os.chdir('D:\Lab\Vfogsim\Python_code\Results')
    sio.savemat(filename, {'var': mircolo})  # replace 'var' with your actual variables
    os.chdir('..')

Mitico_Matrix = np.zeros((UserMatrix.shape[0], UserMatrix.shape[1], UserMatrix.shape[2]))
Mitico_AcceptanceRatio = np.zeros(USERCOUNT)
Mitico_RESDISP = np.zeros(4)
Mitico_Cell = np.zeros(12)

print("Completed")

# For Printing
os.chdir('Results')

for mitico in range(1, UPBOUND + 1):
    infile = f"{mitico}.mat"
    data = sio.loadmat(infile)
    UserMatrix = data['UserMatrix']  # replace 'UserMatrix' with your actual variable name
    Mitico_Matrix += UserMatrix
    os.chdir('..')
    os.chdir('Functions')
    Mitico_AcceptanceRatio += Acceptance_ratio(Unserved, events)
    Mitico_RESDISP += ResourceDistribution(UserMatrix, events, IsBlocked_loc)
    Mitico_Cell += QoS_Cell_based(Cell_ID_loc, Ttr, Tmig, Texec, Cell_Change_loc, Demand_Time_loc, Queue_Delay_loc, UserMatrix)
    os.chdir('..')
    os.chdir('Results')

Mitico_Matrix /= UPBOUND
Mitico_AcceptanceRatio /= UPBOUND
Mitico_RESDISP /= UPBOUND
Mitico_Cell /= UPBOUND

infile = f"{mitico}.mat"
data = sio.loadmat(infile)

os.chdir('..')
os.chdir('Functions')

QoS_Total_Delay(Ttr, Tmig, Texec, Cell_Change_loc, Demand_Time_loc, Queue_Delay_loc, Mitico_Matrix)
QoE_Achieved_rate(np.log2(1 + Mitico_Matrix[:, SINR_loc, :] / GAMMA), Mitico_Matrix[:, SpectralResources_loc, :], ServiceRequirements, ServiceUtilities, Mitico_Matrix)
plotting_general(Mitico_Cell, 'Cell ID', 'Congestion Duration (%Time)')
plotting_general(Mitico_AcceptanceRatio, 'User ID', 'Request Acceptance Ratio')
plotting_general(Mitico_RESDISP.T, 'Service Type', 'Request Acceptance Ratio per Service Type')

os.chdir('..')