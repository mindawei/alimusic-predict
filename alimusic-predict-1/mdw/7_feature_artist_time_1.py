import datetime
import sqlite3
from sklearn import linear_model
import numpy as np

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

check_str = "DROP TABLE IF EXISTS feature_artist_time_1"
conn.execute(check_str)

create_str = "create table feature_artist_time_1(artist_id TEXT,Ds TEXT,new_song_off INTEGER,recent_new_song INTEGER )"
conn.execute(create_str)

ls_artist_id = []
for item in conn.execute("SELECT DISTINCT artist_id FROM songs").fetchall():
    ls_artist_id.append(item[0])

for artist_id in ls_artist_id:
    print(artist_id)
    day_time = datetime.datetime.strptime('20150301', '%Y%m%d')
    while day_time <= datetime.datetime.strptime("20151030", '%Y%m%d'):  # 特征从 3.1号到 10.30号
        Ds = day_time.strftime("%Y%m%d")

        # # 今天发布的歌曲数目
        # select_str = "SELECT COUNT (DISTINCT (song_id)) from songs WHERE artist_id='%s' AND publish_time ='%s'"
        # new_song = conn.execute(select_str % (artist_id, Ds)).fetchall()[0][0]

        # 距离最近发布歌曲的天数
        select_str = "SELECT publish_time from songs WHERE artist_id='%s' AND publish_time <='%s' ORDER BY publish_time DESC "
        recent_publish_time = conn.execute(select_str % (artist_id, Ds)).fetchall()[0][0]
        new_song_off = (day_time - datetime.datetime.strptime(recent_publish_time, '%Y%m%d')).days

        # 最近发布的歌曲数目
        select_str = "SELECT COUNT (DISTINCT (song_id)) from songs WHERE artist_id='%s' AND publish_time ='%s'"
        recent_new_song = conn.execute(select_str % (artist_id, recent_publish_time)).fetchall()[0][0]

        insert_str = "insert into feature_artist_time_1 (artist_id ,Ds,new_song_off,recent_new_song) VALUES (?,?,?,?)"
        item = (artist_id, Ds,int(new_song_off),int(recent_new_song))
        conn.execute(insert_str, item)
        day_time += datetime.timedelta(days=1)
conn.commit()
print("done")
