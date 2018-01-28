import datetime
import sqlite3

# 建立连接
conn = sqlite3.connect('../data/mars_tianchi.db')

check_str = "DROP TABLE IF EXISTS feature_time"
conn.execute(check_str)

create_str = "create table feature_time (Ds TEXT, day_offset INTEGER ,month_offset INTEGER ,week_offset INTEGER,day_of_week INTEGER,is_relax INTEGER )"
conn.execute(create_str)

day_start = datetime.datetime.strptime("20150301", '%Y%m%d')
day_end = datetime.datetime.strptime("20151030", '%Y%m%d')
day_time = day_start;

while day_time <= day_end:

    Ds = day_time.strftime("%Y%m%d")

    # 距离 20150301 第几天 day_offset
    day_offset = (day_time - day_start).days

    # 距离 20150301 第几个月 month_offset
    month_offset = day_time.month - day_start.month

    # 距离 20150302(星期一) 第几周 day_offset
    week_offset = 0
    if day_offset > 0:
        week_offset = (day_offset - 1) / 7

    # 周几
    day_of_week = day_time.weekday()

   # 2 是否休息
    is_relax = 0
    day_of_week = day_time.weekday()
    if 5 <= day_of_week <= 6:
           is_relax = 1
    Ds = day_time.strftime("%Y%m%d")
    if "20150405" <= Ds <= "20150406":
        is_relax = 1
    if "20150501" <= Ds <= "20150503":
        is_relax = 1
    if "20150620" <= Ds <= "20150622":
        is_relax = 1
    if "20150903" <= Ds <= "20150905":
        is_relax = 1
    if "20150926" <= Ds <= "20150928":
        is_relax = 1
    if "20151001" <= Ds <= "20151007":
        is_relax = 1
    # 调休
    if Ds == "20150906":
        is_relax = 0
    if Ds == "20151010":
        is_relax = 0

    insert_str = "insert into feature_time (Ds,day_offset ,month_offset ,week_offset ,day_of_week ,is_relax ) " \
                 "VALUES (?,?,?,?,?,?)"
    item = (Ds, day_offset, month_offset, int(week_offset), day_of_week, is_relax)
    conn.execute(insert_str,item)
    day_time += datetime.timedelta(days=1)
conn.commit()