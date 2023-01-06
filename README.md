# Twitter Birds of a Feather Flock Together: Analyzing American Legislator's Frequent Used Words in Tweets

## Motivations

As the idiom "birds of a feather flock together" suggests, people of the same ideology, hobbies, and interests tend to stick together. Will this idiom ring true for American senators and repersenatives? To find out, our group analyzed the most frequent words used on Twitter in the past 30 days by all 535 Members of Congress. Will legislators from the same political party Tweet similar words to each other? We predict that not only will legislators Tweet similar words with their associated political party but Republicans will be more likely to Tweet words like "family", "border", and "steal". This is because Republicans are traditionally known for their "family" values, borders and immigration is a key talking point for them, and the word "steal" is associated with right-wing conspiracies. On the other hand, we predict Democrats will frequently use "green" and "rights" because the Democratic party has been focusing their efforts on climate change and increasing rights for minority groups. With an increased polarization in not only Congress but in wider US society, the information we gather from Twitter is an important insight into what American legislators have on their mind and wether or not that alligns to the rest of their party. 

## Data Collection

**Data Set:**
We collected data from all of the current Congresspeople's Twitter accounts from the past 30 days. In total, this was xxxxx Tweets. We got the list of Twitter handles from a Excel spreadsheet titled Congressional Twitter Accounts created by the University of California San Diego (UCSD) [(Link to Excel)](https://ucsd.libguides.com/congress_twitter). Our data set is comprised of 223 Democrats (including 4 Delegates) and 215 Republicans (including 1 Delegate and the Resident Commissioner of Puerto Rico), and 3 vacant seats. 

<img width="640" alt="Screen Shot 2023-01-04 at 8 22 27 PM" src="https://user-images.githubusercontent.com/117990566/210680386-51fec2fc-0a3b-4e0a-a43d-f653efc48b63.png">
This map illustrates the distribution of Congressional repersentatives throughout all 50 states.

<img width="490" alt="Screen Shot 2023-01-04 at 8 19 42 PM" src="https://user-images.githubusercontent.com/117990566/210680098-a14c614f-087a-4fbe-a10b-9afba17df567.png">
This map illustrates the distribution of Republican and Democratic legislators throughtout the US.



**Code:**
The code we used to gather our data can be divided into six key sections: implementing the API, finding the Twitter IDs, creating a data frame of all Tweets, extracting key words from the Tweets, finding the word count, and finally, generating csv files.

1. Implemeting the Twitter API to gather Tweets
    
`def connect_to_endpoint(url, params):
    session = requests.Session()
    # configure retrying with a pause for half a minute
    retry = Retry(connect=10, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    
    return response.json()`

One of initial obstacels we had to over come for this project was the Twitter API, which has three types of access levels. The most basic level allows users to retrieve up to 500 thousand Tweets per month and have 25 requests per 15 minutes. These limits would hinder our ability to gather the amount of data we needed so we decided to apply for the elevated access to be able to retrieve up to 2 million Tweets per month and have 50 requests per 15 minutes.

2. Finding and returning the Twitter ID based on passed Twitter handle's of politicians

`def get_twitter_id(handle):
    json_response = connect_to_endpoint(create_userid_url(handle), None)

    # error checking in case a twitter handle can't be found
    if json_response and "data" in json_response:
        return {"id": json_response["data"]["id"],
                "name": json_response["data"]["name"]}
    else:
        print("Error: id not found for ", handle)
        return None`
    
The second major step in our code is to pass the Excel spreadsheet from UCSD into our code to find the Twitter ID of each Member of Congress. A Twitter ID is a Twitter generated, unique 64 number assigned to each Twitter user. For our projects puroposes, we use this ID to gather each legislators tweets from the past 30 days. 

3. Geting all Tweets for each Twitter ID

`   print("get tweets for ", handle)
    url = create_tweet_url(id_dict["id"])
    params = get_params()
    # get first page
    json_response = connect_to_endpoint(url, params)`

One code related challenge we faced was the length of time it took to run the code. Because our dataset contains 535 twitter users, the code would take hours to fully run. To keep track of the process of running code and to make sure things were running smoothly, we put print statements like `print ("loaded tweets from file for ", handle)` and `print("get tweets for ", handle)` 
 

4. Using spacy to exctract key words from Tweets

include_types = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
exclude_words = ["rt", "amp"]

The most frequent words in English are "the", 

are conjuctions like "and" and 

A third barrier we faced was the fact that prepositions, interjections, and conjunctions were the most frequently Tweeted words. However, words like "the", "at", and "in", do not give us context to what the Members of Congress are Tweeting and thinking about. To overcome this, we used Spacy's natural language process to extract onlt adjectives, nouns, propernouns, verbs and adverbs. It is important to note that we decided to exclude "rt" because , while it would give us interesting information on how mant times a congressperson reTweeted in a month, our project only focuses on the individual words of the Tweet. 

5. Counting how many times each key word was used
Adding new coloumn into the dataframe called word count

6. Return dictionary of dataframes and generate csv files



# NOTES TO INCLUDE: [delete later]
## 


# THINGS TO DO : [delete later]
## MAKE SURE TWEET AND TWITTER AND API AND ID IS CAPITALIZED, grammar, fix code format, make spaces between sections
