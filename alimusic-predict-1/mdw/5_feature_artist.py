import datetime
import sqlite3

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

# 之前的表删除
check_str = "DROP TABLE IF EXISTS feature_artist"
conn.execute(check_str)

# 建表
create_str = "create table feature_artist (artist_id TEXT, sum_of_songs INTEGER," \
             "songs_0_1 INTEGER ,songs_0_5 INTEGER,songs_5_10 INTEGER,songs_10_20 INTEGER,songs_20 INTEGER," \
             "song_init_plays INTEGER,avg_song_init_plays INTEGER," \
             "language_0 INTEGER,language_1 INTEGER,language_2 INTEGER,language_3 INTEGER,language_4 INTEGER,language_11 INTEGER,language_12 INTEGER,language_14 INTEGER,language_100 INTEGER," \
             "sum_of_play INTEGER, sum_of_download INTEGER ,sum_of_collect INTEGER," \
             "sum_of_listened_songs INTEGER )"
conn.execute(create_str)

for item in conn.execute("SELECT DISTINCT artist_id,Gender FROM songs").fetchall():
    artist_id = item[0]
    print(artist_id)
    # 歌曲总数
    sum_of_songs = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s'" % artist_id).fetchall()[0][0]
    # 1年内的歌曲数
    songs_0_1 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=20150101" % artist_id).fetchall()[0][0]
    # 5年内的歌曲数
    songs_0_5 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=20100101" % artist_id).fetchall()[0][0]
    # 5到10年内的歌曲数
    songs_5_10 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=20050101 AND publish_time<20100101" % artist_id).fetchall()[0][0]
    # 10到20年内的歌曲数
    songs_10_20 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time>=19950101 AND publish_time<20050101" % artist_id).fetchall()[0][0]
    # 20年以上的歌曲数
    songs_20 = conn.execute("SELECT COUNT (DISTINCT (song_id)) FROM songs WHERE artist_id='%s' AND publish_time<19950101" % artist_id).fetchall()[0][0]
    # 初始播放总数
    song_init_plays = conn.execute("SELECT SUM (song_init_plays) FROM songs WHERE artist_id='%s'" % artist_id).fetchall()[0][0]
    # 平均播放数，整数
    avg_song_init_plays = song_init_plays / sum_of_songs
    # 各种语言歌曲数量
    language_0 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=0" % artist_id).fetchall()[0][0]
    language_1 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=1" % artist_id).fetchall()[0][0]
    language_2 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=2" % artist_id).fetchall()[0][0]
    language_3 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=3" % artist_id).fetchall()[0][0]
    language_4 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=4" % artist_id).fetchall()[0][0]
    language_11 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=11" % artist_id).fetchall()[0][0]
    language_12 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=12" % artist_id).fetchall()[0][0]
    language_14 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=14" % artist_id).fetchall()[0][0]
    language_100 = conn.execute("SELECT COUNT (*) FROM songs WHERE artist_id='%s' AND Language=100" % artist_id).fetchall()[0][0]

    Ds_trainn_end = "20151030"

    # 播放总数
    sum_of_play = conn.execute("SELECT SUM (playCount) FROM statistics_%s WHERE Ds<=%s" % (artist_id,Ds_trainn_end)).fetchall()[0][0]
    # 下载总数
    sum_of_download = conn.execute("SELECT Count(*) FROM user_actions_%s WHERE action_type = 2 And Ds<=%s" % (artist_id,Ds_trainn_end)).fetchall()[0][0]
    # 收藏总数
    sum_of_collect = conn.execute("SELECT Count(*) FROM user_actions_%s WHERE action_type = 3 And Ds<=%s" % (artist_id,Ds_trainn_end)).fetchall()[0][0]
    # 听过歌曲数
    sum_of_listened_songs = conn.execute("SELECT Count(DISTINCT (song_id)) FROM statistics_%s WHERE Ds<=%s" % (artist_id,Ds_trainn_end)).fetchall()[0][0]

    insert_str = "insert into  feature_artist (artist_id," \
                 "sum_of_songs,songs_0_1,songs_0_5,songs_5_10,songs_10_20,songs_20," \
                 "song_init_plays,avg_song_init_plays," \
                 "language_0,language_1,language_2,language_3,language_4,language_11,language_12,language_14,language_100," \
                 "sum_of_play, sum_of_download ,sum_of_collect," \
                 "sum_of_listened_songs)" \
                 "VALUES (?," \
                 "?,?,?,?,?,?," \
                 "?,?," \
                 "?,?,?,?,?,?,?,?,?," \
                 "?,?,?," \
                 "?)"
    item = (artist_id,
            sum_of_songs,songs_0_1,songs_0_5,songs_5_10,songs_10_20,songs_20,
            song_init_plays,int(avg_song_init_plays),
            language_0,language_1,language_2,language_3,language_4,language_11,language_12,language_14,language_100,
            sum_of_play, sum_of_download ,sum_of_collect,
            sum_of_listened_songs)
    conn.execute(insert_str, item)
conn.commit()

