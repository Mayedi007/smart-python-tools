#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:43:07 2024

@author: yuzhen
"""

import os
import zipfile
import pandas as pd

def extract_all_zip_files_in_order(directory, sort_by='time'):
    # 获取所有的ZIP文件列表
    # Get a list of all ZIP files
    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]

    # 按照文件名或时间排序
    # Sort by file name or time
    if sort_by == 'time':
        zip_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    elif sort_by == 'name':
        zip_files.sort()
    else:
        raise ValueError("sort_by must be 'time' or 'name'")

    # 创建一个空的DataFrame用于存放数据
    # Create an empty DataFrame for storing the data
    combined_df = pd.DataFrame()

    for zip_file in zip_files:
        zip_path = os.path.join(directory, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取压缩文件内的所有文件列表
            # Get a list of all files in the zip file
            zip_ref.extractall(directory)
            for file_name in zip_ref.namelist():
                file_path = os.path.join(directory, file_name)
                # 假设所有文件都是CSV文件，可以根据实际情况进行修改
                # Assuming all files are CSV files, which can be modified as appropriate
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_path, sep=';')
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                    # 删除解压后的文件
                    # Delete unzipped files
                    os.remove(file_path)

    return combined_df


# 替换为你的文件夹路径
# Replace it with your folder path
folder_path = '/Users/yuzhen/Documents/original file'

folder_name = 'back_tls212_citation'
directory = folder_path + '/' + folder_name

combined_df = extract_all_zip_files_in_order(directory, sort_by='time')

# 保存最终的合并结果
# Save the final merged result
combined_df = combined_df.drop_duplicates()

combined_df.to_csv(folder_path + '/' + folder_name + '_combined_file.csv', index=False)
