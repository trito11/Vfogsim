import numpy as np

def Ozgur_User_driven_event(N_user, N_appType, T_totalSim, flag, Event, port):
    ui_taskType = np.random.randint(1, N_appType + 1, N_user)  # Each user is assumed to use an application (single task type)
    appData = {}  # 3 different applications
    # Later we could consider different combinations, but now simple one.
    # Demand       AvgSize(kB)    Intensity(cycles/bit)   deadline(sec)
    # appData{1}  = [0                 0                  .25];   # Empty requests
    appData[1] = [0.5e3, 250, 0.15]   # Light
    appData[2] = [1.0e3, 2500, 0.20]  # Medium
    appData[3] = [1.5e3, 10000, 0.25]  # Heavy
    N_cell = 1
    Epoch = 0.5  # 0.1 or 0.5 or 1.0sec controllable for insane result
    Lambda = N_user / N_cell / Epoch  # Number of active users/packets within time duration Epoch
    # Lambda = Lambda * Event
    t = -np.log(np.random.rand()) / Lambda
    n = 0
    et = 0

    arc = np.random.poisson(N_user, N_user) / max(arc)
    arc[arc >= Event * np.mean(arc)] = 1
    arc[arc < Event * np.mean(arc)] = 0

    ui = np.zeros(len(port), dtype=int)
    tt = np.zeros(len(port), dtype=int)
    ts = np.zeros(len(port))
    
    for k in range(len(port)):
        if port[k] > 0:
            n = n + 1
            if arc[n] > 0:
                ui[n] = k  # userId
                if flag == 0:
                    tt[n] = ui_taskType[ui[n]]  # single taskType
                else:
                    tt[n] = np.random.randint(1, N_appType + 1)  # multiple taskType
                app_info = appData[tt[n]]
                ts[n] = app_info[0] + app_info[0] * (np.random.rand() * 0.2 - 0.1)  # taskSize
                et[n] = t
                t = t - np.log(np.random.rand()) / Lambda

    eventInfo = {'et': et, 'ui': ui, 'tt': tt, 'ts': ts}
    return eventInfo
