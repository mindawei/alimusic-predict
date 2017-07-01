import pandas as pd


# 根据输入csv融合输出csv
def merge(all_in_file_path=[], weight=[], merge_out_file_path="../data/predict_merger.csv"):
    predict_data = None
    for i in range(len(all_in_file_path)):
        in_file_path = all_in_file_path[i]
        predict = pd.read_csv(in_file_path, names=['artist_id', 'playCount', 'Ds'])
        if predict_data is None:
            predict_data = predict
            predict_data['playCount'] = predict['playCount'] * weight[i]
        else:
            predict_data['playCount'] += predict['playCount'] * weight[i]
    # 取整数
    predict_data['playCount'] = pd.Series(data=predict_data['playCount'], dtype='int32')
    # 输出
    predict_data.to_csv(merge_out_file_path, header=False, index=False)
