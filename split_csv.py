#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:29:00 2024

@author: yuzhen
"""

import os

def split_csv(file_path, num_splits):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_splits

    with open(file_path, 'r', encoding="utf_8_sig") as file:
        # 读取CSV表头
        # Read CSV headers
        header = file.readline()

        for i in range(num_splits):
            output_file_path = f"{file_path.rsplit('.', 1)[0]}_part{i+1}.csv"
            with open(output_file_path, 'w', encoding="utf_8_sig") as output_file:
                # 写入CSV表头
                # Write to CSV header
                output_file.write(header)

                # 确保每个文件的大小尽可能接近均等
                # Ensure that each file is as close to equal in size as possible
                bytes_written = 0
                while bytes_written < chunk_size:
                    line = file.readline()
                    if not line:  # EOF
                        break
                    output_file.write(line)
                    bytes_written += len(line.encode("utf_8_sig"))

file_path = '/Users/yuzhen/Documents/Forwardcitation.csv'

split_csv(file_path, 3)
