from bot import PredictionParser


def run():
    comment = "!prediction i say bitcoin above 9000 in november 2018"
    print "Parsing: %s" % comment

    pp = PredictionParser()

    ret = pp.parse_message(comment)

    if not ret:
        return None

    cond, price, date = ret
    print "condition: %s" % cond
    print "price: %s" % price
    print "when: %s" % date
    #
    # def process_comment(comment):
    #     msg = comment.body
    #     print msg
    #     print "-------------"
    #
    # reddit = praw.Reddit('bot1')
    # subreddit = reddit.subreddit("BitcoinMarkets")
    # skip_first = 0
    # for comment in subreddit.stream.comments():
    #     if skip_first > 0:
    #         skip_first = skip_first - 1
    #         continue
    #     process_comment(comment)
    #
    # #
    # #
    # # def latest(subreddit):
    # #     """return latest discussion thread"""
    # #     logger.debug("Fetching latest discussion thread")
    # #     for submission in subreddit.search("Daily Discussion", sort="new"):
    # #         if "Altcoin" in submission.title:
    # #             logger.debug("discarding %s", submission.title)
    # #             continue
    # #         if submission.author == "AutoModerator":
    # #             logger.debug("Latest discussion thread returned")
    # #             return submission
    # #     logger.warning("Could not find latest discussion thread. Returning None")
    # #     return None
    # #
    # #
    # # latest_daily_discussion = latest(subreddit=subreddit)
    # #
    # # for new_comment in latest_daily_discussion.comments.list():
    # #     if isinstance(new_comment, MoreComments):
    # #         continue
    # #
    # #     print new_comment.body

    pass
