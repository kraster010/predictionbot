import praw
import logging

logger = logging.getLogger('PredictionBot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("BitcoinMarkets")


def process_comment(comment):
    print comment.body
    print "-------------"


skip_first = 100
for comment in subreddit.stream.comments():
    if skip_first > 0:
        skip_first = skip_first - 1
        continue
    process_comment(comment)

#
#
# def latest(subreddit):
#     """return latest discussion thread"""
#     logger.debug("Fetching latest discussion thread")
#     for submission in subreddit.search("Daily Discussion", sort="new"):
#         if "Altcoin" in submission.title:
#             logger.debug("discarding %s", submission.title)
#             continue
#         if submission.author == "AutoModerator":
#             logger.debug("Latest discussion thread returned")
#             return submission
#     logger.warning("Could not find latest discussion thread. Returning None")
#     return None
#
#
# latest_daily_discussion = latest(subreddit=subreddit)
#
# for new_comment in latest_daily_discussion.comments.list():
#     if isinstance(new_comment, MoreComments):
#         continue
#
#     print new_comment.body