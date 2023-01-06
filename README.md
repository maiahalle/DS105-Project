# Twitter Birds of a Feather Flock Together: Analyzing American Legislator's Frequent Used Words in Tweets

## Motivations

As the idiom "birds of a feather flock together" suggests, people of the same ideology, hobbies, and interests tend to stick together. Will this idiom ring true for American senators and repersenatives? To find out, our group analyzed the most frequent words used on Twitter in the past 30 days by all 535 Members of Congress. Will legislators from the same political party tweet similar words to each other? We predict that not only will legislators tweet similar words with their associated political party but Republicans will be more likely to tweet words like "family", "border", and "steal". This is because Republicans are traditionally known for their "family" values, borders and immigration is a key talking point for them, and the word "steal" is associated with right-wing conspiracies. On the other hand, we predict Democrats will frequently use "green" and "rights" because the Democratic party has been focusing their efforts on climate change and increasing rights for minority groups. With an increased polarization in not only Congress but in wider US society, the information we gather from Twitter is an important insight into what American legislators have on their mind and wether or not that alligns to the rest of their party. 

## Data Collection

**Data Set:**
We collected data from all of the current Congresspeople's Twitter accounts from the past 30 days. In total, this was xxxxx tweets. We got the list of Twitter handles from a Excel spreadsheet titled Congressional Twitter Accounts created by the University of California San Diego [(Link to Excel)](https://ucsd.libguides.com/congress_twitter). Our data set is comprised of 223 Democrats (including 4 Delegates) and 215 Republicans (including 1 Delegate and the Resident Commissioner of Puerto Rico), and 3 vacant seats. 

<img width="640" alt="Screen Shot 2023-01-04 at 8 22 27 PM" src="https://user-images.githubusercontent.com/117990566/210680386-51fec2fc-0a3b-4e0a-a43d-f653efc48b63.png">
This map illustrates the distribution of Congressional repersentatives throughout all 50 states.

<img width="490" alt="Screen Shot 2023-01-04 at 8 19 42 PM" src="https://user-images.githubusercontent.com/117990566/210680098-a14c614f-087a-4fbe-a10b-9afba17df567.png">
This map illustrates the distribution of Republican and Democratic legislators throughtout the US.

**Code:**
The code we used to gather our data can be divided into six key sections: implementing the API, finding the Twitter ids, creating a data frame of all tweets, extracting key words from the tweets, finding the word count, and finally, generating csv files.

1. Implemeting the Twitter API to gather tweets

`# call twitter api with request url and parameters and return the response in json

def connect_to_endpoint(url, params):
    session = requests.Session()
    # configure retrying with a pause for half a minute
    retry = Retry(connect=10, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    
    return response.json()`

2. Finding and returning the Twitter id based on passed twitter handle's of politicians

3. Geting all tweets for each Twitter id

4. Using spacy's natural language process to exctract key words from tweets

5. Counting how many times each key word was used
Adding new coloumn into the dataframe called word count

6. Return dictionary of dataframes and generate csv files



# NOTES TO INCLUDE: [delete later]
## It is important to note that we decided to exclude "rt" because , while it would give us interesting information on how mant times a congressperson retweeted in a month, our project only focuses on the individual words of the tweet. 
