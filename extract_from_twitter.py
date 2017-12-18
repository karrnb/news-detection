# !/usr/bin/env python
# encoding: utf-8

# Source of this code:
# https://stackoverflow.com/questions/37860411/extracting-tweet-from-twitter-api-using-python

import tweepy  # https://github.com/tweepy/tweepy
import csv
import sys
from twython import Twython

# Twitter API credentials
consumer_key = "TAJdcC416EOKij4mIbwsNSZ3e"
consumer_secret = "Jq0XnNqrGvPbceaQ04g7TbgGf9Pd0NAo7f6JGPcP97OMSi4nMT"
access_key = "2335751941-jEB9CtHfgpHrxao7G0pmu8STCyTXqXgIbITXuba"
access_secret = "efWk4lxnRNVrDRLl1BzoWQCYwbCovgnwREBa4jDiEdzUV"


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    return outtweets  

def get_tweets_using_hastags(hashtag):
    
    t = Twython(app_key=consumer_key, 
                app_secret=consumer_secret, 
                oauth_token=access_key, 
                oauth_token_secret=access_secret)

    search = t.search(q=hashtag, count=100)

    tweets = search['statuses']
    print "...%s tweets downloaded so far" % (len(tweets))

    return tweets

def write_into_csv(filename, item_list):
        # write the csv
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])

        for items in item_list:
            print (items)
            tweets = get_all_tweets(items)
            writer.writerows(tweets)

    pass

if __name__ == '__main__':
    # pass in the username of the account you want to download

    news_list = ["BBCBreaking", "cnnbrk", "WSJbreakingnews", "ReutersLive", "CBSTopNews", "SkyNewsBreak", "ABCNewsLive", "TWCBreaking", "BreakingNews", "breakingstorm"]
    non_news_list = ["pakalupapito", "Broslife", "awkwardfamily", "FakeAPStylebook", "TheBloggess", "ShitMyDadSays", "gordonshumway", "TomBodett", "badbanana", "Lmao", "ThatsSarcasm"]

    write_into_csv('non_news_tweets.csv', non_news_list)
    write_into_csv('news_tweets.csv', news_list)