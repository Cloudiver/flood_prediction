import pandas as pd
import numpy as np

def process_evaporation(file_path, start_time, end_time):
    # 读取数据
    df = pd.read_excel(file_path)

    df.columns = ['year', 'month', 'day', '蒸发量']
    
    # 生成日期时间
    df['日期'] = pd.to_datetime(df[['year', 'month', 'day']])
    
    # 初始化新的DataFrame用于存储结果
    result_list = []

    for index, row in df.iterrows():
        date = row['日期']
        evaporation = row['蒸发量'] / 10  # 除以10
        
        # 小于0.1mm则记为0
        if evaporation < 0.1:
            evaporation = 0

        # 平均分配到24小时
        hourly_evaporation = evaporation / 24
        
        # 生成每小时的数据
        for hour in range(24):
            current_time = date + pd.Timedelta(hours=hour)
            result_list.append({'时间': current_time, '蒸发量': hourly_evaporation})

    # 转换结果列表为 DataFrame
    result_df = pd.DataFrame(result_list)
    
    # 根据提供的起始和结束时间进行截取
    mask = (result_df['时间'] >= start_time) & (result_df['时间'] <= end_time)
    result_df = result_df.loc[mask]
    
    return result_df.round(1)

# 示例文件路径和起始、结束时间
file_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/01流域径流预报初赛试题/附件/蒸发数据/6.xlsx'
start_time = '2012-09-11 04:00:00'
end_time = '2012-09-14 08:00:00'

# 处理蒸发数据
result_df = process_evaporation(file_path, start_time, end_time)

# 保存结果到CSV文件
output_file = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/数据预处理/蒸发/' + start_time.split(' ')[0] + '~' + end_time.split(' ')[0] + '.csv'
result_df.to_csv(output_file, index=False)

print(f"处理完成，结果已保存到: {output_file}")
