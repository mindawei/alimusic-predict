import pandas as pd
import sqlite3

# 建立连接
con = sqlite3.connect('../data/mars_tianchi.db')

# 导入歌曲艺人表
songs = pd.read_csv('../data/p2_mars_tianchi_songs.csv',
                    names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'Language', 'Gender'])
songs.to_sql('songs', con, index=False)

# 导入用户行为表
user_actions = pd.read_csv('../data/p2_mars_tianchi_user_actions.csv',
                    names=['user_id', 'song_id', 'gmt_create', 'action_type', 'Ds'])
user_actions.to_sql('user_actions', con, index=False)
