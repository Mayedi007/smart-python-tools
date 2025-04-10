#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 9 12:00:00 2025

@author: Mohamed Ayadi
"""

import os

def split_csv(file_path, num_splits):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_splits

    with open(file_path, 'r', encoding="utf_8_sig") as file:
        # Read CSV header
        header = file.readline()

        for i in range(num_splits):
            output_file_path = f"{file_path.rsplit('.', 1)[0]}_part{i+1}.csv"
            with open(output_file_path, 'w', encoding="utf_8_sig") as output_file:
                # Write header to output file
                output_file.write(header)

                # Split file content evenly by byte size
                bytes_written = 0
                while bytes_written < chunk_size:
                    line = file.readline()
                    if not line:  # End of file
                        break
                    output_file.write(line)
                    bytes_written += len(line.encode("utf_8_sig"))

# Example usage
file_path = 'Forwardcitation.csv'  # Update this path to match your file
split_csv(file_path, 3)
