import numpy as np
import sqlite3
con = sqlite3.connect('../data/mars_tianchi.db')

# 处理依据：正态分布，选取（平均值 + 1 * 标准差）作为上限阈值，或者50首，但是太小的不考虑 30首
def reduce_influence_by_item(artist_id,DS):
    # 知道每个人的在这天的变化
    select_str = "SELECT user_id,COUNT(*) FROM user_actions_%s WHERE action_type=1 AND DS='%s' GROUP BY user_id" % (artist_id,DS)
    result = np.array(con.execute(select_str).fetchall())

    user_ids = np.array(result[:,0])
    playCounts = np.array(result[:,1])
    values = np.array(playCounts,dtype = 'int')

    # 计算阈值
    mean = values.mean()
    std = values.std()
    threshold = int(mean + 1 *std)
    normal_threshold = 60

    # 找出影响大的
    high_influence_lsit = []
    for i in range(len(values)):
        if values[i] < normal_threshold:
            continue
        if values[i] > threshold:
            high_influence_lsit.append(values[i])

    if len(high_influence_lsit) == 0:
        update_str = "UPDATE statistics_%s SET playCount3 = %d  WHERE DS='%s'" % (artist_id,values.sum(),DS)
        con.execute(update_str)
        return

    # 用有效平均值代替影响大的值
    high_influence = np.array(high_influence_lsit)
    left_sum = values.sum() - high_influence.sum()
    left_num = len(values)-len(high_influence)
    left_avg = left_sum / left_num
    valid_sum = left_avg * len(high_influence)
    playCount3 = int(left_sum + valid_sum)

    update_str = "UPDATE statistics_%s SET playCount3 = %d  WHERE DS='%s'" % (artist_id,playCount3,DS)
    con.execute(update_str)


# 获得艺人
select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(con.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
    print("deal %s" % artist_id)
    select_str = "SELECT DS FROM statistics_%s " % artist_id
    result = np.array(con.execute(select_str).fetchall())[:, 0]
    for DS in result:
        reduce_influence_by_item(artist_id,DS)
con.commit()
print('done')
