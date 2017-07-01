import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


conn = sqlite3.connect('../data/mars_tianchi.db')

check_str = "DROP TABLE IF EXISTS statistics"
conn.execute(check_str)

create_str = "create table statistics (artist_id TEXT, Ds TEXT, playCount INTEGER)"
conn.execute(create_str)

# 显示每位艺人每天总的播放数的变化
def update_each_artist(artist_id):
    print(artist_id)
    # 数据库查询
    select_str = "select Ds,sum(playCount) from statistics_%s GROUP BY DS" % artist_id
    result = np.array(conn.execute(select_str).fetchall())
    # 处理数据获得x,y
    ds = result[:, 0]
    plays = result[:,1]

    for i in range(len(ds)):
        Ds = ds[i]
        playCount = plays[i]
        sql ="insert into statistics (artist_id , Ds, playCount) values(?,?,?)"
        item = (artist_id,Ds,int(playCount))
        conn.execute(sql,item)


select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(conn.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
        update_each_artist(artist_id)
        print(artist_id)
conn.commit()
print('done')

