import numpy as np


# 平均
def avg_smooth(x, half_period):
    x_size = len(x)
    x_smoothed = np.zeros(x_size)
    for i in range(x_size):
        i_start = i - half_period
        i_start = max(0,i_start)
        i_end = i + half_period +1
        i_end = min(x_size,i_end)
        data = x[i_start:i_end]
        x_smoothed[i] = int(data.sum() / len(data))
    return x_smoothed


# 加权平均
def weight_smooth(x):
    x_size = len(x)
    x_smoothed = np.zeros(x_size)
    weight = [0.07,0.13,0.18,0.24,0.18,0.13,0.07] # 1

    #weight = [0.14,0.14,0.14,0.16,0.14,0.14,0.14] # 2

    #weight = [0.05,0.08,0.12,0.5,0.12,0.08,0.05] # 3


    half_period = 3
    #weight = [0.25,0.5,0.25]
    #half_period = 1
    for i in range(x_size):
        i_start = i - half_period
        i_start = max(0,i_start)
        i_end = i + half_period +1
        i_end = min(x_size,i_end)
        data = x[i_start:i_end]
        if len(data)<7:
            x_smoothed[i] = x[i]
            #x_smoothed[i] = int(data.sum() / len(data))
        else:
            w = weight[0: i_end-i_start]
            x_smoothed[i] = int((data*w).sum())
    return x_smoothed


# 加权平均
def weight_smooth2(x):
    x_size = len(x)

    x_smoothed = np.zeros(x_size)
    weight = [0.07,0.13,0.18,0.24,0.18,0.13,0.07] # 1

    half_period = 3

    for i in range(x_size):
        i_start = i - half_period
        i_start = max(0,i_start)
        i_end = i + half_period +1
        i_end = min(x_size,i_end)
        data = x[i_start:i_end]
        if len(data)<7:
            x_smoothed[i] = int(data.sum() / len(data))
        else:
            w = weight[0: i_end-i_start]
            x_smoothed[i] = int((data*w).sum())
    return x_smoothed

