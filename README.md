# Twitter Birds of a Feather Flock Together: Analyzing American Legislator's Frequent Used Words in Tweets

## Index
1. [Motivations](https://github.com/maiahalle/DS105-Project/blob/main/README.md#motivations) 
2. [Data Collection](https://github.com/maiahalle/DS105-Project/blob/main/README.md#data-collection)
    - Data Set
    - Code Explanation
    - CSV Files
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
The code we used to gather our data can be divided into four key sections: implementing the twitter API to make querries, converting the twitter json response to a dataframe, extracting key words from each tweet, and lastly grouping and counting keywords per user. 

1. Implemet the Twitter API to retreive Twitter IDs and pages of Tweets
    
One of initial obstacels we had to overcome for this project was the Twitter API, which has three types of access levels. The most basic level allows users to retrieve up to 500 thousand Tweets per month and have 25 requests per 15 minutes. These limits would hinder our ability to gather the amount of data we needed so we decided to apply for the elevated access to be able to retrieve up to 2 million Tweets per month and have 50 requests per 15 minutes. However, even then, we had to retrive more than 2 million Tweets so we had to wait a month to finish gathering all our tweets. Additionallly the maximum number of tweets per request is 100 and it would take 15 minutes to retrieve 5,000 tweets. To put it into context, the average number of tweets per Member of Congress in our data set is 2,842 and most politiicians tweeted more than 3,000 for the 30 day time period we used. This means it would take around 10 minutes per legislator. To save time and prevent reaching the request limit, we used csv files to store our data to avoid using the Twitter API to ask for data we previously requested and re-running the code more than necesary. 

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
       
The JSON repsonse is a tree structure and we needed to create columns per tweet, so this function created a name value pair dictionary that could be used to create an array of consistent dictionaries to be used creating our panda dataframe.       

3. Use spacy to exctract key words from Tweets

<pre><code>nlp = spacy.load("en_core_web_sm")
nlp.disable_pipe("parser")
nlp.add_pipe("sentencizer")</code></pre>

To make the code run faster, we used the sentencizer rather than the default parser since we were only using a limited number of functions from Spacy. 

<pre><code>include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]

def get_tokens(doc):
    return [token.lemma_.lower() for token in doc if token.is_alpha and token.pos_ in include_types and token.lemma_.lower() not in exclude_words]</code></pre>
    
A second barrier we faced was the fact that prepositions, interjections, and conjunctions were the most frequently Tweeted words. However, words like "the", "at", and "in", do not give us context to what the Members of Congress are Tweeting and thinking about. To overcome this, we used Spacy's natural language process to extract only adjectives, nouns, propernouns, verbs and adverbs. Furthermore, to group past tense, plurals, and similar variables of the same word we used the lemma to extract only the base word. For example, "history", "historical", and "histories" would all be grouped into  "history".

<pre><code>exclude_words = ["rt", "amp"]</code></pre>

It is important to note that we decided to exclude "rt" because , while it would give us interesting information on how mant times a congressperson re-tweeted in a month, our project only focuses on the individual words of the Tweet. 

4. Group and count keywords per user and list all of their Tweets

<pre><code>def add_word_count(row):
    word_freq = Counter(row["key_word_list"])
    common_words = word_freq.most_common(50)
    df = pandas.DataFrame(common_words, columns = ['Word', 'Count'])
    df["handle"] = row["handle"]
    return df[["handle","Word","Count"]]</code></pre> 

The last major step was to group all the keywords by Twitter handle and to gather all the keywords from each Tweet into one array to count. Finally, we used a Counter to count the keywords and then find the 50 most frequently used word per legislator, which we used to create a new data frame and csv file. 

<img width="201" alt="image" src="https://user-images.githubusercontent.com/117990566/211174292-baf767c5-bc0b-41d6-b918-ebdcb75063e0.png">
This is a snipet of what our csv file looks like. On the far left is Rep. Austin Scott's Twitter handle, in the middle is 5 of his top 50 frequntly used keywords, and then on the far right is how many times each word was used in the time frame. 

---
**CSV Files:**

Becuase the csv files were too large to upload to github, I have linked the grouped.csv and tweets.csv files here.

grouped.csv:
https://drive.google.com/file/d/1dQA9-0dUVCP86vxsk16WZewj3J7u6yGM/view?usp=drive_web

tweets.csv:
https://drive.google.com/file/d/1PgatNy2y8jExcTvWxDlkcaUwN9YTWHFV/view?usp=drive_web

## Exploratory Data Analysis

What is in the data? 
What does it look like in general? 
How big are your datasets? 
What is the range and distribution of the most relevant variables?


## Findings

## Conclusion

## Contributions

**Maia:**
Maia created the code to collect the Twitter dataset and wrote the Index, Motivation, Data Collection, and Citations sections of the README.md.

**Amara:**

**Samad:**

## Citations

Brush, M. (2010, December 21). White House not concerned about new census numbers. Michigan Radio. Retrieved January 6, 2023, from https://www.michiganradio.org/politics-government/2010-12-21/white-house-not-concerned-about-new-census-numbers 

Smith, K. L. (2022, December 6). Congressional Twitter Accounts. San Deigo. Retrieved January 6, 2023, from https://ucsd.libguides.com/congress_twitter. 

# THINGS TO DO : [delete later]
## grammar,  organize the files better
