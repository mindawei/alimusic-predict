import datetime


# 把预测结果分别存入文件和数据库result表中
# result指代预测的结果，x指所预测日期，即离2015-03-01的天数，name指代艺人名字
def writeResult(fileDescriptor, result, x, name):
    beginDay = datetime.date(2015, 3, 1)
    for i in range(len(result)):
        delta = datetime.timedelta(days=(x[i]))
        t1 = beginDay + delta
        year = t1.year
        month = t1.month
        day = t1.day
        currentDay = '%d%02d%02d' % (year, month, day)
        fileDescriptor.write("%s,%d," % (name, result[i]))
        fileDescriptor.write("%s\n" % currentDay)
