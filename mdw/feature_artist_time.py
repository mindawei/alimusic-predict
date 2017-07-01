import datetime
import sqlite3

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

# 之前的表删除
check_str = "DROP TABLE IF EXISTS feature_artist_time"
conn.execute(check_str)

# 建表
create_str = "create table feature_artist_time (artist_id TEXT,Ds TEXT," \
             "num_of_fans INTEGER,num_of_active_hour INTEGER ,num_of_plays INTEGER )"
conn.execute(create_str)


# 处理一条
def deal_one(artist_id,Ds):
    # 用户数量
    num_of_fans = conn.execute("SELECT COUNT (DISTINCT (user_id)) FROM user_actions_%s WHERE Ds<'%s'" % (artist_id, Ds)).fetchall()[0][0]
    # 用户总的活跃小时数
    num_of_active_hour = conn.execute("SELECT Count(*) FROM (SELECT  user_id,gmt_create FROM user_actions_%s WHERE Ds<'%s' GROUP BY user_id,gmt_create)" % (artist_id, Ds)).fetchall()[0][0]
    # 之前的播放数
    num_of_plays = conn.execute("SELECT Count(*) FROM user_actions_%s WHERE Ds<'%s'" % (artist_id, Ds)).fetchall()[0][0]

    insert_str = "insert into  feature_artist_time (artist_id,Ds," \
                 "num_of_fans,num_of_active_hour,num_of_plays)" \
                 "VALUES (?,?," \
                 "?,?,?)"
    item = (artist_id,Ds,num_of_fans,num_of_active_hour,num_of_plays)
    conn.execute(insert_str, item)


# 根据艺人和时间生成动态特征
for item in conn.execute("SELECT DISTINCT artist_id FROM songs").fetchall():
    artist_id = item[0]
    print(artist_id)
    day_time = datetime.datetime.strptime("20150301", '%Y%m%d')
    day_end = datetime.datetime.strptime("20151030", '%Y%m%d')
    while day_time <= day_end:
        Ds = day_time.strftime("%Y%m%d")
        deal_one(artist_id, Ds)
        day_time += datetime.timedelta(days=1)
    break
conn.commit()

