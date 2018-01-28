import sqlite3
import numpy as np

conn = sqlite3.connect(r"E:/BigData/Temp/test.db")


def selectAllArtists():
    sql = r"select distinct artist_id from songs"
    result = conn.execute(sql).fetchall()
    artists = []
    for i in result:
        artists.append(i[0])
    return artists


artists = selectAllArtists()


def selectException(name):
    sql = r"select artist_id,playCount,fans,Ds from statistics where artist_id = '"
    sql = sql + str(name)
    sql = sql + r"'"
    result = conn.execute(sql).fetchall()
    artists_id = result[0][0]
    playCount = []
    fans = []
    playDate = []
    for item in result:
        playCount.append(item[1])
        fans.append(item[2])
        playDate.append(item[3])
    average = np.array(playCount) / np.array(fans)
    mean = average.mean()
    tempPlayCount = []
    tempFans = []
    tempDate = []
    for i in range(len(playCount)):
        if (average[i] - mean) > 1:
            tempPlayCount.append(playCount[i])
            tempFans.append(fans[i])
            tempDate.append(playDate[i])
    return tempPlayCount, tempFans, tempDate


def deleteException(artists_id, playCount, fans, date):
    for i in range(len(playCount)):
        sql = r"select user_id,count(gmt_create) as playCount from "
        sql = sql + r"(select * from user_actions where song_id in (select"
        sql = sql + r" song_id from songs where artist_id = '"
        sql = sql + str(artists_id)
        sql = sql + r"') and Ds = '"
        sql = sql + str(date[i])
        sql = sql + r"') group by user_id order by playCount Desc"
        result = conn.execute(sql).fetchall()
        user_id = []
        numberOfPlay = []
        for item in result:
            user_id.append(item[0])
            numberOfPlay.append(item[1])
        for j in range(len(numberOfPlay)):
            if (numberOfPlay[j] < 150) and ((numberOfPlay[j] / playCount[i]) < 0.6):
                break
            if (numberOfPlay[j] >= 150):
                deletesql = r"delete  from user_actions where song_id in (select song_id from songs where artist_id = '"
                deletesql = deletesql + str(artists_id)
                deletesql = deletesql + r"') and Ds = '"
                deletesql = deletesql + str(date[i])
                deletesql = deletesql + r"' and user_id = '"
                deletesql = deletesql + str(user_id[j])
                deletesql = deletesql + r"'"
                conn.execute(deletesql)
                continue
            if (numberOfPlay[j] / playCount[i]) > 0.6 and (fans[i] > 2):
                deletesql = r"delete  from user_actions where song_id in (select song_id from songs where artist_id = '"
                deletesql = deletesql + str(artists_id)
                deletesql = deletesql + r"') and Ds = '"
                deletesql = deletesql + str(date[i])
                deletesql = deletesql + r"' and user_id = '"
                deletesql = deletesql + str(user_id[j])
                deletesql = deletesql + r"'"
                conn.execute(deletesql)
                continue
            conn.commit()


for i in artists:
    # playCount,playFans,playDate = selectException(i)
    # deleteException(i,playCount,playFans,playDate)
    print(i)
