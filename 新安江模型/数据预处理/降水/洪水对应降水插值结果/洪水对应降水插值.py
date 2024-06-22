import pandas as pd
import os

base_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/降水/洪水对应降水/2012091104'
save_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/降水/洪水对应降水插值结果/'

def process_file(file_path):
    # 读取数据
    df = pd.read_csv(file_path, parse_dates=['时间'])
    print(file_path)
    
    # 初始化新的DataFrame用于存储结果
    result_list = []
    
    for index, row in df.iterrows():
        time = row['时间']
        rain = row['降雨量']
        duration = row['时段']
        
        # 判断时段是否包含小时和分钟
        if duration >= 1 and duration % 1 != 0:
            hours = int(duration)
            minutes = int((duration - hours) * 100)
            total_minutes = hours * 60 + minutes
        elif duration % 1 == 0:
            total_minutes = int(duration) * 60
        else:
            total_minutes = int(duration * 100)
        
        start_time = time - pd.Timedelta(minutes=total_minutes-1)
        end_time = time

        # 每分钟的降水量
        minute_rain = rain / total_minutes

        # 分配分钟降水量到相应的整点时刻
        for i in range(total_minutes):
            current_time = start_time + pd.Timedelta(minutes=i)
            rounded_time = current_time.ceil('H')
            result_list.append({'时间': rounded_time, '降雨量': minute_rain})

    # 转换结果列表为 DataFrame
    result_df = pd.DataFrame(result_list)

    # 合并同一小时的降水量
    result_df = result_df.groupby('时间')['降雨量'].sum().reset_index()
    
    return result_df

# 获取所有文件路径并排序
file_paths = [str(base_path + '/' + ele) for ele in os.listdir(base_path)]
# file_paths = sorted(glob.glob(base_path + '/*.csv'))

# 初始化一个空的列表来存储所有文件的处理结果
all_results = []

# 处理每个文件
for file_path in file_paths:
    result_df = process_file(file_path)
    all_results.append((file_path, result_df))

# 获取所有文件的起止时间
start_times = [df['时间'].min() for _, df in all_results]
end_times = [df['时间'].max() for _, df in all_results]

global_start_time = min(start_times)
global_end_time = max(end_times)

# 生成全局时间范围内的所有整点时间
all_times = pd.date_range(global_start_time, global_end_time, freq='H')
all_times_df = pd.DataFrame(all_times, columns=['时间'])

# 合并所有处理结果到一个DataFrame中
merged_df = all_times_df.copy()

for file_path, result_df in all_results:
    # 使用文件名作为列名
    file_name = file_path.split('/')[-1][:-4]
    merged_df = pd.merge(merged_df, result_df, on='时间', how='left').fillna(0)
    merged_df.rename(columns={'降雨量': file_name}, inplace=True)

merged_df.to_csv(save_path + base_path.split('/')[-1] + '.csv')

print('ok')

