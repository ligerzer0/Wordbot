import praw
import time
import json
import math
from funcs import *
from setup import *
import re, string;
from collections import Counter
from operator import itemgetter, attrgetter
import os
import sqlite3
from datetime import datetime
import logging

TOTAL_WORDS = 0 
UNIQUE_WORDS = 0


def get_db(path): 
    """Creates a sqLite database Object

    :param path: A String; should be a valid path to the database
    :returns: A database object if one was created; None otherwise
    """
    try:
        #connects to database
        db = (sqlite3.connect(path, 
                 detect_types=
                 sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) )
        logging.info("Database Connection Established...")
        return db
        
    except:
        logging.warning("Error Connecting to database")
        return None


def get_cursor(database):
    """Creates a Cursor Object for interacting with a database

    :param database: A Database Object(sqlite)
    :returns: A Cursor Object if one was created; None otherwise
    """
    try:
        cur = database.cursor()
        logging.info("Cursor sucessfully created in stalker")
        return cur
    except:
        logging.warning("Error creating cursor in stalker")
        return None


#Initializes the database object
db = get_db(DATABASE_PATH)
#Initializes the Cursor object 
cur = get_cursor(db)


def get_users_comments(r,user,number):
    """Fetches [number] comment from [user]'s comment history

    :param r: A Reddit Object(Praw)
    :param user: A String; Redditors Username
    :param number: An int; number of comments to fetch
    :returns: A list of comments; None if none fetched
    """        
    if user == BOT_USERNAME:
        return None
    
    users_comments = []

    while True:
        len_A = len(users_comments)
        comments = r.get_redditor(user).get_comments(limit=number)
        logging.info("length now is %s", str(len(comments)) )
       
 
        users_comments.extend(comments)
        len_B = len(users_comments)
        logging.info("fetched comments: %s", str(len_B))
    
        if not (len_B > len_A)  or len(users_comments) >= number:
            logging.info("DONE fetching comments")
            break
    
    logging.info("Total number of users comments fetched: %s",
                     str(len(users_comments)) )
    full_comments =  []
    for comment in users_comments:
        full_comments.append(convert(comment.body.lower()))    
    li = []
    for x in full_comments:
        li.append(x.split())
    return li


def build_table(wSet , wList , to_ignore,  cutoff):
    """Creates a string that will format as a table on Reddit 

    :param wSet: A List of unique words 
    :param wList: A List of words 
    :param to_ignore: A List of words to omit from the table; 
    :param cutoff: An int; the minimum number of times a word must 
                   appear in wList it to be included in the table
    :returns: A String that is a table
    """
    table = ""
    th = ("|\tWord\t\t|# of Occurences\t|\t   % \t\t|\n")
    table += th
    table += ("|:-------------------------|------------------------:|"
              ":-------------------------------:|")
    unique_words = len(wSet)
    total_words = len(wList)
    global TOTAL_WORDS
    TOTAL_WORDS = total_words
    global UNIQUE_WORDS
    UNIQUE_WORDS = unique_words
    cnt = Counter(wList)    
    word_dict = cnt.items()
    sorted_set = sorted(word_dict, key=itemgetter(1),  reverse=True)

    #for each unique word in the set    
    for item in sorted_set:
    #count how many times it appeared in the list        
        word = item[0]
        count = item[1]
        pct = round(float(count) / float(unique_words) * 100 , 2)
        if count > cutoff and word not in to_ignore and 
                          len(word) is not 2 and not word == "**":
            row = ("|\t   *{0}*    \t\t|\t{1}\t\t|\t\t{2}%    \t|".
                   format(word, str(count), str(pct), str(unique_words),
                    str(total_words) ) )
            table += "\n" + row
    return table

def create_table_message( r, user , num_comments , ignored ):
    """Uses build_table function to create a message complete with 
       analysis and some other rambling

    :param r: A Reddit Object(Praw)
    :param user: A String; Redditors Username
    :param num_comments: An Int; how many comments by the user to fetch
    :param ignored: A List of words to be silently ignored
    :returns: A String that is a complete reply to an analyze inquire
    """    
    comments = get_users_comments(r , user , num_comments)
    
    if not comments:
        info.warning("Well..user %s doesn't appear to have posted" 
                     "any comments...", user) 
        return None    
        
    pattern = re.compile('(?!\s)(?!\')[\W]')    
    
    word_list = []
    
    for c in comments:
        text = pattern.sub('', str(c))
        word_list = word_list + text.split()

    word_list = [l.replace ('u\'', '') for l in word_list]
    word_list = [l.replace ('\':', '') for l in word_list]
    word_list = [l.replace ('\'', '') for l in word_list]
    word_list = [l.replace ('**' , '') for l in word_list]

    word_set = set(word_list)

    message = "Greetings. This is " + BOT_AGENT_NAME + ".\n"
    message += ("##The following table has been generated using"
               "the last " + str(num_comments) + " comments")
    message += " by /u/{}.\n".format(user)    
    message += ("##A list of commonly abused words has been"
                "excluded. \n")
    message += ("##Excluded words:\n[")
    for w in ignored:
        message+= "\t|" + w + "|"

    message += "]\n\n"
    message += "###Total words typed: " + str(len(word_list)) + "\n"
    message += ("###Number of unique words typed: " + 
                str(len(word_set)) + "\n")           
    
    table = build_table(word_set , word_list, ignored,  40)
    message += table
    
    
    footer = ("\nI am still underdevelopment. I am written in python"
              "using the PRAW Reddit API wrapper.\n")
    footer += ("\nYou can find my source code"
               "[here](https://github.com/ligerzer0/Wordbot)\n")
    footer += "\nTo use me, simply enter the following command:\n"
    footer += "\n    wordbot analyze [enter username here]\n"
    footer += ("\nYou may pass 'me' as the username if you wish to see"
               "stats about your own word usage.\n")
    footer += "\n **Note: the square brackets are necessary.**\n"
    footer += ("\nAs an example, let's say one were to request stats on"
              "a user 'Bob'\n")
    footer+=  "\nThen the command would be as follows:\n"
    footer += "    wordbot analyze [Bob]\n"
    footer += "\nSoon, I shall be equipped with snynonyms ... *Soon*\n."
    footer += ("\nFeel feel to make suggestions/compaints to my human,"
               "/u/" + CREATOR + "\n")    

    message += footer
    return message


