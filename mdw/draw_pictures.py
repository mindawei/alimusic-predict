import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


con = sqlite3.connect('../data/mars_tianchi.db')


# 显示每位艺人每天总的播放数的变化
def show_palys_trend_of_each_artist(artist_id):

    select_str = "select Ds,playCount from statistics_%s " % artist_id
    result = np.array(con.execute(select_str).fetchall())
    y1 = result[:,1]

    # 数据库查询
    select_str = "select Ds,sum(playCount)  from user_actions_%s GROUP  BY DS" % artist_id
    result = np.array(con.execute(select_str).fetchall())
    # 处理数据获得x,y
    x_str = result[:, 0]
    x = []
    for x_i in x_str:
        x.append(datetime.strptime(x_i, '%Y%m%d'))
    y2 = result[:,1]
    # 绘图及保存到目录下
    plt.clf()
    plt.title(artist_id)
    plt.xlabel('Date')
    plt.ylabel('Plays')
    plt.plot(x, y1, marker='o',color='b')
    plt.plot(x, y2, marker='s',color='r')
    plt.savefig('../data/artists/%s.png' % artist_id)



select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(con.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
        show_palys_trend_of_each_artist(artist_id)
print('done')

