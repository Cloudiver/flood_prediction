import pandas as pd
import os

base_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/降水/所需数据/'

def process_precipitation(file_path, start_time, end_time):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 检查是否有时间列
    if '时间' not in df.columns:
        raise ValueError(f"文件 {file_path} 中缺少 '时间' 列")
    
    # 将时间列转换为datetime格式
    df['时间'] = pd.to_datetime(df['时间'])
    
    # 计算最早和最晚时间范围
    earliest_time = start_time - pd.Timedelta(hours=24)
    latest_time = end_time + pd.Timedelta(hours=24)
    
    # 筛选数据
    mask = (df['时间'] >= earliest_time) & (df['时间'] <= latest_time)
    filtered_df = df.loc[mask]
    
    return filtered_df

def process_multiple_files(file_paths, start_time, end_time, output_file):
    result_df = pd.DataFrame()
    
    for file_path in file_paths:
        filtered_df = process_precipitation(file_path, start_time, end_time)
        filtered_df.columns = ['时间', '降雨量', '时段']

        filtered_df.to_csv(output_file + file_path.split('/')[-1][:-5] + '.csv', index=False)

# 示例文件路径和起始、结束时间

start_time = pd.to_datetime('2012-09-11 04:00:00')
end_time = pd.to_datetime('2012-09-14 08:00:00')

file_paths = [str(base_path + '/' + ele) for ele in os.listdir(base_path)]

# # 输出文件路径
output_file = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/降水/洪水对应降水/2012091104/'

# 处理多个文件
process_multiple_files(file_paths, start_time, end_time, output_file)

print(f"处理完成，结果已保存到: {output_file}")
