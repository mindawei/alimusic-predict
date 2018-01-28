# 根据艺人名字进行分区
import sqlite3
import time

import numpy as np

from hdc import query

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')


# 创建每个艺人的表
def old_create_user_actions_statistics_of_artist(artist_id):
    # 查询艺人相关数据
    select_str = "SELECT DISTINCT user_id FROM user_actions_%s" % (artist_id)
    result = np.array(conn.execute(select_str).fetchall())
    user_ids = result[:, 0]

    create_str = "create table user_actions_statistics_%s (user_id TEXT, DS TEXT, playCount INTEGER)" % artist_id
    conn.execute(create_str)

    print('deal %s' % artist_id)
    start = time.clock()
    for user_id in user_ids:
        insert_str = "INSERT INTO user_actions_statistics_%s (user_id, DS, playCount) " \
                 "SELECT user_id,DS,COUNT(*) FROM user_actions_%s WHERE user_id='%s'AND action_type=1 GROUP BY DS" \
                 % (artist_id, artist_id, user_id)
        conn.execute(insert_str)
    conn.commit()
    end = time.clock()
    print("cost: %f s" % (end - start))
    print('- - - - - - - - - ')


# 创建每个艺人的表
def create_user_actions_statistics_of_artist(artist_id):

    # 确认表
    check_str = "DROP TABLE IF EXISTS statistics_%s" % (artist_id)
    conn.execute(check_str)

    create_str = "create table statistics_%s (DS TEXT, playCount INTEGER ,download INTEGER ,collect INTEGER,fans INTEGER )" % artist_id
    conn.execute(create_str)

    print('deal %s' % artist_id)
    start = time.clock()
    insert_str = "INSERT INTO statistics_%s (DS, playCount) " \
                 " SELECT DS,COUNT(*) FROM user_actions_%s WHERE action_type ='1' GROUP BY DS" \
                 % (artist_id, artist_id)
    conn.execute(insert_str)
    conn.commit()
    end = time.clock()
    print("cost: %f s" % (end - start))
    print('- - - - - - - - - ')

q = query.Query('../data/mars_tianchi.db')
q.queryAllArtists()
for artist_id in q.allArtists:
    create_user_actions_statistics_of_artist(artist_id)
print('done')