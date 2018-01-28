import sqlite3
from datetime import datetime

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')
day_start = datetime.strptime("20150301", '%Y%m%d')
day_end = datetime.strptime("20151030", '%Y%m%d')


# 添加列
def add_column(column_name, column_type):
    add_sql = "ALTER TABLE feature_time ADD %s %s " % (column_name, column_type)
    conn.execute(add_sql)


# 3 时间特征开始 --------------------------------------------------------

# 距离 20150301 第几天 day_offset
def update_day_offset(artist_id, Ds):
    day_offset = (datetime.strptime(Ds, '%Y%m%d') - day_start).days
    update_str = "UPDATE feature_time SET day_offset=%d  WHERE artist_id='%s' AND Ds='%s'" % (day_offset, artist_id, Ds)
    conn.execute(update_str)


# 距离 20150301 第几个月 day_offset
def update_month_offset(artist_id, Ds):
    month_offset = datetime.strptime(Ds, '%Y%m%d').month - day_start.month
    update_str = "UPDATE feature_time SET month_offset=%d  WHERE artist_id='%s' AND Ds='%s'" % (month_offset, artist_id, Ds)
    conn.execute(update_str)


# 距离 20150302(星期一) 第几周 day_offset
def update_week_offset(artist_id, Ds):
    day_offset = (datetime.strptime(Ds, '%Y%m%d') - day_start).days
    week_offset = 0
    if day_offset > 0:
        week_offset = (day_offset - 1) / 7
    update_str = "UPDATE feature_time SET week_offset=%d  WHERE artist_id='%s' AND Ds='%s'" % (week_offset, artist_id, Ds)
    conn.execute(update_str)


# 周几
def update_day_of_week(artist_id, Ds):
    day_of_week = datetime.strptime(Ds, '%Y%m%d').weekday()
    update_str = "UPDATE feature_time SET day_of_week=%d  WHERE artist_id='%s' AND Ds='%s'" % (day_of_week, artist_id, Ds)
    conn.execute(update_str)


# 是否节假日
def update_is_festival(artist_id, Ds):
    is_festival = 0
    if "20150501" <= Ds <= "20150503":
        is_festival = 1
    if "20150620" <= Ds <= "20150622":
        is_festival = 1
    if "20150926" <= Ds <= "20150928":
        is_festival = 1
    if "20151001" <= Ds <= "20151007":
        is_festival = 1
    update_str = "UPDATE feature_time SET is_festival=%d  WHERE artist_id='%s' AND Ds='%s'" % (is_festival, artist_id, Ds)
    conn.execute(update_str)


# 3 时间特征结束 --------------------------------------------------------



add_column("day_offset", "INTEGER")
add_column("month_offset", "INTEGER")
add_column("week_offset", "INTEGER")
add_column("day_of_week", "INTEGER")
add_column("is_festival", "INTEGER")


for item in conn.execute("SELECT artist_id,Ds FROM statistics").fetchall():
    artist_id = item[0]
    Ds = item[1]
    # update_day_offset(artist_id,Ds)
    # update_month_offset(artist_id,Ds)
    # update_week_offset(artist_id,Ds)
    # update_day_of_week(artist_id,Ds)
    # update_is_festival(artist_id, Ds)
    update_gender(artist_id, Ds)

conn.commit()
