import os
import sys
import json
import time
import bs4
import requests
import random
# import twitter
import urllib.parse
import pandas as pd

from .config import Config

nyt_base = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
twitter_base = "https://twitter.com/search?q="

# api = twitter.Api(consumer_key=Config().get("TWITTER_CONSUMER_KEY"),
# consumer_secret=Config().get("TWITTER_CONSUMER_SECRET"),
# access_token_key=Config().get("TWITTER_ACCESS_TOKEN"),
# access_token_secret=Config().get("TWITTER_ACCESS_TOKEN_SECRET"),
# sleep_on_rate_limit=True,
# tweet_mode="extended")

# print(api.GetUserTimeline(screen_name="danielsuo"))

# print(Config().get("TWITTER_ACCESS_TOKEN_SECRET"))

NYTWIT_HOME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

links = pd.read_csv(os.path.join(NYTWIT_HOME, "data", "links.csv"))

for index, row in links.iterrows():
    url = row.link

    name = os.path.basename(url).split(".")[0]
    directory = "data/{}".format(name)
    os.system("mkdir -p {}".format(directory))

    print(url)

    max_score = 0
    best_tweet = None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'
    }
    twitter_url = "{}{}".format(twitter_base, url)
    response = requests.get(twitter_url, headers=headers)
    twitter_html = response.content

    with open("{}/twitter.html".format(directory), "w") as f:
        f.write(twitter_html.decode("utf-8"))

    twitter_soup = bs4.BeautifulSoup(twitter_html, "html.parser")
    tweets = twitter_soup.find(id="stream-items-id")
    tweets = bs4.BeautifulSoup(str(tweets), "html.parser")
    tweets = tweets.find_all(
        "li", class_="js-stream-item stream-item stream-item")

    reply_count = 0
    retweet_count = 0
    favorite_count = 0

    for tweet in tweets:
        soup = bs4.BeautifulSoup(str(tweet), "html.parser")

        results = soup.find_all(
            "div", class_="ProfileTweet-action ProfileTweet-action--reply")
        subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
        results = subsoup.find_all(
            "span", class_="ProfileTweet-actionCountForPresentation")
        count = results[0].encode_contents().decode("ascii")
        count = 0 if count.strip() == "" else int(count)
        reply_count += count

        results = soup.find_all(
            "div", class_="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt")
        subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
        results = subsoup.find_all(
            "span", class_="ProfileTweet-actionCountForPresentation")
        count = results[0].encode_contents().decode("ascii")
        count = 0 if count.strip() == "" else int(count)
        retweet_count += count

        results = soup.find_all(
            "div", class_="ProfileTweet-action ProfileTweet-action--favorite js-toggleState")
        subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
        results = subsoup.find_all(
            "span", class_="ProfileTweet-actionCountForPresentation")
        count = results[0].encode_contents().decode("ascii")
        count = 0 if count.strip() == "" else int(count)
        favorite_count += count

    print(reply_count, retweet_count, favorite_count)
    with open("{}/counts.json".format(directory), "w") as f:
        json.dump({"reply_count": reply_count, "retweet_count": retweet_count,
                   "favorite_count": favorite_count}, f)

    sleeptime = random.randint(5, 20)
    print("Sleeping for {} seconds...".format(sleeptime))
    time.sleep(sleeptime)

    # print(best_tweet["retweet_count"], best_tweet["favorite_count"])
    # print('@%s tweeted: %s' %
    # (best_tweet['user']['screen_name'], best_tweet['text']))

# url = "https://twitter.com/mattdpearce/status/1145734605472817153"
# html = requests.get(url).text

# soup = bs4.BeautifulSoup(html, "html.parser")
