import helpers as h
from setup import *
import logging
import time

def analyze(r):
    #Keeps looping, taking short breaks, sleep value is in setup
    while True:
        submissions = h.get_hot_submissions(r,SUBS_TO_CRAWL,POST_FETCH_LIMIT)
        for submission in submissions:
            add_submission_to_db = False
            update_timestamp_in_db = False
            #Will evaluate to either True, False, or "ever"
            not_done = h.submission_not_done_recently(submission.id,
                           TIME_BETWEEN__STALKING_SAME_SUBMISSION)
            if (submission.num_comments > 0 and not_done):
                if not_done == "ever":
                    add_submission_to_db = True
                else:
                    update_timestamp_in_db = True
                comments = h.get_all_comments(submission)
                if add_submission_to_db:
                    h.add_submission_to_done(str(submission.id),
                        str(submission.subreddit) )
                if update_timestamp_in_db:
                    h.update_submission(submission.id)
                for comment in (comments):
                    global TRIGGER_PATTERN
                    user_to_analyze = h.comment_has_trigger(comment,
                                          TRIGGER_PATTERN)
                    if(user_to_analyze):
                        self_check = (1 if (user_to_analyze ==
                                          str(comment.author)) else 0 )
                        add_user_to_db = False
                        not_done = h.user_not_done(user_to_analyze,
                                       TIME_BETWEEN_STALKING_SAME_USER)
                        if(not_done == "ever"):
                            add_user_to_db = True
                        if(not_done):
                            reply = h.create_table_message(
                                        r , user_to_analyze,
                                        COMMENTS_TO_GET, ignore_words)
                            if reply:
                                reply_successful = comment_reply(
                                                       comment , reply)
                                if reply_successful:
                                    if(add_user_to_db):
                                        total = h.get_total_words()
                                        unique = h.get_unique_words()
                                        h.add_user_to_done(
                                            user_to_analyze, self_check,
                                            total , unique )
                                    else:
                                        h.update_user(user)
                                else:
                                    break

        #Thread sleeps for time specified, make changes for this in setup.py
        logging.info("Going to sleep now for %s minutes",
                         str(SLEEP_TIME / 60) )

        count = 0

        while count < SLEEP_TIME:

            time.sleep(SLEEP_INTERVAL)

            logging.info("Asleep for another: %s seconds. OR  %s mins",
                str(SLEEP_TIME - count),
                str((SLEEP_TIME - count)/60)    )

            count += SLEEP_INTERVAL
