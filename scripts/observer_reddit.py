import logging
from datetime import datetime

import praw

from bot import PredictionParser, CoinMarketCap
from pbot.models import Prediction
from coinmarketcap import Market

logger = logging.getLogger('PredictionBot')


# registered_date = models.DateField(auto_now=True)
# registered_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
# prediction_type = models.CharField(max_length=10, choices=PREDICTION_TYPES, default="at")
# target_date = models.DateField(auto_now=True)
# target_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

def run():
    try:
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit("BitcoinMarkets")
    except:
        print "reddit connection not working"
        return None

    cmk = CoinMarketCap()
    pp = PredictionParser()

    for comment in subreddit.stream.comments():
        msg = comment.body
        msg_permalink = "https://www.reddit.com/" + comment.permalink
        print msg
        print msg_permalink
        print "-" * 50
        try:
            ret = pp.parse_message(msg)
            if not ret:
                continue

        except Exception:
            continue

        cond, price, date = ret

        try:
            pred = Prediction.objects.create(registered_price=cmk.get_price(), prediction_type=cond, target_date=date,
                                             target_price=price, permalink=msg_permalink)

            print "created prediction with:\n"
            print "condition: %s" % cond
            print "price: %s" % price
            print "when: %s" % date
            print "btc actual price: %d" % pred.registered_price
        except:
            print "exception"
            pass
