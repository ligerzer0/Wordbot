import praw
   # -*- coding: utf-8 -*-
import time
from funcs import *
import stalker
import login
import re, string;
import urllib2
import sqlite3
from datetime import datetime
from setup import *

#How long the thread should sleep. Since there is currently a 7 minute limit on this account for comment posting, it's an easy choice here
SLEEP_TIME = 7*60

#Creates the praw Reddit object using User Agent defined in setup
r = praw.Reddit(user_agent=USER_AGENT)

#Relevant login info is included in login.py, this only passes the User Agent
login.login(r)

#Keep looping
while True:
    #Gets the hot submissions from specified subreddit with the limit passed
    submissions = get_hot_submissions(r , SUBS_TO_CRAWL , POST_FETCH_LIMIT)
    
    for submission in submissions:
        
        #This is false for now and will be changed soon if needed
        add_submission_to_db = False
        #Same as above 
        update_timestamp_in_db = False 
        #This will return either True, False, or "ever", the latter meaning it isn't in the database at all
        not_done = stalker.submission_not_done_recently(submission.id , TIME_BETWEEN__STALKING_SAME_SUBMISSION)
                    
        if (submission.num_comments > 0 and not_done):   #If the submission has comments and has not been crawled recently, or at all
                    
            if not_done == "ever":                        #So if it has never been crawled
                add_submission_to_db = True                   #Then let's remember to add it to the database after crawling            
            else:                                         #Otherwise it must have been crawled but just not done recently        
                update_timestamp_in_db = True                 #So let's remember to update it's timestamp post crawling    
                
            comments = get_all_comments(submission)       #Fetch all the comments from this submission
    
            if add_submission_to_db:                  #Now if a new entry needs to be added in the database for this submission
                stalker.add_submission_to_done(str(submission.id), str(submission.subreddit))  #Add it
                
            if update_timestamp_in_db:                #Or if a submissions timestamp needs to be updated        
                stalker.update_submission(submission.id)  #Update it
            
                
            for comment in (comments):               #Now start iterating through the comments that were just fetched
                global TRIGGER_PATTERN

            
                #A username will be returned here iff comment contains the analyze command. It may return comment's author.
                user_to_analyze = stalker.comment_has_trigger(comment , TRIGGER_PATTERN)
                
                
                if(user_to_analyze):          #So if a username was returned
                    self_check =  1 if (user_to_analyze == str(comment.author)) else 0     #if user is analyzing themselves, selfcheck is 1, else 0
                    add_user_to_db = False    #Set this to false for now; will be changed as needed
                   
                    #Same as above; returns "ever" if never analyzed, True if analyzed but not recently
                    not_done = stalker.user_not_done(user_to_analyze , TIME_BETWEEN_STALKING_SAME_USER)
    
                    if(not_done == "ever"):         #So if this user has never been stalked
                        add_user_to_db = True           #Then let's remember to add them to the database
                                                
                    if(not_done):   # ...   
                                        #A reply will be returned if the table was sucessfully created; None returned otherwise
                        reply = stalker.create_table_message(r , user_to_analyze , COMMENTS_TO_GET, ignore_words) 
                        if reply:      #if a reply was returned 
                            reply_successful = comment_reply(comment , reply)     #Then reply to the comment that contained the command
                            if reply_successful:                                     #The reply comment may not have been posted due to ratelimit etc.
                                if(add_user_to_db):           #now if the user needs to be added to the database
                                    total = stalker.get_total_words()   #Get their total words typed from stalker
                                    unique = stalker.get_unique_words()  #As well as the number of unique words typed by them
                                    stalker.add_user_to_done(user_to_analyze , self_check, total , unique )   #Then pass these back to stalker
                                else:   #otherwise, the user just needs to be updated and not added
                                    stalker.update_user(user)    #So let's simply update that users timestamp
                            else:   #if the reply was not sucessfull
                                break   #it's likely we got hit by Reddit's ratelimit, so let's just take a break 

    #Thread sleeps for time specified, make changes for this in setup.py
    print "Going to sleep now for" , str(SLEEP_TIME / 60), "minutes"
    count = 0    
    while count < SLEEP_TIME:
        time.sleep(SLEEP_INTERVAL)
        print "Still asleep for another: ", str(SLEEP_TIME - count), "seconds. Or ", str((SLEEP_TIME - count)/ 60), "minutes."
        count += SLEEP_INTERVAL





