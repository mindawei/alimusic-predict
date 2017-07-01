import xgboost as xgb
from sklearn import preprocessing
from basic import writer, features
from hdc import query
import numpy as np


# xgb预测
def get_xgb_model(feature, target, predict):
    # 归一化处理
    #feature = preprocessing.scale(feature)  #正则化
    normalizer = preprocessing.Normalizer().fit(feature)  # 归一化
    feature = normalizer.transform(feature)

    # 训练和测试
    dtrain = xgb.DMatrix(feature, label=target.ravel())

    # param['eval_metric'] = ['rmse']
    param = {}
    param['objective'] = 'reg:linear'
    param['booster'] = 'gbtree'
    param['eta'] = 0.03
    param['max_depth'] = 3
    param['eval_metric'] = 'map'
    param['silent'] = 1
    param['min_child_weight'] = 0.1
    param['subsample'] = 0.7
    param['colsample_bytree'] = 0.3
    param['nthread'] = 4
    param['scale_pos_weight'] = 2

    num_round = 2000


    # cross validation那部分是把训练集分成三份，一份拿出来做验证，
    # 两份留作训练，为了验证模型的能力，也可以在这步进行调优参数，
    # model training部分就是训练模型了，训练好的模型做预测，然后提交结果
    # print("this is cv func")

    #cv_num_round = 100
    #xgb.cv(param,dtrain, cv_num_round, nfold = 3, show_progress=False)

    # evallist  = [(dtest,'eval'), (dtrain,'train')] 验证
    bst = xgb.train(param, dtrain, num_round)
    return bst


# 预测
def predict(trainBegin=0, trainEnd=153, predictBegin=154, predictEnd=183, out_file_name="predict"):
    q = query.Query("../data/mars_tianchi.db")
    f = open(out_file_name, "w")  # 存放预测结果的文件

    all_feature = []
    all_label = []

    # 获得每个人的特征进行训练
    for artist_id in q.queryAllArtists():
        # 每个人查询
        q.querySingleArtists(artist_id)
        # 播放值
        playCount = np.array(q.playCount, dtype=np.int32)
        playCount.shape = (len(playCount), 1)
        target = playCount
        # 日期
        feature = features.get_features_between(artist_id, "20150301", "20151030", q.conn)[trainBegin:trainEnd:, ]
        label = playCount[trainBegin:trainEnd]


    # 获得每个人的特征进行训练
    # for artist_id in q.queryAllArtists():
    #     # 每个人查询
    #     q.querySingleArtists(artist_id)
    #     # 播放值
    #     playCount = np.array(q.playCount, dtype=np.int32)
    #     playCount.shape = (len(playCount), 1)
    #     target = playCount
    #     # 日期
    #     feature = features.get_features_between(artist_id, "20150301", "20151030", q.conn)
    #     # 训练
    #     pre = xgbPerArtist(feature, target,trainBegin, trainEnd, predictBegin, predictEnd)
    #     # 写值
    #     writer.writeResult(f, pre, range(predictBegin, predictEnd), artist_id)
    #
    # # 关闭文件
    # f.close()
