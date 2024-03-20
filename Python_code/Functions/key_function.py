import numpy as np

def key_function(USERCOUNT, OBJSIZE, r, R1, R2, R3):
    key1_const = np.zeros((USERCOUNT, OBJSIZE))
    key2_const = np.zeros((USERCOUNT, OBJSIZE))
    key3_const = np.zeros((USERCOUNT, OBJSIZE))

    for k in range(USERCOUNT):
        key1_const[k, 2 * USERCOUNT + k] = 1
        key1_const[k, k] = -r[k] / R1[k]

        key2_const[k, 3 * USERCOUNT + k] = 1
        key2_const[k, k] = -r[k] / R2[k]

        key3_const[k, 4 * USERCOUNT + k] = 1
        key3_const[k, k] = -r[k] / R3[k]

    key_const = np.vstack((key1_const, key2_const, key3_const))
    key_const[np.abs(key_const) == np.inf] = -100000

    return key_const
