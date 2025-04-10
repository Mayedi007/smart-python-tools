#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 9 12:00:00 2025

@author: Mohamed Ayadi
"""

import os
import zipfile
import pandas as pd

def extract_all_zip_files_in_order(directory, sort_by='time'):
    # Get all .zip files in the directory
    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]

    # Sort zip files by time or name
    if sort_by == 'time':
        zip_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    elif sort_by == 'name':
        zip_files.sort()
    else:
        raise ValueError("sort_by must be 'time' or 'name'")

    # Prepare a DataFrame to combine all CSVs
    combined_df = pd.DataFrame()

    for zip_file in zip_files:
        zip_path = os.path.join(directory, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(directory)
            for file_name in zip_ref.namelist():
                file_path = os.path.join(directory, file_name)
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_path, sep=';')
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                    os.remove(file_path)  # Clean up extracted file

    return combined_df

# === Example usage ===

# Update this to your actual folder path
folder_path = 'data/original-files'  # example relative path
folder_name = 'back_tls212_citation'
directory = os.path.join(folder_path, folder_name)

combined_df = extract_all_zip_files_in_order(directory, sort_by='time')

# Remove duplicates and save the result
combined_df = combined_df.drop_duplicates()
output_path = os.path.join(folder_path, f'{folder_name}_combined_file.csv')
combined_df.to_csv(output_path, index=False)
