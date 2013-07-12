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

#How long the thread should sleep. 
SLEEP_TIME = 7*60

#Creates the praw Reddit object using User Agent defined in setup
r = praw.Reddit(user_agent=USER_AGENT)

#Relevant login info is included in login.py, passes the User Agent
login.login(r)

#Keep looping
while True:
	
    submissions = get_hot_submissions(r,SUBS_TO_CRAWL,POST_FETCH_LIMIT)
    
    for submission in submissions:
        
        add_submission_to_db = False
        
        update_timestamp_in_db = False 
        
        #Will evaluate to either True, False, or "ever"
        not_done = stalker.submission_not_done_recently(submission.id,  
                       TIME_BETWEEN__STALKING_SAME_SUBMISSION)
                    
        if (submission.num_comments > 0 and not_done):   
                        
            if not_done == "ever":    
                            
                add_submission_to_db = True   
                                        
            else:  
                                      
                update_timestamp_in_db = True                   
                
            comments = get_all_comments(submission)       
    
            if add_submission_to_db:    
                          
                stalker.add_submission_to_done(str(submission.id), 
                    str(submission.subreddit) )  
                
            if update_timestamp_in_db:   
                              
                stalker.update_submission(submission.id)  
                          
            for comment in (comments): 
                         
                global TRIGGER_PATTERN
    
                user_to_analyze = stalker.comment_has_trigger(comment,
                                      TRIGGER_PATTERN)
                             
                if(user_to_analyze): 
                       
                    self_check = (1 if (user_to_analyze == 
                                      str(comment.author)) else 0 )
                                      
                    add_user_to_db = False  
                   
                    not_done = stalker.user_not_done(user_to_analyze,                 
                                   TIME_BETWEEN_STALKING_SAME_USER)
    
                    if(not_done == "ever"): 
                           
                        add_user_to_db = True          
                                                
                    if(not_done):  
                      
                        reply = stalker.create_table_message(
                                    r , user_to_analyze,
                                    COMMENTS_TO_GET, ignore_words) 
                        if reply:  
                            
                            reply_successful = comment_reply(
                                                   comment , reply)     
                            if reply_successful:
								                                    
                                if(add_user_to_db):
									          
                                    total = stalker.get_total_words() 
                                     
                                    unique = stalker.get_unique_words() 
                                     
                                    stalker.add_user_to_done(
                                        user_to_analyze, self_check,
                                        total , unique )  
                                else:
									
                                    stalker.update_user(user)    
                            else:  
                            
                                break   

    #Thread sleeps for time specified, make changes for this in setup.py
    print "Going to sleep now for" , str(SLEEP_TIME / 60), "minutes"
    
    count = 0   
     
    while count < SLEEP_TIME:
		
        time.sleep(SLEEP_INTERVAL)
        
        print "Still asleep for another: ", 
            str(SLEEP_TIME - count), "seconds. Or ",
            str((SLEEP_TIME - count)/ 60), "minutes."
            
        count += SLEEP_INTERVAL





