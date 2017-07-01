import xgboost as xgb
from basic import writer, features,smooth,time,rule
import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt


day_start = datetime.datetime.strptime("20150301", '%Y%m%d')


# 获得特征
def get_features(Ds, conn):
    feature = (datetime.datetime.strptime(Ds, '%Y%m%d') - day_start).days
    feature = np.array(feature,dtype=np.int32)
    return feature


# 获得某个区间的特征
def get_features_between(Ds_start,Ds_end,conn):
    # 起始日期
    day_time = datetime.datetime.strptime(Ds_start, '%Y%m%d')
    day_end = datetime.datetime.strptime(Ds_end, '%Y%m%d')
    # 初始化
    all_features = get_features(day_time.strftime("%Y%m%d"),conn)
    day_time += datetime.timedelta(days=1)
    # 获得区间
    while day_time <= day_end:
        one_feature = get_features(day_time.strftime("%Y%m%d"),conn)
        all_features = np.row_stack((all_features, one_feature))
        day_time += datetime.timedelta(days=1)
    return all_features


# xgb预测
def xgbPerArtist(feature, target, trainBegin, trainEnd, predictBegin, predictEnd):
    #
    # # 归一化处理
    # try:
    #     normalizer = preprocessing.Normalizer().fit(feature)  # 归一化
    #     feature = normalizer.transform(feature)
    # except Exception:
    #     for f in feature:
    #         print(f)
    #     return
    #
    # # 训练和测试
    # w = [[i] for i in range(trainBegin,trainEnd)]
    #weight=np.array(w)
    dtrain = xgb.DMatrix(feature[trainBegin:trainEnd:, ], label=target[trainBegin:trainEnd].ravel())

    param = {}
    param['objective'] = 'reg:linear'
    param['booster'] = 'gbtree'
    param['eta'] = 0.03
    param['max_depth'] = 3
    param['eval_metric'] = 'rmse'
    param['silent'] = 1
    num_round = 2000

    # # # # cv_num_round = 1000
    # print(xgb.cv(param,dtrain,  num_round, nfold = 10, show_progress=False))

    # evallist  = [(dtest,'eval'), (dtrain,'train')] 验证
    # 第几个月 第几周 是否休息 是否新歌


    bst = xgb.train(param, dtrain, num_round)


    # 预测值
    dpredict = xgb.DMatrix(feature[predictBegin:predictEnd:, ])
    ypred = bst.predict(dpredict)
    return ypred


#建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

# 预测
def predict(train_begin_Ds, train_end_Ds, predict_begin_Ds, predict_end_Ds, out_file_name):
    f = open(out_file_name, "w")  # 存放预测结果的文件

    # 获得每个人的特征进行训练
    select_str = "SELECT DISTINCT(artist_id) FROM songs"
    artists = np.array(conn.execute(select_str).fetchall())[:, 0]

    for artist_id in artists:
        # 每个人查询
        sql = "select Ds,playCount from statistics where artist_id='%s' and Ds>='%s' and Ds<='%s'" % (artist_id,train_begin_Ds,train_end_Ds)

        result = np.array(conn.execute(sql).fetchall())

        train_x = None

        for Ds in result[:,0]:
            if train_x is None:
              train_x = get_features(Ds,conn)
            else:
              train_x = np.row_stack((train_x, get_features(Ds,conn)))


        train_y = np.array(result[:,1], dtype=np.int32)
        # 平滑
        smooth_train_y = train_y
        for i in range(5):
            smooth_train_y = smooth.weight_smooth(smooth_train_y)
        for i in range(3):
            smooth_train_y = smooth.weight_smooth2(smooth_train_y)
        smooth_train_y.shape = (len(smooth_train_y), 1)


        predict_x = get_features_between(predict_begin_Ds,predict_end_Ds,conn)


        # 训练
        param = {}
        param['objective'] = 'reg:linear'
        param['booster'] = 'gbtree'
        param['eta'] = 0.03
        param['max_depth'] = 3
        param['eval_metric'] = 'rmse'
        param['silent'] = 1
        num_round = 2000
        # # # # cv_num_round = 1000
        # print(xgb.cv(param,dtrain,  num_round, nfold = 10, show_progress=False))
        # evallist  = [(dtest,'eval'), (dtrain,'train')] 验证

        dtrain = xgb.DMatrix(train_x, label=smooth_train_y.ravel())
        bst = xgb.train(param, dtrain, num_round)
        dpredict = xgb.DMatrix(predict_x)
        pre = bst.predict(dpredict)

        #rule
        pre = rule.modify(artist_id,pre)

        # 写值
        predict_begin = (datetime.datetime.strptime(predict_begin_Ds, '%Y%m%d') - day_start).days
        predict_end = (datetime.datetime.strptime(predict_end_Ds, '%Y%m%d') - day_start).days + 1
        writer.writeResult(f, pre, range(predict_begin, predict_end), artist_id)
        # break

        plt.clf()
        plt.title(artist_id)
        plt.xlabel('Date')
        plt.ylabel('Plays')

        ls_Ds = [datetime.datetime.strptime(Ds, '%Y%m%d') for Ds in result[:,0]]

        plt.plot(ls_Ds, np.array(train_y, dtype=np.int32), marker='o',color='b')
        plt.plot(ls_Ds, np.array(smooth_train_y, dtype=np.int32),color='r')

        plt.plot(time.get_date_range(predict_begin_Ds,predict_end_Ds), pre, color='g')
        plt.savefig('../data/predict/6.7/%s.png' % artist_id)


    # 关闭文件
    f.close()
