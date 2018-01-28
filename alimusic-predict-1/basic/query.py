"""
    数据库读取文件
"""

import sqlite3
import numpy as np


class Query:
    conn = None

    # 初始化，数据库地址可以替换,查询歌手示例： artists = query.Query().get_all_artists()
    def __init__(self, path='../data/mars_tianchi.db'):
        self.conn = sqlite3.connect(path)

    # 获得所有的艺人的id,返回艺人数组
    def get_all_artists(self):
        sql = "SELECT DISTINCT(artist_id) FROM songs"
        artists = np.array(self.conn.execute(sql).fetchall())[:, 0]
        return artists

    # 获得信息
    def get_xy_of_artist(self,artist_id,date_begin,date_end):
        sql = "select Ds,playCount from statistics where artist_id = '%s' and Ds>=%s and Ds<=%s  order by Ds" % (artist_id,date_begin,date_end)
        dates = np.array(self.conn.execute(sql).fetchall())[:,0]
        plays = np.array(self.conn.execute(sql).fetchall(),dtype=int)[:,1]
        return dates, plays

    # 获得指定艺人所有歌曲的播放总量，注：查询分区后的表
    def get_play_sum_of_artist(self, artist_id):
        select_str = "SELECT COUNT (*) FROM user_actions_%s WHERE action_type = '1'" % artist_id
        play_sum = np.array(self.conn.execute(select_str).fetchall())[0, 0]
        return play_sum

    # 获得指定艺人所有歌曲数
    def get_song_sum_of_artist(self, artist_id):
        select_str = "SELECT COUNT (*) FROM songs WHERE artist_id='%s'" % artist_id
        song_sum = np.array(self.conn.execute(select_str).fetchall())[0, 0]
        return song_sum

    # 获得指定艺人初始热度总数
    def get_song_init_plays_sum_of_artist(self, artist_id):
        select_str = "SELECT SUM (song_init_plays) FROM songs WHERE artist_id='%s'" % artist_id
        song_init_plays_sum = np.array(self.conn.execute(select_str).fetchall())[0, 0]
        return song_init_plays_sum

    # 获得指定艺人歌曲的主要语言
    def get_main_language_of_artist(self, artist_id):
        select_str = "SELECT Language,COUNT (*) AS num FROM songs WHERE artist_id='%s' GROUP BY Language ORDER BY num DESC" % artist_id
        main_language = np.array(self.conn.execute(select_str).fetchall())[0, 0]
        return main_language

    # 获得指定艺人的性别
    def get_gender_of_artist(self, artist_id):
        select_str = "SELECT Gender FROM songs WHERE artist_id='%s' GROUP BY Gender" % artist_id
        gender = np.array(self.conn.execute(select_str).fetchall())[0, 0]
        return gender

