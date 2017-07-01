import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


# 显示每位艺人每天总的播放数的变化
def show_palys_trend_of_each_artist(artist_id):
    # 数据库查询
    con = sqlite3.connect('../data/mars_tianchi.db')
    select_str = "select Ds,playCount,playCount2,playCount3 as user_num from statistics_%s " % artist_id
    result = np.array(con.execute(select_str).fetchall())
    # 处理数据获得x,y
    x_str = result[:, 0]
    x = []
    for x_i in x_str:
        x.append(datetime.strptime(x_i, '%Y%m%d'))
    y1 = np.array(result[:, 1],dtype='int')
    y2 = np.array(result[:, 2],dtype='int')
    y3 = np.array(result[:, 3],dtype='int')
    y4 = []
    for i in range(len(x)):
        if y2[i] < y3[i]:
            y4.append(y2[i])
        else:
            y4.append(y3[i])
    # 绘图及保存到目录下
    plt.clf()
    plt.title(artist_id)
    plt.xlabel('Date')
    plt.ylabel('Plays')
    plt.plot(x, y1, marker='o',color='b')
    plt.plot(x, y2, marker='s',color='r')
    plt.savefig('../data/artists/%s.png' % artist_id)


# 显示艺人们每天的听歌数量的变化
def show_palys_trend_of_artists():
    # 获得艺人
    con = sqlite3.connect('../data/mars_tianchi.db')
    select_str = "SELECT DISTINCT(artist_id) FROM songs"
    artists = np.array(con.execute(select_str).fetchall())[:, 0]
    # 对每个艺人进行处理
    for artist_id in artists:
        show_palys_trend_of_each_artist(artist_id)


# 艺人们总体播放情况
show_palys_trend_of_artists()