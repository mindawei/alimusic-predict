import numpy as np
import pandas as pd
from collections import Counter

# 读取歌曲csv
songs = pd.read_csv('data/mars_tianchi_songs.csv',
                    names=['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'Language', 'Gender'])

# 显示记录数
items_num = len(songs)
print('歌曲文件记录数: %d' % items_num)

# 检查歌曲是否唯一
songs_counts = Counter(songs['song_id'])
print('歌曲ID是否唯一: %s' % (songs_counts.most_common(1)[0][1] == 1))

# 每位歌手分析
artist_counts = Counter(songs['artist_id'])

# 多少歌手
print("歌手人数：%d" % len(artist_counts))

# 每位歌手多少首歌
print("每位歌手多少首歌:")
print(artist_counts)

# 歌手性别比例情况
print("歌手性别比例情况:")
gender_counts = Counter(songs['Gender'])
print(gender_counts)

# 语言情况
print("歌曲语言情况:")
language_counts = Counter(songs['Language'])
print(language_counts)

# 歌曲初始热度初探
print("每位歌手的平均初始热度:")
mean_song_init_plays = songs.pivot_table(values='song_init_plays', index='artist_id', aggfunc=np.mean)
print(mean_song_init_plays.sort_values())

# 每天的歌曲发布变化
#print("每天的歌曲发布变化:")
#publish_time_counts = Counter(songs['publish_time'])
#print(publish_time_counts)

