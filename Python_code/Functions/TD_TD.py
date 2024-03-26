def Td_Td(inp, r1, r2):
    # Converting 3D function to 2D.
    # Input: inp[r1][1][r2] --> TD[r1][r2]
    TD = [[0]*r2 for _ in range(r1)]
    for i in range(r1):
        for j in range(r2):
            TD[i][j] = inp[i][0][j]
    return TD