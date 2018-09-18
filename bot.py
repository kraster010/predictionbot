import praw
from parse import *
import logging
from datetime import datetime

logger = logging.getLogger('PredictionBot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# !prediction < (PRICE) DATE
# !prediction > (PRICE) DATE
# !prediction less (PRICE) DATE
# !prediction greater (PRICE) DATE
# !prediction (PRICE) DATE

# DATE -> 21/03/1989 or 1989/03/21

@with_pattern(r'\d{4}/\d\d?/\d{2}')
def parse_date(text):
    return text


@with_pattern(r'0*\d{4}')
def parse_year(text):
    text = text.lstrip("0")
    return int(text)


@with_pattern(r'0*\d\d?')
def parse_day_month(text):
    text = text.lstrip("0")
    return int(text)


@with_pattern(
    r'(0*\d\d?|(september|october|november|december|january|febraury|march|april|may|june|july|august))\s+0*\d{4}')
def parse_verbose(text):
    temp = [x.strip() for x in text.lstrip("0").split() if x]
    return {"month": temp[0], "year": temp[1]}


@with_pattern(r'(@|at|above|below|less|greater|>|<)')
def parse_condition(text):
    return text


months = ["january", "febraury", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "dicember"]

year = "{year:^ty}"
month = "{month:^td}"
month_verbose = "{monthv:^tdv}"
day = "{day:^td}"
delim = ["-", "/"]
format_date = [year + d + month + d + day for d in delim] + \
              [day + d + month + d + year for d in delim] + \
              [month + d + year for d in delim] + \
              [month_verbose]

format_price = "{price:^g}"
format_cond = "{cond:^cs}"

comment = "asdasdasd less than 8900 waddaw 21/02/ 2018"

print "message: %s" % comment

price = search(format_price, comment)
if price:
    price = price["price"]
cond = search(format_cond, comment, extra_types=dict(cs=parse_condition))
cond = cond["cond"] if cond else "at"
if cond == "@":
    cond = "at"
elif cond == "<":
    cond = "less"
elif cond == ">":
    cond = "greater"

res = None
final_f = None
for f in format_date:
    res_temp = search(f, comment, extra_types=dict(ty=parse_year, td=parse_day_month, tdv=parse_verbose))
    if not res_temp:
        continue
    res = res_temp
    final_f = f
    break

if not res:
    print "missing date in comment, abort."

date = res

datetime_object = None

if date:
    if "monthv" in final_f:
        date = date["monthv"]
        temp = months.index(date["month"])
        if temp != -1:
            date["month"] = temp + 1

        date["month"] = '%02d' % date["month"]
        datetime_object = datetime.strptime('{} {}'.format('%02d' % date["month"], date["year"]), '%m %Y')
    else:
        print date
        month = date["month"]
        datetime_object = datetime.strptime('{} {} {}'.format('%02d' % date["day"],'%02d' % date["month"], date["year"]), '%d %m %Y')

if not datetime_object:
    exit(-1)

print "condition: %s" % cond
print "price: %s" % price
print "when: %s" % datetime_object
exit(-1)

date = ""


def process_comment(comment):
    msg = comment.body
    print msg
    print "-------------"


reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("BitcoinMarkets")
skip_first = 0
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
