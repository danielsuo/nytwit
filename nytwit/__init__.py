import json
import bs4
import requests
from TwitterSearch import *

nyt_key = ""
nyt_base = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

search = TwitterSearch(consumer_key="",
                       consumer_secret="",
                       access_token="",
                       access_token_secret="")

# TODO: handle pagination
# TODO: handle new queries with more recent dates
results = requests.get(nyt_base, params={
    "api-key": nyt_key, "fq": 'news_desk:("Opinion")', "begin_date": 20190101, "page": 0})
results = json.loads(results.text)

for result in results["response"]["docs"]:
    url = result["web_url"]
    print(url)

    tso = TwitterSearchOrder()
    tso.set_keywords([url])

    max_score = 0
    best_tweet = None
    for tweet in search.search_tweets_iterable(tso):
        # if tweet["retweet_count"] == 171 and tweet["favorite_count"] == 0:
            # print(tweet)
        score = tweet["retweet_count"] + tweet["favorite_count"]
        if "retweeted_status" in tweet:
            print(score)
            score += tweet["retweeted_status"]["retweet_count"] + tweet["retweeted_status"]["favorite_count"]
            print(score)
        if score > max_score:
            max_score = score
            best_tweet = tweet
    if best_tweet is None:
        best_tweet = tweet

    print(best_tweet["retweet_count"], best_tweet["favorite_count"])
    print('@%s tweeted: %s' %
          (best_tweet['user']['screen_name'], best_tweet['text']))

# url = "https://twitter.com/mattdpearce/status/1145734605472817153"
# html = requests.get(url).text

# soup = bs4.BeautifulSoup(html, "html.parser")
# results = soup.find_all("div", class_="ProfileTweet-action ProfileTweet-action--reply")

# subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
# results = subsoup.find_all("span", class_="ProfileTweet-actionCountForPresentation")
# print(results[0].encode_contents().decode("ascii"))

# results = soup.find_all("div", class_="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt")

# subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
# results = subsoup.find_all("span", class_="ProfileTweet-actionCountForPresentation")
# print(results[0].encode_contents().decode("ascii"))

# results = soup.find_all("div", class_="ProfileTweet-action ProfileTweet-action--favorite js-toggleState")

# subsoup = bs4.BeautifulSoup(str(results[0]), "html.parser")
# results = subsoup.find_all("span", class_="ProfileTweet-actionCountForPresentation")
# print(results[0].encode_contents().decode("ascii"))
