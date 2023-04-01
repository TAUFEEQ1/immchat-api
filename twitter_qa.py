import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
# Replace with the URL of the account's "with_replies" page
account_url = "https://twitter.com/DCICUg/with_replies"

# Replace with the number of replies you want to scrape
num_replies = 300

# Initialize ChromeDriver and navigate to the account URL
driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get(account_url)

replies = []

def get_tweets():
    # Find all the tweet cards on the page
    tweet_cards = driver.find_elements(By.XPATH,'//article[@data-testid="tweet"]')
    # Get the text and URL of each reply
    for card in tweet_cards:
        try:
            reply = {"topic":'tweet','qn':'unknown'}
            reply['ans'] = card.find_element(By.XPATH,'.//div[@lang="en"]/span').text
            reply['link'] = card.find_element(By.XPATH,'.//a[contains(@href,"/status/")]').get_attribute('href')
            replies.append(reply)
        except:
            continue    

# Scroll down to load more tweets
for i in range(30):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    get_tweets()
    time.sleep(10)

# Print the replies
driver.quit()

# Open a file for writing
with open("twitter_qa.json", "a") as json_file:
    # Encode the dictionary to JSON and write to file
    json.dump(replies, json_file)