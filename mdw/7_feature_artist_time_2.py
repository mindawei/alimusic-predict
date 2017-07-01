import datetime
import sqlite3
from sklearn import linear_model
import  numpy as np

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

check_str = "DROP TABLE IF EXISTS feature_artist_time_2"
conn.execute(check_str)

create_str = "create table feature_artist_time_2 (artist_id TEXT,Ds TEXT," \
    "rec_play_mean FLOAT,rec_play_std FLOAT,rec_play_min FLOAT,rec_play_max FLOAT,rec_play_median FLOAT,rec_play_last FLOAT,rec_play_trend FLOAT," \
             "all_play_mean FLOAT,all_play_std FLOAT,all_play_min FLOAT,all_play_max FLOAT,all_play_median FLOAT,all_play_trend FLOAT)"
conn.execute(create_str)

# 获得几天之前的
def get_before_day(Ds,offset):
    date_time = datetime.datetime.strptime( Ds, '%Y%m%d')
    date_time -= datetime.timedelta(days=offset)
    return date_time.strftime("%Y%m%d")


def get_trend(Y):
    X = []
    for i in range(len(Y)):
        X.append([i])
    clf = linear_model.LinearRegression()
    clf.fit(X, Y)
    trend = clf.coef_[0]
    return trend


def get_feature_recent(Y):
    y_mean = Y.mean()          # 平均值
    y_std = Y.std()            # 标准差
    y_min = Y.min()            # 最小值
    y_max = Y.max()            # 最大值
    y_median = np.median(Y)    # 中位数
    y_last = Y[len(Y)-1]       # 最新值
    y_trend = get_trend(Y)     # 斜率
    return float(y_mean),float(y_std),float(y_min),float(y_max),float(y_median),float(y_last),float(y_trend)


def get_feature_all(Y):
    y_mean = Y.mean()          # 平均值
    y_std = Y.std()            # 标准差
    y_min = Y.min()            # 最小值
    y_max = Y.max()            # 最大值
    y_median = np.median(Y)    # 中位数
    y_trend = get_trend(Y)     # 斜率
    return float(y_mean),float(y_std),float(y_min),float(y_max),float(y_median),float(y_trend)


# def get_feature_hour(X,Y):
#     for i in range(len(Y)):
#         if Y[i] > 24:
#             Y[i] = 24
#     y_mean = Y.mean()          # 平均值
#     y_std = Y.std()            # 标准差
#     y_var = Y.var()            # 方差
#     y_min = Y.min()            # 最小值
#     y_max = Y.max()            # 最大值
#     y_median = np.median(Y)    # 中位数
#     y_ptp = Y.ptp()            # 最大最小之差
#     y_trend = get_trend(X, Y)  # 斜率
#     return y_mean,y_std,y_var,float(y_min),float(y_max),float(y_median),float(y_ptp),y_trend

ls_artist_id = []
for item in conn.execute("SELECT DISTINCT artist_id FROM songs").fetchall():
    ls_artist_id.append(item[0])


for artist_id in ls_artist_id:
    print(artist_id)
    result = conn.execute("SELECT Sum(playCount) FROM statistics_%s WHERE Ds>=%s And Ds<=%s GROUP BY Ds ORDER BY  Ds ASC " % (artist_id, "20150301", "20150830")).fetchall()
    result = np.array(result,dtype=int)

    Ds_data_begin = datetime.datetime.strptime('20150301','%Y%m%d')  # 从3月1号有数据
    Ds_train_begin = datetime.datetime.strptime('20150315', '%Y%m%d')  # 训练开始区域，有数据
    Ds_train_end = datetime.datetime.strptime('20150731', '%Y%m%d')    # 从该时段开始进入预测无数据区域
    # Ds_train_end = datetime.datetime.strptime('20150830', '%Y%m%d')    # 从该时段开始进入预测无数据区域

    day_time = datetime.datetime.strptime('20150301', '%Y%m%d')      # 从3月2号开始有特征
    while day_time <= datetime.datetime.strptime("20151030", '%Y%m%d'): # 特征从 3.29号到 10.30号
        end = 0
        if day_time <= Ds_train_begin:  # Ds_train_begin前的用Ds_train_begin替代
            end = (Ds_train_begin - Ds_data_begin).days
        elif day_time <= Ds_train_end:
            end = (day_time - Ds_data_begin).days
        else:  # Ds_train_end后的用Ds_train_end替代
            end = (Ds_train_end - Ds_data_begin).days
        begin = end - 14 # 最近14天
        Y_play = result[begin:end, 0]
        rec_play_mean,rec_play_std,rec_play_min,rec_play_max,rec_play_median,rec_play_last,rec_play_trend = get_feature_recent(Y_play)

        Y_play = result[0:end, 0] # 全部
        all_play_mean,all_play_std,all_play_min,all_play_max,all_play_median,all_play_trend = get_feature_all(Y_play)

        insert_str = "insert into feature_artist_time_2 (artist_id ,Ds," \
                     "rec_play_mean,rec_play_std,rec_play_min,rec_play_max,rec_play_median,rec_play_last,rec_play_trend," \
                     "all_play_mean,all_play_std,all_play_min,all_play_max,all_play_median,all_play_trend)" \
                   "VALUES (?,?," \
                     "?,?,?,?,?,?,?," \
                     "?,?,?,?,?,?)"

        Ds = day_time.strftime("%Y%m%d")
        item = (artist_id ,Ds ,
                rec_play_mean,rec_play_std,rec_play_min,rec_play_max,rec_play_median,rec_play_last,rec_play_trend,
                 all_play_mean,all_play_std,all_play_min,all_play_max,all_play_median,all_play_trend)

        conn.execute(insert_str,item)
        day_time += datetime.timedelta(days=1)
conn.commit()
print("done")