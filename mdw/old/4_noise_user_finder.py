import sqlite3
import numpy as np

con = sqlite3.connect('../data/mars_tianchi.db')
# 确认表
check_str = "DROP TABLE IF EXISTS noise_user"
con.execute(check_str)

create_str = "create table noise_user (artist_id TEXT, DS TEXT,user_id TEXT ,playCount INTEGER)"
con.execute(create_str)


# 处理依据：正态分布，选取（平均值 + 1 * 标准差）作为上限阈值，或者50首，但是太小的不考虑 30首
def deal_each_noise_item(artist_id,DS,playCount):
    #print("deal :%s %s %s" % (artist_id,DS,playCount))
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
    normal_threshold = 40

    for i in range(len(values)):
        if values[i] <= normal_threshold:
            continue
        if values[i] > threshold:
            insert_str = "INSERT INTO noise_user (artist_id,DS,user_id,playCount) VALUES (?,?,?,?)"
            con.execute(insert_str,(artist_id,DS,user_ids[i],playCounts[i]))
    con.commit()

select_str = 'SELECT * FROM noise'
result = np.array(con.execute(select_str).fetchall())
index = 0
for item in result:
    artist_id = item[0]
    DS = item[1]
    playCount = item[2]
    if index % 100 == 0:
        print(index)
    deal_each_noise_item(artist_id, DS, playCount)
    index += 1
print(index)
print('done')
