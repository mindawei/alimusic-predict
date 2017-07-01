import numpy as np
import datetime
from sklearn import preprocessing
import  sqlite3


# 获得特征
def get_features(Ds, conn):
    feature = conn.execute("SELECT * FROM feature_time WHERE Ds = %s" % Ds).fetchall()[0]
    feature = np.array(feature)[1:2]
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
