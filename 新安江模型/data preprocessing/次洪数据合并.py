import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

base_path = 'C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/模型构建/'
files = os.listdir(base_path)

new_df = pd.DataFrame()
for ele in files:
    data = pd.read_csv(base_path + ele)

    new_df = pd.concat([new_df, data], ignore_index=True)

new_df.to_csv('C:/aaUserProgram/ArcGIS10.8/Project/shuikexue/result.csv', index=False)