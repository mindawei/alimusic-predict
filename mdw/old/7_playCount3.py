import sqlite3
import numpy as np

# 获得艺人
con = sqlite3.connect('../data/mars_tianchi.db')
select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(con.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
    print(artist_id)
    alert_str = "ALTER TABLE statistics_%s ADD playCount3 INTEGER " % artist_id
    con.execute(alert_str)
    con.commit()
print('done')
