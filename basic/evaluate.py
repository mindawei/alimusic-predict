'''
对所有艺人进行评测
'''
from hdc import query
import numpy as np
import pandas as pd
from datetime import date


# 查询某一艺人的预测值和预测日期
def querySingleArtistPredict(name,out_file_path):
    predict = pd.read_csv(out_file_path, names=['artist_id', 'playCount', 'Ds'])
    predict = predict[predict['artist_id'] == name]
    playCount = []
    delta = []
    beginDay = date(2015, 3, 1)
    for item in predict.values:
         playCount.append(item[1])
         Ds = str(item[2])
         currDay = date(int(Ds[0:4]), int(Ds[4:6]), int(Ds[6:8]))
         delta.append(int((currDay - beginDay).days))
    return playCount, delta


# 对单个艺人进行评测，q 是feature文件夹里的query类　
def evaluateSingleArtist(q, artist_id,out_file_path):
    #　获得预测值和天数
    tempPredictPlayCount, tempPredictDeltaDay = querySingleArtistPredict(artist_id,out_file_path)
    # 预测值
    predictResult = np.array(tempPredictPlayCount, dtype=np.int32)
    # 距离多少天
    deltaDay = np.array(tempPredictDeltaDay, dtype=np.int32)
    # 获得真实值
    q.querySingleArtists(artist_id)
    playCount = np.array(q.playCount, dtype=np.int32)
    realResult = playCount[deltaDay]
    # 偏差
    diff = (predictResult - realResult) / realResult
    # sigma 预测值和实际值的归一化方差
    sigma = np.sqrt((diff * diff).sum() / len(diff))
    # 比重
    fai = np.sqrt(realResult.sum())
    # f值
    fScore = (1 - sigma) * fai
    return fScore, sigma, fai


# 评价所有的选手
def evaluateAllArtist(out_file_path):
    q = query.Query("../data/mars_tianchi.db")
    fScore = []
    totalScore = []
    f = open(r"../data/artist&&sigma.txt", 'w')
    for artist in q.queryAllArtists():
        score, sigma, fai = evaluateSingleArtist(q, artist,out_file_path)
        fScore.append(score)
        totalScore.append(fai)
        f.write("%s,%.4f,%d\n" % (artist, sigma, fai))
    f.close()
    q.conn.close()
    return (sum(fScore) / sum(totalScore))
