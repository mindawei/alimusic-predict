# 计算寻找与歌手播放量相关的变量

import numpy as np
from basic import query
from basic import correlation


# 计算相关相似度
def find_correlation(ls_0, name_0, ls_1, name_1):
    arr_0 = np.array(ls_0,dtype='int')
    arr_1 = np.array(ls_1,dtype='int')
    val = correlation.pearsonSimilar(arr_0, arr_1)
    print("%s 与 %s 的皮尔逊相关系数: %.4f" % (name_0, name_1, val))


db_query = query.Query()
artists = db_query.get_all_artists()
play_sum_list = []
song_sum_list = []
song_init_plays_sum_list = []
main_language_list = []
gender_list = []

main_language_dict = {}
gender_dict = {}

for artist_id in artists:
    # 艺人播放总数
    play_sum = db_query.get_play_sum_of_artist(artist_id)
    play_sum_list.append(play_sum)
    # 艺人歌曲总数
    song_sum = db_query.get_song_sum_of_artist(artist_id)
    song_sum_list.append(song_sum)
    # 艺人歌曲初始热度总数
    song_init_plays_sum = db_query.get_song_init_plays_sum_of_artist(artist_id)
    song_init_plays_sum_list.append(song_init_plays_sum)
    # 艺人歌曲的主要语言
    main_language = db_query.get_main_language_of_artist(artist_id)
    main_language_list.append(main_language)
    if main_language in main_language_dict:
        main_language_dict[main_language].append(play_sum)
    else:
        main_language_dict[main_language] = [play_sum]
    # 艺人的性别
    gender = db_query.get_gender_of_artist(artist_id)
    gender_list.append(gender)
    if gender in gender_dict:
        gender_dict[gender].append(play_sum)
    else:
        gender_dict[gender] = [play_sum]

    print('%s %d %d %d %d %d' % (artist_id, play_sum, song_sum,song_init_plays_sum,main_language,gender))

find_correlation(play_sum_list, "艺人播放总数", song_sum_list, "艺人歌曲总数")

find_correlation(play_sum_list, "艺人播放总数", song_init_plays_sum_list, "艺人歌曲初始热度总数")

find_correlation(play_sum_list, "艺人播放总数", main_language_list, "艺人歌曲的主要语言")

find_correlation(play_sum_list, "艺人播放总数", gender_list, "艺人的性别")

print("歌曲语言类型 该语言歌曲平均播放量")
for main_language in main_language_dict:
    print("%s %.0f" % (main_language,sum(main_language_dict[main_language])/len(main_language_dict[main_language])))
print()

print("艺人的性别 该语言歌曲平均播放量")
for gender in gender_dict:
    print("%s %.0f" % (gender,sum(gender_dict[gender])/len(gender_dict[gender])))
print()
