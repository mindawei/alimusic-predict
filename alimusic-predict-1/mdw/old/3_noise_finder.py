import sqlite3

import numpy as np

from hdc import query

con = sqlite3.connect('../data/mars_tianchi.db')
# 确认表
check_str = "DROP TABLE IF EXISTS noise"
con.execute(check_str)

create_str = "create table noise (artist_id TEXT, DS TEXT ,playCount INTEGER)"
con.execute(create_str)


# 处理依据：正态分布，选取（平均值 + 1 * 标准差）作为上限阈值 0.8 左右
def find_noise(artist_id):
    select_str = "SELECT DS,playCount FROM statistics_%s " % (artist_id)
    result = np.array(con.execute(select_str).fetchall())
    # 取出值
    dates = np.array(result[:,0])
    playCounts = np.array(result[:,1])
    values = np.array(playCounts,dtype = 'int')
    # 计算阈值
    mean = values.mean()
    std = values.std()
    threshold = int(mean + 1 * std)
    normal_threshold = 100

    for i in range(len(values)):
        if values[i] <= normal_threshold:
            continue
        if values[i] >= threshold:
            insert_str = "INSERT INTO noise (artist_id,DS,playCount) VALUES (?,?,?)"
            con.execute(insert_str,(artist_id,dates[i],playCounts[i]))
    con.commit()

q = query.Query('../data/mars_tianchi.db')
q.queryAllArtists()
for artist_id in q.allArtists:
    print('deal %s' % artist_id)
    find_noise(artist_id)
print('done')