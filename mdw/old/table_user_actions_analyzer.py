import sqlite3

con = sqlite3.connect('data/mars_tianchi.db')

# 行为数
#select_str = "SELECT COUNT(*) from user_actions ";
#rows = con.execute(select_str).fetchall()
#print("行为记录数：")
#print(rows)

# 用户数
#select_str = "SELECT COUNT(DISTINCT(user_id)) FROM user_actions"
#rows = con.execute(select_str).fetchall()
#print("涉及用户数：")
#print(rows)

# 多少首歌
select_str = "SELECT COUNT(DISTINCT(song_id)) FROM user_actions"

#  播放，下载，收藏的比例
select_str = "SELECT action_type,COUNT(*) FROM user_actions GROUP BY action_type"
rows = con.execute(select_str).fetchall()
print("播放，下载，收藏的比例：")
print(rows)