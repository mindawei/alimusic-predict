import numpy as np
import datetime
from sklearn import preprocessing
import  sqlite3

enc = preprocessing.OneHotEncoder()
enc.fit([[0],[1],[2],[3],[4],[5],[6]])

day_start = datetime.datetime.strptime("20150301", '%Y%m%d')
day_end = datetime.datetime.strptime("20151030", '%Y%m%d')


# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

# 获得时间特征
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


# 获得艺人特征
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


# 缓存时间特征
day_time = day_start
feature_time_dict = {}

while day_time <= day_end:
    Ds = day_time.strftime("%Y%m%d")
    feature_time_dict[Ds] = get_feature_time(Ds)
    day_time += datetime.timedelta(days=1)
print("feature_time is ok")

# 缓存艺人特征
feature_artist_dict = {}
for item in conn.execute("SELECT DISTINCT artist_id FROM songs").fetchall():
    artist_id = item[0]
    #feature_artist_dict[artist_id] = get_feature_artist(artist_id)
    feature_artist = conn.execute("SELECT * FROM feature_artist WHERE artist_id='%s'" % artist_id).fetchall()[0]
    feature_artist = np.array(feature_artist,)[1:]
    feature_artist = np.array(feature_artist,dtype=np.int32)
    feature_artist_dict[artist_id] = feature_artist
print("feature_artist is ok")


# 获得特征
def get_features(artist_id, Ds, conn):
    # 时间特征
    # feature_time = conn.execute("SELECT * FROM feature_time WHERE Ds='%s'" % Ds).fetchall()[0]
    # feature_time = np.array(feature_time,dtype=np.int32)[1:]
    feature_time = feature_time_dict[Ds]

    # 艺人特征
    # feature_artist = conn.execute("SELECT * FROM feature_artist WHERE artist_id='%s'" % artist_id).fetchall()[0]
    # feature_artist = np.array(feature_artist,)[4:]
    # feature_artist = np.array(feature_artist,dtype=np.int32)
    feature_artist = feature_artist_dict[artist_id]

    feature_artist_time_1 = conn.execute("SELECT * FROM feature_artist_time_1 WHERE artist_id='%s' And Ds = %s" % (artist_id,Ds)).fetchall()[0]
    feature_artist_time_1 = np.array(feature_artist_time_1)[2:]
    feature_artist_time_1 = np.array(feature_artist_time_1,dtype=np.int32)

    # feature_artist_time_2 = conn.execute("SELECT * FROM feature_artist_time_2 WHERE artist_id='%s' And Ds = %s" % (artist_id,Ds)).fetchall()[0]
    # feature_artist_time_2 = np.array(feature_artist_time_2)[5:6]
    # feature_artist_time_2 = np.array(feature_artist_time_2,dtype=np.float32)

    # # 特征拼接 40位`
    feature = np.append(feature_time, feature_artist)
    feature = np.append(feature, feature_artist_time_1)
    # feature = np.append(feature, feature_artist_time_2)

    return feature


# 获得某个区间的特征
def get_features_between(artist_id,Ds_start,Ds_end,conn):
    # 起始日期
    day_time = datetime.datetime.strptime(Ds_start, '%Y%m%d')
    day_end = datetime.datetime.strptime(Ds_end, '%Y%m%d')
    # 初始化
    all_features = get_features(artist_id,day_time.strftime("%Y%m%d"),conn)
    day_time += datetime.timedelta(days=1) #3月1号的用3月2号的,多放一天
    # 获得区间
    while day_time <= day_end:
        one_feature = get_features(artist_id,day_time.strftime("%Y%m%d"),conn)
        all_features = np.row_stack((all_features, one_feature))
        day_time += datetime.timedelta(days=1)
    return all_features
