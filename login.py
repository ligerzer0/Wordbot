import praw 
from setup import *


#logs in
def login(r):
    """Logs in using credentials defined in setup.py

    :param r: A Reddit Object (Praw)
    :returns: True if login successful; False otherwise
    """    
    print "logging in...."
    try: 
        r.login(BOT_USERNAME,BOT_PASSWORD)
        print "logged in as" , BOT_USERNAME
        return True
    except:
        print "Unabe to log in as", BOT_USER
        return None
        



