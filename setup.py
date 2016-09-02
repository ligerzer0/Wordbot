import re

#-------------------------------------------------------------------------------------------------------------------------------
# REQUIRED SETTINGS. Change everyone single one of these
#This is the account information of the bot; Change these to their appropirate values
BOT_USERNAME = 'ligerzer0'
BOT_PASSWORD = 'kyokushin'

#Path to the sqlite database to be used
DATABASE_PATH = "BotData.sqlite"
#To be used in the User Agent description
BOT_AGENT_NAME = "Word Analyzer Bot"
VERSION = "v1.3"

#Reddit username of human being responsible for this bot
CREATOR = "LigerZero"





#-------------------------------------------------------------------------------------------------------------------------------
#              NOT REQUIRED, but you should really change these
#-------------------------------------------------------------------------------------------------------------------------------

#              By default matches the string "wordbot analyze [?]"
#                  where ? will be tried as Redditor's username
TRIGGER_PATTERN = re.compile('\w*wordbot\sanalyze\s\[([^]]*)\]')

#              Words to omit from the analysis
ignore_words = ['that' , 'the' , 'to', 'and' , 'a' , 'it' , 'in',
                'is', 'this' , 'on', 'not', 'are', 'or' , 'but',
                'for' , 'of', 'was', 'as', 'with', 'if' , 'so',
                'can', 'what' , 'from', '**', 'its' , 'they' ,
                'your', 'their' , 'them' , 'when', 'theyre' ,
                'there' , 'dont' ]

#--------The Subreddits that the bot will crawl; append using +
SUBS_TO_CRAWL = 'test+learnpython'



#-------------------------------------------------------------------------------------------------------------------------------
#       You may leave as they are.
#       User Agent description is required in the arguments
#          when creating a User Agent
USER_AGENT = ("User-Agent: {0} {1} by /u/{2}".
                 format(BOT_AGENT_NAME, VERSION, CREATOR ))

#The limit on how many submissions to fetch from each subreddit
POST_FETCH_LIMIT = 10

#Time in seconds to wait before stalking a user twice
TIME_BETWEEN_STALKING_SAME_USER = 7*24*60*60

#Time in seconds to wait before stalking a submission twice
TIME_BETWEEN__STALKING_SAME_SUBMISSION = 1*60

# Number of comments to be fetched from targe users comment history
# If a users total comments < this number, then all of them will be used
COMMENTS_TO_GET = 500

# How long the thread should sleep. Since there is currently a 7 minute
# limit on this account for comment posting, it's an easy choice here
SLEEP_TIME = 7*60
#How often while sleeping should the bot wake up and send a quick
#  message before going back to sleep
SLEEP_INTERVAL = 20
