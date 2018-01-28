import sqlite3
import numpy as np

# 获得艺人
con = sqlite3.connect('../data/mars_tianchi.db')
select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(con.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
    print(artist_id)
    #alert_str = "ALTER TABLE statistics_%s ADD playCount2 INTEGER " % artist_id
    #con.execute(alert_str)
    update_str = "UPDATE statistics_%s SET playCount2 = playCount " % artist_id
    con.execute(update_str)
    con.commit()
print('done')
