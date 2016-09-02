# Wordbot
### A customizable Reddit crawler for analyzing data on reddit

To run, first edit `setup.py`.    
Provide the required settings--the bot needs a reddit account to run.

All other settings can be left as default, or changed as needed.

Once you run `main.py` the bot is live and waiting for a tigger comment in the specified sub (both of which can be modified in setup.py).  

Default syntax for a trigger comment: `wordbot analyze [redditor's username here]`   
Let's say the following comment was posted: `wordbot analyze bakuretsu`   
Bakuretsu is a randomly chosen real redditor; wordbot's reply to the above comment can be seen [here](https://www.reddit.com/r/test/comments/1i40m5/testing_obviously/cb0rt7p)

------
#####__How does it work__?
------
1. Wordbot crawls the specified subreddit(s) waiting for the trigger comment ( see `setup.py` )
2. If the trigger comment contained a valid reddit username, data extraction begins
3. Wordbot extracts the given user's comment and submission history( by default their last 500 comments)
4. Wordbot then builds a report detailing:   
  + Distinct words the user has posted to the website   
  + The relative frequency with which the users uses that word   
5. This report is posted on reddit as a reply to the tigger comment

######(By default [/r/test](reddit.com/r/test) is the only subreddit set to be crawled)
###### To prevent being banned by reddit, use [/r/test](reddit.com/r/test). You can spam away here without being banned.


Words considered to be fillers are ignored by default.
The list of these ignored words can be seen and modified via `setup.py`.
Analyzing user vocabularies is just one potential usage, it is trivial to modify Wordbot for other types of analysis.
