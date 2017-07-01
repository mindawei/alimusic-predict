# 使用本文件首先需要添加一个statistics表，statistics表的作用是统计每个艺人每天的播放量，下载量、收藏量、以及听众数
#CREATE TABLE `songs` (
#	`song_id`	TEXT,
#	`artist_id`	TEXT,
#	`publish_time`	INTEGER,
#	`song_init_plays`	INTEGER,
#	`Language`	INTEGER,
#	`Gender`	INTEGER,
#	`totalPlay`	INTEGER
#);

from datetime import date,timedelta
import sqlite3
import numpy as np
from sklearn import  linear_model
class Query:
	dates = []					  #日期
	deltaDay = []                 #从20150301起第多少天
	conn = None					  #数据库连接
	playCount = []                #每天播放量
	dayOfWeek = []				  #一周中的第几天与deltaDay一一对应
	fans = []					  #艺人每天的听众数目
	download = []				  #艺人每天的下载量
	collect = []				  #艺人每天的收藏量
	def __init__(self,path=r'E:\BigData\Data\test.db'):
		self.conn = sqlite3.connect(path)
	def queryAllArtists(self):
		allArtists = []
		sql = r"select distinct artist_id from statistics"
		result = self.conn.execute(sql).fetchall()
		for item in result:
			allArtists.append(item[0])
		return allArtists

	def smooth(self,target,winSize = 3):
		afterSmooth = []
		for i in range(winSize):
			afterSmooth.append(int(round(sum(target[0:i+1])/(i+1))))
		for i in range(winSize, len(target)):
			afterSmooth.append(int(round(sum(target[i - winSize:i]) / winSize)))
		return afterSmooth



	def querySingleArtists(self,name):
		sql = "select playCount,Ds from statistics where artist_id = '%s' order by Ds" % name
		result = self.conn.execute(sql).fetchall()
		self.deltaDay.clear()
		self.playCount.clear()
		self.dayOfWeek.clear()
		# self.fans.clear()
		# self.download.clear()
		# self.collect.clear()
		self.dates.clear()
		start = date(2015,3,1)  #开始的天数作为第零天
		for item in result:
			self.playCount.append(int(item[0]))
			tt = item[1]                                 #对应与日期项，便与下一行书写
			dt = date(int(tt[0:4]),int(tt[4:6]),int(tt[6:8]))
			self.dates.append(dt)
			self.deltaDay.append((dt-start).days)
			weekday = int(dt.weekday())
			self.dayOfWeek.append(weekday)
	'''
	得到target的月度走势，作为下一个月的预测参考
	例如艺人每天播放次数的月度走势
	'''

	def getTargetTrend(self, target, end):
		trend = np.zeros((end, 1))
		playCount = target
		deltaDay = np.array(range(end), dtype=np.int16)
		deltaDay.shape = (end, 1)
		regr1 = linear_model.LinearRegression()
		regr1.fit(deltaDay[0:31], playCount[0:31])
		trend[31:61] = regr1.coef_
		regr2 = linear_model.LinearRegression()
		regr2.fit(deltaDay[31:61], playCount[31:61])
		trend[61:92] = regr2.coef_
		regr3 = linear_model.LinearRegression()
		regr3.fit(deltaDay[61:92], playCount[61:92])
		trend[92:122] = regr3.coef_
		if end > 200:
			regr4 = linear_model.LinearRegression()
			regr4.fit(deltaDay[92:122], playCount[92:122])
			trend[122:153] = regr4.coef_
			regr5 = linear_model.LinearRegression()
			regr5.fit(deltaDay[122:153], playCount[122:153])
			trend[153:183] = regr5.coef_
			regr6 = linear_model.LinearRegression()
			regr6.fit(deltaDay[153:183], playCount[153:183])
			trend[183:244] = regr6.coef_
		else:
			regr7 = linear_model.LinearRegression()
			regr7.fit(deltaDay[92:122], playCount[92:122])
			trend[122:183] = regr7.coef_
		return trend

	def daysToPeek(self):
		lastDays = np.zeros(183,dtype=np.int32)
		for i in range(len(lastDays)):
			lastDays[i] = -1
		i = 0
		temp = -1
		flag = False
		while i<182:
			if(self.playCount[i+1]-self.playCount[i])<500:
				if(flag):
					lastDays[i] = temp
					temp = temp + 1
				i = i + 1
				continue;
			else:
				while self.playCount[i]<self.playCount[i+1]:
					lastDays[i] = 0
					i = i + 1
				lastDays[i] = 0
			i = i + 1
			temp = 1
			flag = True
		if flag:
			lastDays[182] = temp
		lastDays.shape = (183,1)
		return lastDays
	def queryAllSong(self,name):
		sql = "select song_id from songs where artist_id = '%s'" % name
		result = self.conn.execute(sql).fetchall()
		allSong = []
		for item in result:
			allSong.append(item)
		return allSong
	def getTargetLastMonthSum(self,target):
		t = np.array(target,dtype=np.int32)
		t[0:31] = -1
		t[31:61] = sum(target[0:31])
		t[61:92] = sum(target[31:61])
		t[92:122] = sum(target[61:92])
		t[122:183] = sum(target[92:122])
		return t