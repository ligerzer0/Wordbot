from pprint import pprint
import praw 
import re, string;
import logging




#converts json to normal text
def convert(input):
    """Converts Json reddit comment object into a String 

    :param input: Json to be converted to regular text
    :returns: A string
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in 
                                                 input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input




def send_message(user_agent, recipient,  subject , message):
    """Sends a message to a Redditor

    :param user_agent: A Reddit Object(Praw)
    :param recipient: A String; Redditors Username
    :param subject: A String; Message Subject
    :param message: A string; Message body
    :returns: True if message sent; False otherwise
    """
    if (send_message):
        logging.info('sending message to %s',  recipient)
        try:
            user_agent.send_message(recipient, subject, message)
            return True
        except:
            logging.warning('unable to send message to %s', recipient)
            return False


def get_all_comments(submission):
    """Returns a flattened tree of all the comments in the submission 

    :param submission: A Submission Object(Praw)
    :returns: A list of Comments if submission contains any
    """
    if submission.num_comments > 0:
        return praw.helpers.flatten_tree(submission.comments)
    else:
		logging.warning("Submission %s contained no comments", 
		                submission.title )
        return None
        

def check_comment(text, trigger): 
    """Checks if text contains any of the words in trigger
       (Replaced by comment_has_trigger in stalker.py) 

    :param text: A String to check
    :param trigger: A List of Strings to check for in text
    :returns: True if a trigger exists in text; False otherwise
    """    
    if any(string in triggers for string in text.lower()):
        return True
    return False 


def comment_reply(comment , reply):
    """Replies to a Comment on Reddit; requires login()  

    :param comment: A Comment Object(Praw)
    :param reply: A String; the reply to post
    :returns: True if reply posted; False otherwise
    """
    try:
        logging.info('Replying to %s\'s comment' , str(comment.author))
        comment.reply(reply)
        return True
    except:
        logging.warning('Error: unable to post comment')
        return False


def get_hot_submissions(r , sub , lim):
    """Fetches the hot submissions from a subreddit using lim as limit 

    :param r: A Reddit Object(Praw)
    :param sub: A String; Subreddit name
    :param lim: An int; The limit on number of submissions to fetch
    :returns: A list of Submission Objects if fetch was sucessful
    """
    logging.info('getting submissions from %s with limit %s..', sub,
                  str(lim))
    try:
        submissions = r.get_subreddit(sub).get_hot(limit=lim)
        logging.info('success fetching submissions...')
        return submissions
    except: 
        logging.warning('couldn\'t fetch submissions...')
        return None



