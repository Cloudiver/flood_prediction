import os
import pandas as pd
import numpy as np

base_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/洪水事件/新建文件夹'
save_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/洪水事件插值结果'
files = os.listdir(base_path)

for single_file in files:
    df = pd.read_csv(os.path.join(base_path, single_file))

    df['时间'] = pd.to_datetime(df['时间'])
    df.set_index('时间', inplace=True)

    print("原始 DataFrame:")
    print(df)

    # 确保 DataFrame 按索引排序
    df.sort_index(inplace=True)

    # 创建一个完整的 DateTimeIndex，包括从00:00到23:00的每一个小时
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H')

    # 重新索引 DataFrame 到新的 DateTimeIndex
    df_reindexed = df.reindex(date_range)

    # 插值补充缺失的值
    df_interpolated = df_reindexed.interpolate(method='linear')

    # print(df_interpolated)
    df_interpolated.to_csv(os.path.join(save_path, single_file[:-4] + '-插值结果gai.csv'))
