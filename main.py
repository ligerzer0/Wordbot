import praw
   # -*- coding: utf-8 -*-

import login
import logging
from setup import *
import re, string;
import urllib2
import sqlite3
from datetime import datetime
from algo import analyze

#logging file bot.log created in root directory by default
logging.basicConfig(filename='bot.log', filemode='w', level=logging.DEBUG)
#How long the thread should sleep.
SLEEP_TIME = 7*60
#Creates the praw Reddit object using User Agent defined in setup
r = praw.Reddit(user_agent=USER_AGENT)
#Relevant login info is included in login.py, passes the User Agent
login.login(r)
# Once the analyze funtion starts, the bot runs either until
# a user interrupt or an error occurs
analyze(r)
