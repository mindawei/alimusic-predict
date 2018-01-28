# 根据艺人名字进行分区
import sqlite3
import numpy as np

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')


# 创建每个艺人的表
def create_user_actions_of_artist(artist_id):
    # 新建艺人相关的听歌事件表
    create_str = "create table user_actions_%s (user_id TEXT, song_id TEXT, gmt_create INTEGER, action_type INTEGER, Ds TEXT)" % artist_id
    conn.execute(create_str)
    # 查询艺人相关数据
    select_str = "SELECT * FROM user_actions WHERE song_id IN (SELECT song_id FROM songs WHERE artist_id ='%s' )" % artist_id
    result = conn.execute(select_str).fetchall()
    # 逐条插入
    for item in result:
        insert_str = "insert into user_actions_%s (user_id, song_id, gmt_create, action_type, Ds)values (?,?,?,?,?)" % artist_id
        conn.execute(insert_str, item)
    conn.commit()
    print("table user_actions_%s is created" % artist_id)


select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(conn.execute(select_str).fetchall())[:, 0]

for artist_id in artists:
    create_user_actions_of_artist(artist_id)
print("done")

