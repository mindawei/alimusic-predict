import query as query
import numpy as np
import math
from sklearn import preprocessing
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor

pi = math.pi
t1 = 2 * pi * 90
t2 = 2 * pi / 30
t3 = 2 * pi / 7
q = query.Query('../data/mars_tianchi.db')
q.queryAllArtists()
rng = np.random.RandomState(1)
mses = []
for i in q.allArtists:
    q.querySingleArtists(i)
    deltaDay = np.array(q.deltaDay,dtype=np.float64)
    deltaDay.shape = (len(q.deltaDay), 1)
    playCount = np.array(q.playCount)
    playCount.shape = (len(q.playCount), 1)
    dayOfWeek = np.array(q.dayOfWeek,dtype=np.float64)
    dayOfWeek.shape = (len(q.dayOfWeek), 1)
    #feature = np.column_stack((deltaDay, dayOfWeek, np.sin(t1 * deltaDay), np.cos(t1 * deltaDay)))
    #feature = np.column_stack((deltaDay))
    feature = deltaDay
    train_feature = feature[0:150:, ]
    train_Y = playCount[0:150]
    test_feature = feature[150:len(feature):, ]
    test_Y = playCount[150:]
    scaler = preprocessing.StandardScaler().fit(train_feature)
    scaler_X_train = scaler.transform(train_feature)
    scaler_X_test = scaler.transform(test_feature)
    #regr_1 = DecisionTreeRegressor(max_depth=4)
    #regr_2 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4), n_estimators=500, random_state=rng)
    #regr_1.fit(scaler_X_train, train_Y.ravel())
    #regr_2.fit(scaler_X_train, train_Y.ravel())
    params = {'n_estimators': 400, 'max_depth': None, 'min_samples_split': 1,
     'learning_rate': 0.01, 'loss': 'ls'}
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(scaler_X_train,train_Y.ravel())
    #mse = mean_squared_error(test_Y, regr_2.predict(scaler_X_test))
    mse = mean_squared_error(test_Y,clf.predict(scaler_X_test))
    print("%s  MSE: %.4f" % (i,mse))
    mses.append(mse)
    plt.cla()
    plt.title(i)
    plt.xlim(0, len(deltaDay))
    plt.plot(deltaDay, playCount, 'b-')
    plt.scatter(deltaDay, playCount)
    # plt.plot(deltaDay[0:150],clf.predict(scaler_X_train),'r-')
    # plt.plot(deltaDay[150:],clf.predict(scaler_X_test),'k-')
    plt.plot(deltaDay[0:150], clf.predict(scaler_X_train), 'r-')
    plt.plot(deltaDay[150:], clf.predict(scaler_X_test), 'k-')
    plt.savefig('../data/period/only_deltaDay/%s_mse(%.4f).png' % (i,mse))
avg = sum(mses)/len(mses)
print("avg MSE: %.4f" % avg)