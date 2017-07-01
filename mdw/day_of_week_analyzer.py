import matplotlib.pyplot as plt

from hdc import query


# 显示每个艺人周末的影响:全部序列，未求平均值
def weekday_trend_of_artist(artist_id):
    q.querySingleArtists(artist_id)
    plt.cla()
    plt.xlim(0,len(q.deltaDay))
    plt.xlabel('days')
    plt.ylabel('playCount')
    plt.scatter(q.deltaDay,q.playCount,s = q.area,c = q.color,alpha = 0.5)
    plt.plot(q.deltaDay,q.playCount)
    plt.savefig('../data/day_of_week/%s.png' % artist_id)


# 显示每个艺人周末的影响:求平均值
def avg_weekday_trend_of_artist(artist_id):
    q.querySingleArtists(artist_id)
    x = [1,2,3,4,5,6,7]
    y = [0,0,0,0,0,0,0]
    for i in range(len(q.deltaDay)):
        index = q.dayOfWeek[i]
        num = q.playCount[i]
        y[index] += num;

    plt.cla()
    plt.xlabel('days')
    plt.ylabel('sum of playCount')
    plt.plot(x,y)
    plt.savefig('../data/sum_day_of_week/%s.png' % artist_id)


# 显示每个艺人周末的影响:求平均值
def each_weekday_trend_of_artist(artist_id):
    q.querySingleArtists(artist_id)
    #week_day = [1,2,3,4,5,6,7]
    styles = ['r-','g-','b-','c-','m-','y-','k-']
    # 0 1 2 3 4 5 6
    ys = [[],[],[],[],[],[],[]]
    for i in range(len(q.deltaDay)):
        if q.deltaDay == 0 :
            continue;
        index = q.dayOfWeek[i] # 0-6
        num = q.playCount[i]
        ys[index].append(num);

    plt.cla()
    for i in range(len(ys)):
        y = ys[i];
        x = range(len(y))
        plt.xlabel('weeks')
        plt.ylabel('sum of playCount')
        plt.plot(x,y,styles[i])
    plt.savefig('../data/each_day_of_week/%s.png' % artist_id)

q = query.Query('../data/mars_tianchi.db')
q.queryAllArtists()
for artist_id in q.allArtists:
    each_weekday_trend_of_artist(artist_id)
