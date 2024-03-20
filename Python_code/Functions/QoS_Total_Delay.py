import numpy as np
import matplotlib.pyplot as plt
import TD_TD

def QoS_Total_Delay(Ttr, Tmig, Texec, Cell_Change_loc, Demand_Time_loc, Queue_Delay_loc, UserMatrix):
    # T queueing
    dummy = TD_TD(UserMatrix[:, Queue_Delay_loc, :], UserMatrix.shape[0], UserMatrix.shape[2])
    Tqueueing = dummy[:, -1]

    # T migration calculation
    pre_m = TD_TD(UserMatrix[:, Cell_Change_loc, :], UserMatrix.shape[0], UserMatrix.shape[2])
    m = np.max(pre_m, axis=1)
    Tmigration = Tmig * m

    # T execution calculation
    pre_r = TD_TD(UserMatrix[:, Demand_Time_loc, :], UserMatrix.shape[0], UserMatrix.shape[2])
    pre_r[pre_r < 0] = 0
    r = np.sum(pre_r, axis=1)
    Texecution = Texec * r

    # T transmission calculation
    Ttrans = r * 0.5 * Ttr

    # Plotting
    T = np.vstack([Tqueueing, Tmigration])
    plt.figure()
    plt.bar(np.arange(T.shape[1]), T.T, stacked=True)
    plt.xlabel('Users ID')
    plt.ylabel('Total Delay')
    plt.legend(['Queueing Delay', 'Migration Delay'])
    plt.grid(True)
    plt.show()