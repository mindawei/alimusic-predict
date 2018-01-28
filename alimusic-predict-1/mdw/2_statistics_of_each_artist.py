import sqlite3
import numpy as np

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')


# 创建每个艺人的表
def create_user_actions_statistics_of_artist(artist_id):
    check_str = "DROP TABLE IF EXISTS statistics_%s" % artist_id
    conn.execute(check_str)

    # 新建艺人相关的听歌事件表
    create_str = "create table statistics_%s (user_id TEXT, song_id TEXT, gmt_create INTEGER,Ds TEXT,playCount INTEGER )" % artist_id
    conn.execute(create_str)

    insert_str = "insert into statistics_%s (user_id, song_id, gmt_create,Ds,playCount) " \
                 "SELECT user_id,song_id,gmt_create,Ds,count(*) FROM " \
                 "user_actions_%s WHERE action_type = '1' GROUP BY user_id,song_id,gmt_create,DS" % (artist_id,artist_id)
    conn.execute(insert_str)
    conn.commit()
    print("table statistics_%s is created" % artist_id)


select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(conn.execute(select_str).fetchall())[:, 0]

for artist_id in artists:
    create_user_actions_statistics_of_artist(artist_id)
print("done")
