# alimusic-predict
[阿里音乐流行趋势预测大赛](https://tianchi.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.4c5fd3bez7WUi&raceId=231531)比赛要求参赛者利用阿里音乐用户前 6 个月的播放数据预测未来 2 个月的播放情况。本人在比赛中负责数据的清洗和平滑、规则的编写。初赛排名第216名（前500名进入复赛），复赛排名第 12（共 5476 队），获得极客奖。

## alimusic-predict-1<br>
这是初赛代码（Python）,解题思路：进行数据分析，清理异常值，构造数据特征，调用一些模型（GBDT,随机深林）进行预测。

## alimusic-predict-2<br>
这是复赛代码（Java）,解题思路：由于数据质量不高，均值预测效果较好。趋势的反映可以制定相关规则实现。

## 总结
* 基本概念一定要清晰：其他选手会将一些输入输出公式化；宏观问题不适合使用微观因素，因为缺少部分它们之间的相互关系。
* 分类效率不高：我们使用一些规则、人工进行判断 <-> 对方 GBDT 进行分类
* 预测模型：我们是直线 <-> 对方是V字型
* 公式观察：没有观察 <-> 对方分析，公式来看偏小值进行预测比偏大值预测分数高
* 提交问题：直观分析 <-> 记录每次提交的详细信息，并分析分数变动的原因；为了一些未知的部分，可以设定值去试
* 其他：对手模型融合增加鲁棒性；分类部分GBDT基本默认参数；数据清洗；充分运用均值、中位数等
