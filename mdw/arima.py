from basic import query,time,smooth
import matplotlib.pyplot as plt

q = query.Query()

date_begin = "20150301"
date_end = "20150830"

def draw(artist_id,x,y):
    plt.clf()
    plt.title(artist_id)
    plt.xlabel('Date')
    plt.ylabel('Plays')
    plt.plot(x, y, marker='o',color='b')
    plt.savefig('../data/artists/%s.png' % artist_id)


def draw_smooth(artist_id, x, y1, y2):
    # 绘图及保存到目录下
    plt.clf()
    plt.title(artist_id)
    plt.xlabel('Date')
    plt.ylabel('Plays')
    plt.plot(x, y1, color='b')
    plt.plot(x, y2, color='r')
    plt.savefig('../data/artists/max_5_weight_3_2/%s.png' % artist_id)



for artist_id in q.get_all_artists():
    print(artist_id)
    dates,plays = q.get_xy_of_artist(artist_id,date_begin,date_end)
    dates = time.str_to_date(dates)
    draw_smooth(artist_id, dates, plays, smooth.weight_smooth(plays))

print("done")


# from __future__ import print_function
# import numpy as np
# from scipy import stats
# import pandas as pd
# import matplotlib.pyplot as plt
#
# import statsmodels.api as sm