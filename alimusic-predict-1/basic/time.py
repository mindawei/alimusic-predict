import datetime


# 字符串列表转换为日期类型列表
def str_to_date(strings):
    return [datetime.datetime.strptime(s, '%Y%m%d') for s in strings]


# 获得指定范围的日期 闭区间
def get_date_range(day_begin, day_end):
    day_time = datetime.datetime.strptime(day_begin, '%Y%m%d')
    dates = []
    while day_time <= datetime.datetime.strptime(day_end, '%Y%m%d'):
        dates.append(day_time)
        day_time += datetime.timedelta(days=1)
    return dates


