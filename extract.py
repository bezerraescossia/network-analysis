from twython import Twython, TwythonError
from pprint import pprint
import itertools
from os.path import join
import json
from datetime import datetime, timedelta

days_ago = 1

def authentification():
    my_file = open("keys.txt", "r")
    content = my_file.read()
    API_KEY, API_SECRET_KEY = content.split("\n")
    my_file.close()

    twitter = Twython(API_KEY, API_SECRET_KEY)
    authentication_tokens = twitter.get_authentication_tokens()
    print(authentication_tokens['auth_url'])
    VERIFIER = input('Enter verification code: ')

    twitter = Twython(API_KEY, API_SECRET_KEY,
                  authentication_tokens['oauth_token'],
                  authentication_tokens['oauth_token_secret'])
    authorized_tokens = twitter.get_authorized_tokens(VERIFIER)
    
    twitter = Twython(
        API_KEY, API_SECRET_KEY,
        authorized_tokens['oauth_token'],
        authorized_tokens['oauth_token_secret']
    )

    return twitter

def get_tweets(twitter):
    NUM_TWEETS_TO_FETCH = 1000
    cursor = twitter.cursor(
        twitter.search, q='eleições 2022', 
        count=100, result_type='mixed', 
        until=(datetime.now() - timedelta(days = days_ago)).strftime("%Y-%m-%d")
        )
    search_tweets = list(itertools.islice(cursor, NUM_TWEETS_TO_FETCH))
    return search_tweets

def filter_retweets(search_tweets):
    retweets = []
    for tweet in search_tweets:
        if 'retweeted_status' in tweet:
            retweets.append(tweet)
    return retweets

if __name__ == '__main__':
    twitter = authentification()
    search_tweets = get_tweets(twitter)
    retweets = filter_retweets(search_tweets)
    
    with open(join('datalake', f'extract_date={(datetime.now() - timedelta(days = days_ago)).strftime("%Y-%m-%d")}.json'), 'w') as outfile:
        json.dump(retweets, outfile)
    
    print('Tweets sobre "Eleições 2022" extraidos e salvo com sucesso!')