#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import datetime
import argparse

def scrape_forum(base_url, page_start, page_end, topic_selector, reply_selector, driver_path, output_file, delay=10):
    topics_names = []
    questions_content = []
    question_img = []
    replies_content = []
    replies_order = []
    image1 = []
    video_link1 = []
    topic_urls = []

    print(f'Scraping started at {datetime.datetime.now()}')

    # Configure WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in background
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    for page in range(page_start, page_end + 1):
        try:
            url = f'{base_url}/page-{page}' if page > 1 else base_url
            driver.get(url)
            soup = bs(driver.page_source, 'lxml')
            topics = soup.find_all('div', class_=topic_selector)
            
            for topic in topics:
                topic_title = topic.find('a').text.strip()
                topic_url = f"{base_url.split('/forums')[0]}{topic.find('a').get('href').split('/page-')[0]}"
                
                # Scrape individual topic
                driver.get(topic_url)
                topic_soup = bs(driver.page_source, 'lxml')
                replies = topic_soup.find_all('div', class_=reply_selector)
                
                if not replies:
                    continue  # Skip if no replies
                
                # Extract question and images
                question = replies[0].find('div', class_="bbWrapper").text.strip()
                q_img = replies[0].find('img', class_="bbImage")
                q_img_url = q_img.get('src') if q_img else 'No Image'
                
                # Process replies
                for idx, reply in enumerate(replies[1:], 1):
                    reply_text = reply.find('div', class_="bbWrapper").text.strip()
                    img = reply.find('img', class_="bbImage")
                    img_url = img.get('src') if img else 'No Image'
                    video = reply.find('iframe')
                    video_url = video.get('src') if video else 'No Video'
                    
                    # Append data
                    topics_names.append(topic_title)
                    questions_content.append(question)
                    question_img.append(q_img_url)
                    replies_content.append(reply_text)
                    replies_order.append(idx)
                    image1.append(img_url)
                    video_link1.append(video_url)
                    topic_urls.append(topic_url)
                
                print(f'Page {page}: Scraped "{topic_title}" ({len(replies)-1} replies)')
                time.sleep(delay)  # Respectful delay

        except Exception as e:
            print(f'Error on page {page}: {str(e)}')
            time.sleep(delay)

    driver.quit()
    
    # Save data
    df = pd.DataFrame({
        'Topic': topics_names,
        'Question': questions_content,
        'Question_Image': question_img,
        'Reply': replies_content,
        'Reply_Order': replies_order,
        'Reply_Image': image1,
        'Video_Link': video_link1,
        'Topic_URL': topic_urls
    })
    
    if output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    else:
        df.to_csv(output_file, index=False)
    
    print(f'Scraping completed at {datetime.datetime.now()}')
    print(f'Data saved to {output_file}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Forum Scraper')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL of the forum (e.g., https://control.com/forums/forums/hmi.8)')
    parser.add_argument('--start_page', type=int, default=1, help='Starting page number')
    parser.add_argument('--end_page', type=int, required=True, help='Ending page number')
    parser.add_argument('--topic_selector', type=str, default='structItem-cell structItem-cell--main', help='CSS class for topics')
    parser.add_argument('--reply_selector', type=str, default='message-cell message-cell--main', help='CSS class for replies')
    parser.add_argument('--driver_path', type=str, required=True, help='Path to ChromeDriver')
    parser.add_argument('--output', type=str, default='forum_data.csv', help='Output filename (CSV or XLSX)')
    parser.add_argument('--delay', type=int, default=10, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    scrape_forum(
        base_url=args.base_url,
        page_start=args.start_page,
        page_end=args.end_page,
        topic_selector=args.topic_selector,
        reply_selector=args.reply_selector,
        driver_path=args.driver_path,
        output_file=args.output,
        delay=args.delay
    )