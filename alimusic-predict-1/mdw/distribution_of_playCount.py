#统计大家每小时听一首歌次数的分布
import sqlite3

import numpy as np
from matplotlib import  pyplot as plt

from hdc import query

# 建立连接
con = sqlite3.connect('../data/mars_tianchi.db')

dic = {};

def deal_2(artist_id):
    select_str = "select playCount,Count(*) from statistics_%s group by playCount" % artist_id
    result = np.array(con.execute(select_str).fetchall())
    playCounts = result[:,0]
    nums = result[:,1]
    for i in range(len(playCounts)):
        playCount = playCounts[i]
        num = nums[i]
        if playCount in dic:
            dic[playCount] += num
        else:
            dic[playCount] = num

for item in con.execute("SELECT DISTINCT artist_id FROM songs").fetchall():
    artist_id = item[0]
    deal_2(artist_id)

print("done")


def key_cmp(k1,k2):
    return int(k1) -int(k2)

sorted(dic)

x = []
y = []
for i in dic:
    x.append(int(i))
    y.append(dic[i])

for i in sorted(x):
   print("%s,%s" % (i, dic[i]))

plt.cla()
plt.title('playCount distribution')
plt.xlabel('playCount')
plt.ylabel('appear num')
plt.plot(x,y)
plt.show()
#plt.savefig('../data/sum_day_of_week/%s.png' % artist_id)
