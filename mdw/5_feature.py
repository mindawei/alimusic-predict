import datetime
import sqlite3
from sklearn import linear_model
import  numpy as np
from basic import query

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

check_str = "DROP TABLE IF EXISTS feature"
conn.execute(check_str)

create_str = "create table feature (artist_id TEXT,Ds TEXT,month_offset INTEGER ,week_offset INTEGER ,is_relax INTEGER ,trend FLOAT,new_song_off INTEGER)"
conn.execute(create_str)

# 获得几天之前的
def get_before_day(Ds,offset):
    date_time = datetime.datetime.strptime( Ds, '%Y%m%d')
    date_time -= datetime.timedelta(days=offset)
    return date_time.strftime("%Y%m%d")

for artist_id in query.Query().get_all_artists():
    print(artist_id)


    result = conn.execute("SELECT Sum(playCount) FROM statistics_%s WHERE Ds>=%s And Ds<=%s GROUP BY Ds ORDER BY  Ds ASC " % (artist_id, "20150301", "20150830")).fetchall()
    result = np.array(result,dtype=int)

    day_start = datetime.datetime.strptime('20150301','%Y%m%d')  # 从3月1号有数据
    day_train_begin = datetime.datetime.strptime('20150315', '%Y%m%d')  # 训练开始区域，有数据
    #day_train_end = datetime.datetime.strptime('20150630', '%Y%m%d')    # 从该时段开始进入预测无数据区域
    day_train_end = datetime.datetime.strptime('20150830', '%Y%m%d')    # 从该时段开始进入预测无数据区域

    day_time = datetime.datetime.strptime('20150301', '%Y%m%d')      # 从3月2号开始有特征
    last_trend = 0 #最后的趋势
    while day_time <= datetime.datetime.strptime("20151030", '%Y%m%d'): # 特征从 3.29号到 10.30号

        # 0 距离 20150301 第几个月 month_offset
        month_offset = day_time.month - day_start.month

        # 1 距离 20150302(星期一) 第几周 day_offset
        day_offset = (day_time - day_start).days
        week_offset = 0
        if day_offset > 0:
            week_offset = (day_offset - 1) / 7

        # 2 是否休息
        is_relax = 0
        day_of_week = day_time.weekday()
        if 5 <= day_of_week <= 6:
            is_relax = 1
        Ds = day_time.strftime("%Y%m%d")
        if "20150405" <= Ds <= "20150406":
            is_relax = 1
        if "20150501" <= Ds <= "20150503":
            is_relax = 1
        if "20150620" <= Ds <= "20150622":
            is_relax = 1
        if "20150903" <= Ds <= "20150905":
            is_relax = 1
        if "20150926" <= Ds <= "20150928":
            is_relax = 1
        if "20151001" <= Ds <= "20151007":
            is_relax = 1
        # 调休
        if Ds == "20150906":
            is_relax = 0
        if Ds == "20151010":
            is_relax = 0

        # 3 趋势
        trend = 0
        if day_time <= day_train_begin:  # Ds_train_begin前的用Ds_train_begin替代
            trend = 0
        elif day_time <= day_train_end:
            end = (day_time - day_start).days
            begin = end - 14  # 最近14天
            Y = result[begin:end, 0]
            X = [[i] for i in range(len(Y))]
            clf = linear_model.LinearRegression()
            clf.fit(X, Y)
            trend = clf.coef_[0]
            last_trend = trend
        else:  # Ds_train_end后的用Ds_train_end替代
            trend = last_trend * 0.85
            last_trend = trend

        # 4 距离已经发布的最后一首歌曲的天数
        sql = "SELECT publish_time from songs WHERE artist_id='%s' AND publish_time <='%s' ORDER BY publish_time DESC "
        recent_publish_time = conn.execute(sql % (artist_id, Ds)).fetchall()[0][0]
        new_song_off = (day_time - datetime.datetime.strptime(recent_publish_time, '%Y%m%d')).days

        # 5 如果数据较好的话，可以考虑距离之后新歌的日期

        insert_str = "insert into feature (artist_id ,Ds,month_offset,week_offset,is_relax,trend,new_song_off) VALUES (?,?,?,?,?,?,?)"
        item = (artist_id ,Ds ,month_offset,week_offset,is_relax,trend,new_song_off)
        conn.execute(insert_str,item)
        day_time += datetime.timedelta(days=1)

conn.commit()
print("done")