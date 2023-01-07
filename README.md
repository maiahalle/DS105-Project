# Twitter Birds of a Feather Flock Together: Analyzing American Legislator's Frequent Used Words in Tweets

## Index
1. [Motivations](https://github.com/maiahalle/DS105-Project/blob/main/README.md#motivations) 
2. [Data Collection](https://github.com/maiahalle/DS105-Project/blob/main/README.md#data-collection)
    - Data Set
    - Code Explanation
3. [Exploratory Data Analysis](https://github.com/maiahalle/DS105-Project/blob/main/README.md#exploratory-data-analysis)
4. [Findings](https://github.com/maiahalle/DS105-Project/blob/main/README.md#findings)
5. [Conclusion](https://github.com/maiahalle/DS105-Project/blob/main/README.md#conclusion)
6. [Contributions](https://github.com/maiahalle/DS105-Project/blob/main/README.md#exploratory-data-analysis)
    - Maia
    - Amara
    - Samad
7. [Citations](https://github.com/maiahalle/DS105-Project/blob/main/README.md#citations)

## Motivations

As the idiom "birds of a feather flock together" suggests, people of the same ideology, hobbies, and interests tend to stick together. Will this idiom ring true for American senators and representatives? To find out, our group analyzed the most frequent words used on Twitter in the past 30 days by all 535 Members of Congress. Will legislators from the same political party Tweet similar words to each other? We predict that not only will legislators Tweet similar words with their associated political party, but Republicans will be more likely to Tweet words like "family", "border", and "steal". This is because Republicans are traditionally known for their "family" values, borders and immigration are key talking points for them, and the word "steal" is associated with right-wing conspiracies. On the other hand, we predict Democrats will frequently use "green" and "rights" because the Democratic party has been focusing their efforts on climate change and increasing rights for minority groups. With an increased polarization in not only Congress but in wider US society, the information we gather from Twitter are important insights into what American legislators have on their minds and whether or not that aligns with the rest of their party.

## Data Collection

**Data Set:**
We collected Tweets from all of the current Congresspeople's Twitter accounts from the past 30 days, which was almost 3 million Tweets. We got the list of Twitter handles from a Excel spreadsheet titled Congressional Twitter Accounts created by the [University of California San Diego (UCSD)](https://ucsd.libguides.com/congress_twitter). Our data set is comprised of 223 Democrats (including 4 Delegates) and 215 Republicans (including 1 Delegate and the Resident Commissioner of Puerto Rico), and 3 vacant seats. 

<img width="640" alt="Screen Shot 2023-01-04 at 8 22 27 PM" src="https://user-images.githubusercontent.com/117990566/210680386-51fec2fc-0a3b-4e0a-a43d-f653efc48b63.png">
This map illustrates the distribution of Congressional repersentatives throughout all 50 states.

---
**Code Expalnation:**
The code we used to gather our data can be divided into six key sections: implementing the twitter API to make querries, convertin json to dataframe, extracting key words from the Tweets, grouping and counting keywords per user, and finally, generating csv files. 

1. Implemet the Twitter API to retreive Twitter IDs and pages of Tweets

<pre><code>def connect_to_endpoint(url, params):
    session = requests.Session()
    # configure retrying with a pause for half a minute
    retry = Retry(connect=10, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)</code></pre>
    
One of initial obstacels we had to over come for this project was the Twitter API, which has three types of access levels. The most basic level allows users to retrieve up to 500 thousand Tweets per month and have 25 requests per 15 minutes. These limits would hinder our ability to gather the amount of data we needed so we decided to apply for the elevated access to be able to retrieve up to 2 million Tweets per month and have 50 requests per 15 minutes. However, even then, we had to retrive more than 2 million Tweets so we had to wait a month to finish gathering all our tweets. We also used csv files to store our data to avoid re-running the code more than necesary. 

2. Convert json to dataframe

The second major step we took was extracting the necesary data from the Twitter json response by creating a name value pair dictionary.

<pre><code>def get_tweet_dict(tweet, handle, name):
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
            "quote_count": metrics["quote_count"]}</code></pre>
       
       
       
<pre><code>dict_list.extend([get_tweet_dict(tweet, handle, id_dict["name"]) for tweet in json_response["data"]])</code></pre>
 
<pre><code>df_tweets = pandas.concat([get_tweets(handle) for handle in df_politicians["handle"]])</code></pre>

3. Use spacy to exctract key words from Tweets

<pre><code>include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
exclude_words = ["rt", "amp"]</code></pre>

A second barrier we faced was the fact that prepositions, interjections, and conjunctions were the most frequently Tweeted words. However, words like "the", "at", and "in", do not give us context to what the Members of Congress are Tweeting and thinking about. To overcome this, we used Spacy's natural language process to extract onlt adjectives, nouns, propernouns, verbs and adverbs. It is important to note that we decided to exclude "rt" because , while it would give us interesting information on how mant times a congressperson reTweeted in a month, our project only focuses on the individual words of the Tweet. 

4. Group and count keywords per user and list all of their Tweets

<pre><code>def group_tweets(df_tweets, group_filename):
    print("creating summary grouping by handle")
    df_grouped = df_tweets.groupby('handle',as_index=False).agg({'tweet_text': 'count','key_word_list': 'sum'})</code></pre>
    
<pre><code>df_grouped = group_tweets(df_tweets, group_filename)
        df_word_count = count_words(word_count_filename, df_grouped)</code></pre>

The second to last major step was to group all the keywords by Twitter handle and count the total amount of tweets. A third code related challenge we faced was the length of time it took to run the code. Because our dataset contains 535 twitter users, the code would take hours to fully run. To keep track of the process of running code and to make sure things were running smoothly, we put print statements like <pre><code>print("creating summary grouping by handle")</code></pre>.

5. Return dictionary of dataframes and generate csv files

<pre><code>df_tweets['key_word_list'] = [get_tokens(doc) for doc in nlp.pipe(df_tweets.tweet_text)]
df_tweets.to_csv(tweet_filename, encoding='utf-8', index=False)

df_grouped = group_tweets(df_tweets, group_filename)
df_word_count = count_words(word_count_filename, df_grouped)

return {"tweets_df": df_tweets, "summary_df": df_grouped, "freq_words_df": df_word_count}</code></pre>
    
Lastly, we generated the csv files. To do this, we first had to load the file containing the legislator's Twitter handles, and then for each politician we called the Twitter API and exctracted their tweets. The final dataframe which was converted into a csv file contained information on but not limited to the name, twitter id, text of the tweet, retweet, reply, and like counts, and list of the key texts.


## Exploratory Data Analysis

## Findings

## Conclusion

## Contributions

**Maia:**
Maia created the code to collect the Twitter data set and wrote the Index, Motivation, Data Collection, and Citations sections of the README.md.


**Amara:**

**Samad:**

## Citations

Brush, M. (2010, December 21). White House not concerned about new census numbers. Michigan Radio. Retrieved January 6, 2023, from https://www.michiganradio.org/politics-government/2010-12-21/white-house-not-concerned-about-new-census-numbers 

Smith, K. L. (2022, December 6). Congressional Twitter Accounts. San Deigo. Retrieved January 6, 2023, from https://ucsd.libguides.com/congress_twitter. 

# THINGS TO DO : [delete later]
## grammar,  organize the files better
