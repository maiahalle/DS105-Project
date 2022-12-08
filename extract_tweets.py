# to use this code add "from twitter_word_count import get_most_common_words"
# to call this function you must pass the twitter handle
# some examples of calling the function
#   cruz_df = get_most_common_words("sentedcruz")
#   bernie_df = get_most_common_words("SenSanders")
#   aoc_df = get_most_common_words("aoc")
# This will return a dataframe with columns = ['Word', 'Count']


# import the required libraries
import requests
import pandas
import json
import spacy
import time
from collections import Counter
import config

# Storing and defining URL
base_url = "https://api.twitter.com/2/"

# build url to retrieve all recent tweets for a user
def create_tweet_url(user_id):
    return "{}users/{}/tweets".format(base_url, user_id)

# build the url to find user ids from a twitter handle
def create_userid_url(user_handle):
    return "{}users/by/username/{}".format(base_url, user_handle)

# create dictionary to get required fields for tweets and return maximum number of rows per request
def get_params():
    return {"tweet.fields":
                "id,text,author_id,conversation_id,created_at,in_reply_to_user_id,lang,possibly_sensitive,public_metrics",
            "max_results": 100}
    
# build the header needed to gain access with the Bearer token stored in the config file
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {config.bearer_token}"
    r.headers["User-Agent"] = "LSE-WordCounter"
    return r

# call twitter api with request url and parameters and return the response in json
def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    return response.json()

# find and return the twitter id based on passed twitter handle
# error handling: if no id is found return None and print an error message
def get_twitter_id(handle):
    json_response = connect_to_endpoint(create_userid_url(handle), None)

    # error checking in case a twitter handle can't be found
    if json_response and "data" in json_response:
        return {"id": json_response["data"]["id"],
                "name": json_response["data"]["name"]}
    else:
        print("Error: id not found for ", handle)
        return None
    
# convert tweet data into a flat dictionary
def get_tweet_dict(tweet, handle, name):
    metrics = tweet["public_metrics"]
    return {"handle": handle,
            "name": name,
            "tweet_id": tweet["id"],
            "author_id": tweet["author_id"],
            "lang": tweet["lang"],
            "replied_to": ",".join(tweet['edit_history_tweet_ids']),
            'created_at': tweet['created_at'],
            'tweet_text': tweet['text'],
            'possibly_sensitive': tweet['possibly_sensitive'],
            'conversation_id': tweet['conversation_id'],
            "retweet_count": metrics["retweet_count"],
            "reply_count": metrics["reply_count"],
            "like_count": metrics["reply_count"],
            "quote_count": metrics["quote_count"]}

# get all tweets for a twitter handle
# returns a tweet data in a dataframe
# if there are not tweets an empty dataframe will be returned
def get_tweets(handle):
    id_dict = get_twitter_id(handle)
    if id_dict is None:
        return None
    
    url = create_tweet_url(id_dict["id"])
    params = get_params()
    # get first page
    json_response = connect_to_endpoint(url, params)

    # initialize list to hold all the tweet dictionaries
    dict_list = []
    # while there is data to process extract tweet data
    while json_response and "data" in json_response:
        tweets = json_response["data"]
        # use extend function to merge tweets with previous dicts
        dict_list.extend([get_tweet_dict(tweet, handle, id_dict["name"]) for tweet in tweets])
        if "next_token" not in json_response["meta"]:
            break
        params['pagination_token'] = json_response["meta"]["next_token"]
        # api can only support 1 request per second
        time.sleep(1)
        json_response = connect_to_endpoint(url, params)
    return pandas.DataFrame(dict_list)
        
nlp = spacy.load("en_core_web_sm")
#since we are only looking for tokens we can turn off parsing and use more effiecent 
nlp.disable_pipe("parser")
nlp.add_pipe("sentencizer")
# all tokens that arent stop words or punctuations
include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
exclude_words = ["rt", "amp"]
def get_tokens(doc):
    return [token.lemma_.lower() for token in doc if token.is_alpha and token.pos_ in include_types and token.lemma_.lower() not in exclude_words]

def add_word_count(row):
    word_freq = Counter(row["key_word_list"])
    common_words = word_freq.most_common(50)
    df = pandas.DataFrame(common_words, columns = ['Word', 'Count'])
    df["handle"] = row["handle"]
    return df[["handle","Word","Count"]]

df_politicians = pandas.read_csv("reptweets.csv")

df_tweets = pandas.concat([get_tweets(handle) for handle in df_politicians["Handles"]])
# add key_word_list column from a list this is faster using the pipe to reduce loading loading times
df_tweets['key_word_list'] = [get_tokens(doc) for doc in nlp.pipe(df_tweets.tweet_text)]
df_tweets.to_csv('tweets.csv', encoding='utf-8', index=False)

df_grouped = df_tweets.groupby('handle',as_index=False).agg({'tweet_text': 'count','key_word_list': 'sum'})

#rename columns
df_grouped.rename(columns = {'tweet_text':'tweet_count'}, inplace = True)
df_grouped.to_csv("grouped.csv", encoding='utf-8', index=False)

df_word_count = pandas.concat([add_word_count(row) for index, row in df_grouped.iterrows()])
df_word_count.to_csv('word_count.csv', encoding='utf-8', index=False)
