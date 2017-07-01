import sqlite3
import numpy as np
import time

con = sqlite3.connect('../data/mars_tianchi.db')

def deal_user_noise(artist_id, DS, user_id, playCount):
    # print("deal :%s %s %s %s" % (artist_id,DS,user_id,playCount))
    select_str = "SELECT song_id,gmt_create,COUNT (*) FROM user_actions_%s WHERE DS='%s' AND user_id='%s' AND action_type=1 GROUP BY gmt_create,song_id" % (
    artist_id, DS, user_id)
    result = np.array(con.execute(select_str).fetchall())
    # song_ids = np.array(result[:,0])
    # gmt_creates = np.array(result[:,1])
    playCounts = np.array(result[:, 2])
    values = np.array(playCounts, dtype='int')

    wrong_num = 0;
    max_num_per_hour = 15;
    for i in range(len(values)):
        if values[i] <= max_num_per_hour:
            continue
        else:
            wrong_num += values[i] - max_num_per_hour;
    if wrong_num > 0:
        update_str = "UPDATE statistics_%s SET playCount2 = playCount2 - %d WHERE DS='%s'" % (artist_id, wrong_num, DS)
        con.execute(update_str)


start = time.clock()

select_str = 'SELECT * FROM noise_user'
result = np.array(con.execute(select_str).fetchall())
index = 0
for item in result:
    artist_id = item[0]
    DS = item[1]
    user_id = item[2]
    playCount = int(item[3])
    if index % 100 == 0:
        print(index)
    deal_user_noise(artist_id, DS, user_id, playCount)
    index += 1
print(index)
con.commit()

end = time.clock()
print("done cost: %f s" % (end - start))
