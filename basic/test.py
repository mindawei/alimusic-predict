
import numpy as np
import sqlite3
import datetime
from sklearn import preprocessing

day_start = datetime.datetime.strptime("20150301", '%Y%m%d')


# 获得特征
def get_feature_time(Ds):
    feature_time = []
    day_time = datetime.datetime.strptime(Ds, '%Y%m%d')
    Ds = day_time.strftime("%Y%m%d")

    # 距离 20150301 第几天 day_offset
    day_offset = (day_time - day_start).days
    feature_time.append(day_offset)
    # 距离 20150302(星期一) 第几周 day_offset
    week_offset = 0
    if day_offset > 0:
        week_offset = (day_offset - 1) / 7
    feature_time.append(week_offset)
    # 距离 20150301 第几个月 month_offset
    month_offset = day_time.month - day_start.month
    feature_time.append(month_offset)

    # 周几
    day_of_week = day_time.weekday()
    enc = preprocessing.OneHotEncoder()
    enc.fit([[0],[1],[2],[3],[4],[5],[6]])
    for i in enc.transform([[day_of_week]]).toarray()[0]:
        feature_time.append(i)

    # 是否周末
    is_weekend = 0
    if 5 <= day_of_week <= 6:
        is_weekend = 1
    feature_time.append(is_weekend)

    # 是否节假日
    is_festival = 0
    if "20150501" <= Ds <= "20150503":
        is_festival = 1
    if "20150620" <= Ds <= "20150622":
        is_festival = 1
    if "20150926" <= Ds <= "20150928":
        is_festival = 1
    if "20151001" <= Ds <= "20151007":
        is_festival = 1
    feature_time.append(is_festival)
    return np.array(feature_time,dtype=np.int32)



# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')


def get_feature_artist(artist_id):
    feature_artist = []
    # 歌曲总数
    sum_of_songs = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s'" % artist_id).fetchall()[0][0]
    feature_artist.append(sum_of_songs)

    # 5年内的歌曲数
    songs_0_5 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=20100101" % artist_id).fetchall()[0][0]
    feature_artist.append(songs_0_5)

    # 5到10年内的歌曲数
    songs_5_10 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=20050101 AND publish_time<20100101" % artist_id).fetchall()[0][0]
    feature_artist.append(songs_5_10)

    # 10到20年内的歌曲数
    songs_10_20 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=19950101 AND publish_time<20050101" % artist_id).fetchall()[0][0]
    feature_artist.append(songs_10_20)

    # 20年以上的歌曲数
    songs_20 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time<19950101" % artist_id).fetchall()[0][0]
    feature_artist.append(songs_20)

    # 初始播放总数
    song_init_plays = conn.execute("SELECT SUM (song_init_plays) FROM songs WHERE artist_id='%s'" % artist_id).fetchall()[0][0]
    feature_artist.append(song_init_plays)

    # 平均播放数，整数
    avg_song_init_plays = song_init_plays / sum_of_songs
    feature_artist.append(avg_song_init_plays)

    # 各种语言歌曲数量
    language_dict = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        11: 0,
        12: 0,
        14: 0,
        100: 0
    }
    for item in conn.execute("SELECT Language,COUNT (*) FROM songs WHERE artist_id='%s' GROUP BY Language" % artist_id).fetchall():
        language_dict[item[0]] = item[1]
    for language in language_dict:
        feature_artist.append(language_dict[language])

    # 播放总数
    sum_of_play = conn.execute("SELECT SUM (playCount) FROM statistics_%s" % artist_id).fetchall()[0][0]
    feature_artist.append(sum_of_play)

    # 下载总数
    sum_of_download = conn.execute("SELECT Count(*) FROM user_actions_%s WHERE action_type = 2" % artist_id).fetchall()[0][0]
    feature_artist.append(sum_of_download)

    # 收藏总数
    sum_of_collect = conn.execute("SELECT Count(*) FROM user_actions_%s WHERE action_type = 3" % artist_id).fetchall()[0][0]
    feature_artist.append(sum_of_collect)

    # 听过歌曲数
    sum_of_listened_songs = conn.execute("SELECT Count(DISTINCT (song_id)) FROM statistics_%s" % artist_id).fetchall()[0][0]
    feature_artist.append(sum_of_listened_songs)

    return np.array(feature_artist,dtype=np.int32)


artist_id = '0c80008b0a28d356026f4b1097041689'
# 艺人特征
feature_artist = conn.execute("SELECT * FROM feature_artist WHERE artist_id='%s'" % artist_id).fetchall()[0]
feature_artist = np.array(feature_artist,)[4:]
feature_artist = np.array(feature_artist,dtype=np.int32)
print(feature_artist)

print(get_feature_artist(artist_id))







