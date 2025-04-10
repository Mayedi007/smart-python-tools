#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 9 12:00:00 2025

@author: Mohamed Ayadi
"""

import requests
from bs4 import BeautifulSoup

# Custom headers to simulate a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
}

def fetch_exam_info(url):
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    soup_str = str(soup)

    # Save the entire HTML content (optional)
    with open('exam_raw.html', 'w', encoding='utf-8') as file:
        file.write(soup_str)

    # Extract metadata
    examtype = soup.find('a', class_='discussion-link').text.strip()

    question_info = soup.find('div', class_='question-discussion-header').get_text(separator=' ').strip()
    question_no = question_info.split('Question #: ')[1].split(' ')[0]
    topic_no = question_info.split('Topic #: ')[1].split(' ')[0]

    description = soup.find('div', class_='question-body').p.get_text(separator=' ').strip()

    # Extract answer options
    options_elements = soup.find_all('li', class_='multi-choice-item')
    options = '\n'.join([opt.get_text(separator=' ').strip() for opt in options_elements])

    suggested_answer = soup.find('span', class_='correct-answer').text.strip()
    most_voted_answer = soup.find('div', class_='voted-answers-tally').script.get_text()

    # Extract discussion data
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

    # Output results
    print(f"Exam type: {examtype}")
    print(f"Question #: {question_no}")
    print(f"Topic #: {topic_no}")
    print(f"Description: {description}")
    print(f"Options:\n{options}")
    print(f"Suggested Answer: {suggested_answer}")
    print(f"Most Voted Answer (raw): {most_voted_answer}")
    print("\nDiscussions:")
    for discussion in discussions:
        print(f"{discussion['user']} | {discussion['date']}")
        print(f"Selected Answer: {discussion['selected_answer']}")
        print(f"{discussion['text']}")
        print(f"   👍 {discussion['upvotes']} upvotes\n")

# Example usage
url = 'https://www.examtopics.com/discussions/amazon/view/117053-exam-aws-certified-solutions-architect-associate-saa-c03/'
fetch_exam_info(url)
