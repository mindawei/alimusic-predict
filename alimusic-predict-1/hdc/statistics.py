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
def selectArtistsAllSong(name):
    sql = r"select Ds,count(gmt_create) as playCount,count(distinct user_id) as fans from user_actions where song_id in (select song_id from"
    sql = sql + r" songs where artist_id = '"
    sql = sql + str(name)
    sql = sql + r"') group by Ds"
    result = conn.execute(sql).fetchall()
    dateti =[]
    playCount = []
    fans = []
    for i in result:
        dateti.append(i[0])
        playCount.append(i[1])
        fans.append(i[2])
    sql = r"select Ds,count(action_type) from user_actions where song_id in (select song_id from songs where artist_id = '"
    sql = sql + str(name)
    sql = sql + r"') and action_type = 2 group by Ds"
    tempdownload = []
    tempdate = []
    result = conn.execute(sql).fetchall()
    for i in result:
        tempdate.append(i[0])
        tempdownload.append(i[1])
    j = 0
    download = []
    for i in range(len(dateti)):
        if(j<len(tempdownload)) and (dateti[i] == tempdate[j]):
            download.append(tempdownload[j])
            j = j +1
        else:
            download.append(0)
    sql = r"select Ds,count(action_type) from user_actions where song_id in (select song_id from songs where artist_id = '"
    sql = sql + str(name)
    sql = sql + r"') and action_type = 3 group by Ds"
    tempcollect = []
    tempdate1 = []
    result = conn.execute(sql).fetchall()
    for i in result:
        tempdate1.append(i[0])
        tempcollect.append(i[1])
    j = 0
    collect = []
    for i in range(len(dateti)):
        if (j<len(tempdate1)) and (dateti[i] == tempdate1[j]):
            collect.append(tempcollect[j])
            j = j + 1
        else:
            collect.append(0)
    return dateti,playCount,fans,download,collect
artists = selectAllArtists()
for name in artists:
    playDate,playCount,fans,download,collect = selectArtistsAllSong(name)
    sql = r"insert into statistics_after_filter values(?,?,?,?,?,?)"
    for i in range(len(playDate)):
        value = [name,playCount[i],fans[i],download[i],collect[i],playDate[i]]
        conn.execute(sql,value)
    conn.commit()
    print(name)
conn.close()