from pprint import pprint
import praw 
import re, string;





#converts json to normal text
def convert(input):
    """Converts Json to regular text

    :param input: Json to be converted to regular text
    :returns: A string
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input




def send_message(user_agent, recipient,  subject , message):
    """Sends a message to a Redditor; requires login() to have been called 

    :param user_agent: A Reddit Object(Praw)
    :param recipient: A String; Redditors Username
    :param subject: A String; Message Subject
    :param message: A string; Message body
    :returns: True if message sent; False otherwise
    """
    if (send_message):
        print('sending message to ' + recipient)
        try:
            user_agent.send_message(recipient, subject, message)
            return True
        except:
            print('unable to send message to ' + recipient)
            return False


def get_all_comments(submission):
    """Returns a flattened tree of all the comments in the submission passed 

    :param submission: A Submission Object(Praw)
    :returns: A list of Comments if submission contains any; None otherwise
    """
    if submission.num_comments > 0:
        return praw.helpers.flatten_tree(submission.comments)
    else:
        return None
        

def check_comment(text, trigger): 
    """Checks if text contains any of the words in trigger(Replaced by comment_has_trigger in stalker.py) 

    :param text: A String to check
    :param trigger: A List of Strings to check for in text
    :returns: True if a trigger exists in text; False otherwise
    """    
    if any(string in triggers for string in text.lower()):
        return True
    return False 


def comment_reply(comment , reply):
    """Replies to a Comment on Reddit; requires login() to have been called 

    :param comment: A Comment Object(Praw)
    :param reply: A String; the reply to post
    :returns: True if reply posted; False otherwise
    """
    try:
        print('Replying to ' + str(comment.author) + '\'s comment')
        comment.reply(reply)
        return True
    except:
        print('Error: unable to post comment')
        return False


def get_hot_submissions(r , sub , lim):
    """Fetches the hot submissions from a subreddit using lim as the limit 

    :param r: A Reddit Object(Praw)
    :param sub: A String; Subreddit name
    :param lim: An int; The limit on number of submissions to fetch
    :returns: A list of Submission Objects if fetch was sucessful; None otherwise
    """
    print('getting submissions...')
    try:
        submissions = r.get_subreddit(sub).get_hot(limit=lim)
        print('success fetching submissions...')
        return submissions
    except: 
        print('couldn\'t fetch submissions...')
        return None



