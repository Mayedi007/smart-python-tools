#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 16:37:15 2024

@author: yuzhen
"""
import requests
from bs4 import BeautifulSoup

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,uk;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',  # Do Not Track 请求头，表示不愿被追踪
}

def fetch_exam_info(url):
    response = requests.get(url, headers=headers)
    print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    soup_str= str(soup)
    # 指定文件路径
    file_path = '/Users/yuzhen/Documents/new.txt'
    
    # 打开文件，如果文件不存在则创建新文件
    with open(file_path, 'w') as file:  # 'w' 表示写入模式，会覆盖已有文件内容
        # 写入字符串到文件
        file.write(soup_str)
    
    # 提取examtype
    examtype = soup.find('a', class_='discussion-link').text.strip()

    # 提取QuestionNo.和Topic
    question_info = soup.find('div', class_='question-discussion-header').get_text(separator=' ').strip()
    question_no = question_info.split('Question #: ')[1].split(' ')[0]
    topic_no = question_info.split('Topic #: ')[1].split(' ')[0]

    # 提取description
    description = soup.find('div', class_='question-body').p.get_text(separator=' ').strip()

    # 提取options
    options_elements = soup.find_all('li', class_='multi-choice-item')
    options = '\n'.join([opt.get_text(separator=' ').strip() for opt in options_elements])

    # 提取SuggestedAnswer
    suggested_answer = soup.find('span', class_='correct-answer').text.strip()

    # 提取MostVotedAnswer
    most_voted_answer = soup.find('div', class_='voted-answers-tally').script.get_text()

    # 提取discussion
    discussion_elements = soup.find_all('div', class_='media comment-container')
    discussions = []
    for comment in discussion_elements:
        user = comment.find('h5', class_='comment-username').text.strip()
        date = comment.find('span', class_='comment-date').text.strip()
        selected_answer = comment.find('div', class_='comment-selected-answers').text.strip().replace('Selected Answer: ', '')
        text = comment.find('div', class_='comment-content').get_text(separator=' ').strip()
        upvotes = comment.find('span', class_='upvote-count').text.strip() if comment.find('span', class_='upvote-count') else '0'
        
        discussions.append({
            'user': user,
            'date': date,
            'selected_answer': selected_answer,
            'text': text,
            'upvotes': upvotes
        })

    # 输出提取的内容
    print(f"examtype: {examtype}")
    print(f"QuestionNo. :{question_no}")
    print(f"Topic:{topic_no}")
    print(f"description:{description}")
    print(f"options:{options}")
    print(f"SuggestedAnswer:{suggested_answer}")
    print(f"MostVotedAnswer:{most_voted_answer}")
    print("discussion：")
    for discussion in discussions:
        print(f" {discussion['user']} {discussion['date']}")
        print(f"Selected Answer: {discussion['selected_answer']}")
        print(f"{discussion['text']}")
        print(f"   upvoted {discussion['upvotes']} times")

# 使用示例
url = 'https://www.examtopics.com/discussions/amazon/view/117053-exam-aws-certified-solutions-architect-associate-saa-c03/'
fetch_exam_info(url)
