"""
Created on Sun Dec 28 10:33:42 2014

@author: wepon

"""

# 相似度计算,inA、inB都是行向量
import numpy as np
from numpy import linalg as la


# 欧式距离
def euclidSimilar(inA, inB):
    return 1.0 / (1.0 + la.norm(inA - inB))


# 皮尔逊相关系数
def pearsonSimilar(inA, inB):
    if len(inA) < 3:
        return 1.0
    return np.corrcoef(inA, inB, rowvar=0)[0][1]


# 余弦相似度
def cosSimilar(inA, inB):
    inA = np.mat(inA)
    inB = np.mat(inB)
    num = float(inA * inB.T)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / denom)
