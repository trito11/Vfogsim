import numpy as np

def default_bandwidth(MAXBW, OBJSIZE, USERCOUNT, user_list):
    const = np.zeros((USERCOUNT, OBJSIZE))
    for k in range(USERCOUNT):
        const[k, k] = MAXBW * user_list[k]
    return const
