# 根据已有的特征预测未来的播放量
# 预测的播放量会存在特定的表中，也会存放在数据库的result表中
# 用于平时训练
from sklearn import preprocessing
from hdc import query
from basic import evaluate, writer, features, merge,xgboost_model
import numpy as np
import warnings
import xgboost as xgb

warnings.filterwarnings('ignore')


# 3 31     0 -31
# 4 30 61  31-61
# 5 31 92  61-92
# 6 30 122 92-122
# 7 31 153 122-153
# 8 31 184  8.30 没有
# 9 30 214 184-214
# 10 30 244 214-244

max = 0

data_ranges = [
    [14, 183, 184, 244]    # 3-8
    # [31, 183, 184, 244],   # 4-8
    # [61, 183, 184, 244],   # 5-8
    # [92, 183, 184, 244],   # 6-8
    # [122, 183, 184, 244],  # 7-8
    # [153, 183, 184, 244],  # 8-8
    # [167, 183, 184, 244]   # 8.5-8
]

# 融合统计
all_in_file_path = []
weight = []
merge_out_file_path = "../data/predict/mars_tianchi_artist_plays_predict.csv"

for data_range in data_ranges:
    trainBegin = data_range[0]
    trainEnd = data_range[1]
    predictBegin = data_range[2]
    predictEnd = data_range[3]

    out_file_path = '../data/predict_%d_%d_%d_%d.csv' % (trainBegin, trainEnd, predictBegin, predictEnd)
    all_in_file_path.append(out_file_path)
    #weight.append(trainEnd-trainBegin) # 按天数
    weight.append(1) # 按平均

    xgboost_model.predict(trainBegin, trainEnd, predictBegin, predictEnd, out_file_path)
    print(out_file_path)

# 按分数来
weight = np.array(weight)/sum(weight)
print(weight)

merge.merge(all_in_file_path, weight, merge_out_file_path)

# predict(6, 0,177,177,183, 184,244) # predict(i, 183, 244)
