# 分析出 2b7fedeea967becd9408b896de8ff903 异常部分
#  ['20150626' '236']
#  ['20150627' '271']
import sqlite3

import numpy as np


# 显示每位艺人每天总的播放数的变化
def abnormal_analyze(artist_id):
    # 数据库查询
    con = sqlite3.connect('../data/mars_tianchi.db')
    select_str = "SELECT COUNT (DISTINCT (user_id)) FROM user_actions_%s  WHERE action_type='1'" % (artist_id)
    result = np.array(con.execute(select_str).fetchall())
    num = result[0][0]
    return num
    #select_str = "SELECT song_id,COUNT (*) FROM user_actions_%s " \
    #             "WHERE song_id IN (SELECT song_id FROM songs WHERE artist_id ='%s' ) " \
    #             "AND Ds='20150626' AND action_type='1' GROUP BY song_id" % (artist_id,artist_id)


artist_id = '2b7fedeea967becd9408b896de8ff903'
con = sqlite3.connect('../data/mars_tianchi.db')
select_str = "SELECT DS,COUNT (user_id),COUNT (DISTINCT (user_id)) FROM user_actions_%s  WHERE action_type='1' AND DS ='20150626'" % (artist_id)
result = np.array(con.execute(select_str).fetchall())
print(result)


# 处理依据：正态分布，选取（平均值 + 1 * 标准差）作为上限阈值，或者50首，但是太小的不考虑 30首
def deal_each_noise_item(artist_id,DS):
    print("deal :%s %s" % (artist_id,DS))
    # 知道每个人的在这天的变化
    select_str = "SELECT user_id,COUNT(*) FROM user_actions_%s WHERE action_type=1 AND DS='%s' GROUP BY user_id" % (artist_id,DS)
    result = np.array(con.execute(select_str).fetchall())

    user_ids = np.array(result[:,0])
    playCounts = np.array(result[:,1])
    values = np.array(playCounts,dtype = 'int')
    print(result)

    # 计算阈值
    mean = values.mean()
    std = values.std()
    threshold = int(mean + 1 *std)

    for i in range(len(values)):
        if values[i] < 20:
            continue
        if values[i] > threshold:
            print(user_ids[i])
deal_each_noise_item( '2b7fedeea967becd9408b896de8ff903','20150626')


def deal_user_noise(artist_id, DS, user_id, playCount):
    # print("deal :%s %s %s %s" % (artist_id,DS,user_id,playCount))
    select_str = "SELECT song_id,gmt_create,COUNT (*) FROM user_actions_%s WHERE DS='%s' AND user_id='%s' AND action_type=1 GROUP BY gmt_create,song_id" % (
    artist_id, DS, user_id)
    result = np.array(con.execute(select_str).fetchall())
    playCounts = np.array(result[:, 2])
    values = np.array(playCounts, dtype='int')
    print(result)
    print(values.sum())

    wrong_num = 0;
    max_num_per_hour = 15;
    for i in range(len(values)):
        if values[i] < max_num_per_hour:
            continue
        else:
            wrong_num += values[i];
    if wrong_num > 0:
        print(user_id)
        print(wrong_num)
deal_user_noise( '2b7fedeea967becd9408b896de8ff903','20150626','f7396c89ca77110dfb7fd435a02290c1',231)

v = np.array([1,2,1,1,231])
print(v.mean())
print(v.std())
print(v.mean()+v.std())