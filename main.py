from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from collections import Counter
import time


def analyze_youtube_comments(driver, video_url):
    # initialize the web driver
    driver.get(video_url)

    # give it time to load
    time.sleep(5)

    prev_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll to bottom of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # wait some time for comments to load
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.comment-renderer')))
        except TimeoutException:
            print("Timed out waiting for comments to load.")

        # get new scroll height
        new_height = driver.execute_script(
            "return document.body.scrollHeight")

        if new_height == prev_height:
            break
        prev_height = new_height

    # extract comments
    comments = []
    comment_elements = driver.find_elements(
        By.CSS_SELECTOR, '.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap')
    for comment_element in comment_elements:
        comment_text = comment_element.text
        comments.append(comment_text)

    return comments


stop_words = ['the', 'i', 'to', 'this', 'of', 'a', 'and', 'in', 'is', 'that', 
              'it', 'but', 'get', 'on', 'at', 'nobody', 'an', 'were', 'me']


def find_common_words(comments):
    # returns list of 10 most common words
    # make em lowercase
    all_words = ''.join(comments).lower()
    # str.isalnum is a Boolean method indicating whether it's an
    # alphanumerical thang (no # OR @)
    words = [word for word in all_words.split() if word.isalnum()
             and word not in stop_words]
    word_counts = Counter(words)
    return [word for word, count in word_counts.most_common(10)]


video_url = 'https://www.youtube.com/watch?v=-RFunvF0mDw'

driver = webdriver.Chrome()

comments = analyze_youtube_comments(driver, video_url)

comment_lengths = [len(comment) for comment in comments]
if comments:
    avg_comment_length = sum(comment_lengths) / len(comment_lengths)
else:
    avg_comment_length = 0

common_words = find_common_words(comments)

driver.quit()

analysis = {
    'num_comments': len(comments),
    'avg_comment_length': avg_comment_length,
    'common_words': common_words
}
print(analysis)
