import xgboost as xgb
from sklearn import preprocessing
from basic import writer, features,smooth
from hdc import query
import numpy as np


# xgb预测
def xgbPerArtist(feature, target, trainBegin, trainEnd, predictBegin, predictEnd):
    # 归一化处理
    #feature = preprocessing.scale(feature)  #正则化
    try:
        normalizer = preprocessing.Normalizer().fit(feature)  # 归一化
        feature = normalizer.transform(feature)
    except Exception:
        for f in feature:
            print(f)
        return

    # 训练和测试
    dtrain = xgb.DMatrix(feature[trainBegin:trainEnd:, ], label=target[trainBegin:trainEnd].ravel())

    # param['eval_metric'] = ['rmse']
    # param = {}
    # param['objective'] = 'reg:linear'
    # param['booster'] = 'gbtree'
    # param['eta'] = 0.03
    # param['max_depth'] = 3
    # param['eval_metric'] = 'map'
    # param['silent'] = 1
    # param['min_child_weight'] = 0.1
    # param['subsample'] = 0.7
    # param['colsample_bytree'] = 0.3
    # param['nthread'] = 4
    # param['scale_pos_weight'] = 2
    param = {}
    param['objective'] = 'reg:linear'
    param['booster'] = 'gbtree'
    param['eta'] = 0.03
    # 0.02 0.7506
    # 0.025 0.7510
    # 0.03 0.7513
    # 0.04 0.7497
    # 0.05 0.7502

    param['max_depth'] = 3
    param['eval_metric'] = 'rmse'
    # map 0.7513
    # rmse 0.7513
    param['silent'] = 1
    param['min_child_weight'] = 0.1
    param['subsample'] = 1
    # 0.7 0.7513
    # 0.8 0.7503
    param['colsample_bytree'] = 1 # 特征采样比例
    # 0.3    0.7513
    # 0.4    0.7518
    # 0.5    0.7522
    # 0.628  0.7521
    # 0.7    0.7522
    # 0.8    0.7518
    # 1      0.7514

    param['scale_pos_weight'] = 2

    num_round = 2000


    # days = trainEnd - trainBegin
    # if days <= 28:
    #      param['subsample'] = 0.8
    # elif days <= 56:
    #      param['subsample'] = 0.75
    # else:
    #      param['subsample'] = 0.7
    #　2000 0.3
    # ( 2000,0.7513 )    (1000,0.7503)  (3000,0.7499)
    # (2500,0.7490)            (1500,0.7495)
    #
    # cross validation那部分是把训练集分成三份，一份拿出来做验证，
    # 两份留作训练，为了验证模型的能力，也可以在这步进行调优参数，
    # model training部分就是训练模型了，训练好的模型做预测，然后提交结果
    # print("this is cv func")
    # 20 5 0.7513
    # 50 3
    # # # # cv_num_round = 1000
    # print(xgb.cv(param,dtrain,  num_round, nfold = 10, show_progress=False))

    # evallist  = [(dtest,'eval'), (dtrain,'train')] 验证
    bst = xgb.train(param, dtrain, num_round)

    # 预测值
    dpredict = xgb.DMatrix(feature[predictBegin:predictEnd:, ])
    ypred = bst.predict(dpredict)
    return ypred

q = query.Query("../data/mars_tianchi.db")
features_dict = {}
for artist_id in q.queryAllArtists():
    print(artist_id)
    features_dict[artist_id] = features.get_features_between(artist_id, "20150301", "20151030", q.conn)
print("features_dict is ok ")

# 预测
def predict(trainBegin=0, trainEnd=153, predictBegin=154, predictEnd=183, out_file_name="predict",feature_index =0):
    f = open(out_file_name, "w")  # 存放预测结果的文件

    # 获得每个人的特征进行训练
    for artist_id in q.queryAllArtists():
        # artist_id = '2e14d32266ee6b4678595f8f50c369ac'
        # 每个人查询
        q.querySingleArtists(artist_id)
        # 播放值
        playCount = np.array(q.playCount, dtype=np.int32)
        # 平滑
        playCount = smooth.weight_smooth(playCount)
        playCount.shape = (len(playCount), 1)
        target = playCount

        # 日期
        ls = [[row[feature_index]] for row in features_dict[artist_id]]
        feature = np.array(ls)

        # 训练
        pre = xgbPerArtist(feature, target,trainBegin, trainEnd, predictBegin, predictEnd)
        # 写值
        writer.writeResult(f, pre, range(predictBegin, predictEnd), artist_id)
        # break

    # 关闭文件
    f.close()