def add_user_to_done(user, self_check, total, unique):
    """Adds a user the database of users who have been analyzed already 

    :param user: A String; Redditor's username
    :param self_check: 0 or 1 depending on if [user] requested analysis 
                       on their own comment history
    :param total: An Int; total number of words fetched from [user]'s 
                  comment history
    :param unique: An Int; total number of unique words fetched from 
                   [user]'s comment history
    :returns: True if addition was made to the database; False otherwise
    """
    self_ch = True if (self_check == 1) else False 
    try:    
        cur.execute("INSERT into Done_Users(user_name, self_check,"
                    "total_words, unique_words) VALUES(? , ?, ?, ?)", 
                     [user,	self_ch, total, unique])
        db.commit()
        return True
    except: 
        logging.warning("Unable to insert entry into User table:"
                        "user: %s", user )        
        return False

    
def words(fileobj):
    """This function is not used. It extracts words from a textfile;
       useful if you don't want to use a database but rather a text file

    :param fileobj: A File object
    :returns: Words in fileobj
    """
    for line in fileobj:
        for word in line.split():
            yield word

def user_not_done(user, limit):
    """Checks if [user] has been analyzed in the last [limit] seconds,
       or not at all

    :param user: A String; Redditors Username
    :param limit: An int; the time in seconds that quantifies "recently"
    :returns: True if user has been analyzed recently; False if not
              recently; String "ever" if never analyzed
    """
    cur.execute("SELECT date as DATETIME from Done_Users where"
                "user_name = ?", [user])
    row = cur.fetchone()
    if row:
        now = datetime.now()
        then = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        time_delta = then - now
        import math        
        return math.fabs(time_delta.total_seconds()) > limit
    return "ever"    

def add_submission_to_done(the_id, subreddit):
    """Adds a submission's id to the database

    :param the_id: A String; unique id of a Submission object
    :param subreddt: A String; the subreddit where the submisison was 
                     posted
    :returns: True if successfully added to database; False otherwise
    """
    try:    
        cur.execute("INSERT into Submission(submission_id, subreddit)"
                    "VALUES(? , ?)", [the_id , subreddit])
        db.commit()
        return True
    except: 
        logging.warning("Unable to insert entry into Submission table:"
              "id: %s subreddit: %s", the_id, subreddit )    
        return False
        
def submission_not_done_recently(the_id , limit):
    """Checks if a submission with [the_id] has been analyzed in the
       last [limit] seconds, or not at all

    :param the_id: A String; A Submission Objects id attribute
    :param limit: An int; the time in seconds that quantifies "recently"
    :returns: True if submission has been analyzed recently; False if 
              not recently; String "ever" if never analyzed
    """    
    
    cur.execute("SELECT date as DATETIME FROM Submission WHERE"
                "submission_id= ?", [the_id]) 
    row = cur.fetchone()
    if row:
        now = datetime.now()
        then = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")        
        time_delta = then - now
        import math                    
        return math.fabs(time_delta.total_seconds()) > limit
    return "ever"

def update_submission(the_id):
    """Updates the timestamp of a submission with [the_id] in database

    :param the_id: A String; A Submission Objects id attribute
    :returns: True if update successful; False otherwise
    """    
    try:
        cur.execute("UPDATE Submission SET date=CURRENT_TIMESTAMP WHERE" 
                    "submission_id=?", [the_id])
        db.commit() 
        return True
    except:
        return False

def update_user(user):
    """Updates the timestamp of [user] in the database

    :param user: A String; A redditors username
    :returns: True if update successful; False otherwise
    """    
    try:
        cur.execute("UPDATE Done_Users SET date=CURRENT_TIMESTAMP WHERE" 
                    "user_name=?", [user]) 
        db.commit()
        return True
    except:
        return False
        
def get_total_words():
    """Reads the global TOTAL_WORDS in stalker.py 

    :returns: An int which is the total words for user being analyzed, 
              if it has been set to a non-zero value; None otherwise
    """        
    global TOTAL_WORDS
    t = TOTAL_
    WORDS    
    if(t > 0):
        return t
    return None    

#returns the number of unique words used by a user
def get_unique_words():
    """Reads the global UNIQUE_WORDS in stalker.py 

    :returns: An int which is the total number of unique words for user 
              being analyzed, if it has been set to a non-zero value; 
              None otherwise
    """        
    global UNIQUE_WORDS
    u = UNIQUE_WORDS
    if(u > 0):
        return u
    return None            


def comment_has_trigger(comment, pattern):
    """Checks if [comment] contains a match for [pattern]

    :param comment: A Comment Object(Praw)
    :param pattern: A regex Object(created with re.compile); 
                    see global TRIGGER_PATTERN in setup.py
    :returns: A string which is assumed to be a valid username; False 
              if no match was found
    """        
    author = str(comment.author)
    if author == BOT_USERNAME:
        return None
    comment_text = convert(comment.body.lower())
    line = pattern.search(comment_text)
    if(line):
        user = line.group(1)
        if user == "me":
            return author
        elif user == BOT_USERNAME:
            return None
        return user
    return None



