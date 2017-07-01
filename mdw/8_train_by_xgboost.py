# 根据已有的特征预测未来的播放量
# 预测的播放量会存在特定的表中，也会存放在数据库的result表中
# 用于平时训练
from basic import evaluate, merge,xgboost_model
import  numpy as np
import warnings

warnings.filterwarnings('ignore')

'''
    自动化测试部分
'''
# warnings.filterwarnings('ignore')
# max = 0
# best_num_round = 0
# for num_round in range(3,10):
#     # 0-137 训练 138-153 测试 154-183 预测
#     # best round 6 bestScore 0.7024
#     predict(num_round, 0,153,147,153, 153,183,) # predict(i, 183, 244)
#     score = evaluate.evaluateAllArtist()
#     print("%d round score is %.4f" % (num_round, score))
#     if score > max:
#         max = score
#         best_num_round = num_round

# 3 31     0 -31
# 4 30 61  31-61
# 5 31 92  61-92
# 6 30 122 92-122
# 7 31 153 122-153
# 8 31 184  8.30 没有
# 9 30 214 184-214
# 10 30 244 214-244
max = 0
# data_ranges = [
#     [14, 122, 122, 183],  # 3-7
#     [31, 122, 122, 183],  # 4-7
#     [61, 122, 122, 183],  # 5-7
#     [92, 122, 122, 183],  # 6-7
#     [106, 122, 122, 183]  # 7.5
# ]

data_ranges = [
    ["20150301", "20150731", "20150801", "20150830"]   # 3-7
    # [31, 153, 153, 183],  # 4-7
    # [61, 153, 153, 183],  # 5-7
    # [92, 153, 153, 183],  # 6-7
    # [106, 153, 153, 183]  # 7.5
]



# 融合统计
all_in_file_path = []
weight = []
merge_out_file_path = "../data/predict_merge.csv"

best_data_range = []
for data_range in data_ranges:

    trainBegin = data_range[0]
    trainEnd = data_range[1]
    predictBegin = data_range[2]
    predictEnd = data_range[3]

    out_file_path = '../data/predict_%s_%s_%s_%s.csv' % (trainBegin, trainEnd, predictBegin, predictEnd)
    all_in_file_path.append(out_file_path)

    xgboost_model.predict(trainBegin, trainEnd, predictBegin, predictEnd, out_file_path)

    score = evaluate.evaluateAllArtist(out_file_path)
    weight.append(1)
    print(data_range)
    print("score is %.4f" % score)
    if score > max:
        max = score
        best_data_range = data_range

# 按分数来
weight = np.array(weight)/sum(weight)
print(weight)

print(best_data_range)
print("bestScore %.4f" % max)

merge.merge(all_in_file_path, weight, merge_out_file_path)
score = evaluate.evaluateAllArtist(merge_out_file_path)
print("merge score is %.4f" % score)

# predict(6, 0,177,177,183, 184,244) # predict(i, 183, 244)
