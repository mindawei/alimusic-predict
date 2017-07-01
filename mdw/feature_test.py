# 根据已有的特征预测未来的播放量
# 预测的播放量会存在特定的表中，也会存放在数据库的result表中
# 用于平时训练
from basic import evaluate,xgboost_for_fature_test
import warnings

warnings.filterwarnings('ignore')

for feature_index in range(26):
    print("feature_index" , feature_index)
    trainBegin = 14
    trainEnd = 153
    predictBegin = 153
    predictEnd = 183

    out_file_path = '../data/predict_%d_%d_%d_%d.csv' % (trainBegin, trainEnd, predictBegin, predictEnd)
    xgboost_for_fature_test.predict(trainBegin, trainEnd, predictBegin, predictEnd, out_file_path,feature_index)
    score = evaluate.evaluateAllArtist(out_file_path)
    print("score is %.4f" % score)



