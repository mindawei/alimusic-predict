import matplotlib.pyplot as plt
import numpy as np

from hdc import query as query

q = query.Query('../data/mars_tianchi.db')
q.queryAllArtists()
rng = np.random.RandomState(1)
pathDir = '../data/artists/'
for i in q.allArtists:
    q.querySingleArtists(i)
    plt.cla()
    plt.xlim(q.deltaDay[0], q.deltaDay[len(q.deltaDay) - 1])
    plt.title(i)
    plt.xlabel("deltaDay")
    plt.ylabel("playCount")
    plt.scatter(q.deltaDay, q.playCount)
    plt.plot(q.deltaDay, q.playCount, 'b-')
    name = pathDir + str(i)
    name = name + ".png"
    plt.savefig(name)
print("ok")
