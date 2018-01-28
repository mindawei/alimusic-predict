import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


con = sqlite3.connect('../data/mars_tianchi.db')


select_str = "SELECT DISTINCT(artist_id) FROM songs"
artists = np.array(con.execute(select_str).fetchall())[:, 0]

# 对每个艺人进行处理
for artist_id in artists:
        print(artist_id)
        # 确认表
        check_str = "DROP TABLE IF EXISTS statistics_%s" % (artist_id)
        con.execute(check_str)
        check_str = "DROP TABLE IF EXISTS user_statistics_actions_%s" % artist_id
        con.execute(check_str)
print('done')

