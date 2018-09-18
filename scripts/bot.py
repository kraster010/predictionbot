from parse import *
import logging
from datetime import datetime
from parse import compile
from coinmarketcap import Market

logger = logging.getLogger('PredictionBot')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# !prediction < (PRICE) DATE
# !prediction > (PRICE) DATE
# !prediction less (PRICE) DATE
# !prediction greater (PRICE) DATE
# !prediction above (PRICE) DATE
# !prediction below (PRICE) DATE
# !prediction at (PRICE) DATE

# DATE -> 21/03/1989 or 1989/03/21

class PredictionParser:
    @classmethod
    @with_pattern(r'0*\d{4}')
    def parse_year(cls, text):
        text = text.lstrip("0")
        return int(text)

    @classmethod
    @with_pattern(r'0*\d\d?')
    def parse_day_month(cls, text):
        text = text.lstrip("0")
        return int(text)

    @classmethod
    @with_pattern(
        r'(0*\d\d?|(september|october|november|december|january|febraury|march|april|may|june|july|august))\s+0*\d{4}')
    def parse_verbose(cls, text):
        temp = [x.strip() for x in text.lstrip("0").split() if x]
        return {"month": temp[0], "year": temp[1]}

    @classmethod
    @with_pattern(r'(@|at|above|below|less|greater|>|<)')
    def parse_condition(cls, text):
        return text

    def __init__(self):
        self.MONTHS = ["january", "febraury", "march", "april", "may", "june", "july", "august", "september", "october",
                       "november", "dicember"]

        year = "{year:^ty}"
        month = "{month:^td}"
        month_verbose = "{monthv:^tdv}"
        day = "{day:^td}"
        delim = ["-", "/"]
        price = "{price:^g}"
        cond = "{cond:^cs}"
        format_date = [year + d + month + d + day for d in delim] + \
                      [day + d + month + d + year for d in delim] + \
                      [month + d + year for d in delim] + \
                      [month_verbose]
        extra_types_date = dict(ty=self.parse_year, td=self.parse_day_month, tdv=self.parse_verbose)
        extra_types = dict(cs=self.parse_condition)
        self.format_date = [(compile(x, extra_types=extra_types_date), x) for x in format_date]
        self.format_price = compile(price)
        self.format_cond = compile(cond, extra_types=extra_types)

    def parse_message(self, text):
        price = self.format_price.search(text)
        if not price:
            return None
        price = price["price"]

        cond = self.format_cond.search(text)
        cond = cond["cond"] if cond else "at"
        if cond == "@":
            cond = "at"
        elif cond == "<":
            cond = "less"
        elif cond == ">":
            cond = "greater"

        res = None
        final_f = None
        for f, raw_f in self.format_date:
            res_temp = f.search(text)
            if not res_temp:
                continue
            res = res_temp
            final_f = f, raw_f
            break
        date = res
        if not date:
            return None

        date_parser, date_format = final_f
        if "monthv" in date_format:
            date = date["monthv"]
            temp = self.MONTHS.index(date["month"])
            if temp != -1:
                date["month"] = temp + 1

            datetime_object = datetime.strptime('{} {}'.format('%02d' % date["month"], date["year"]), '%m %Y')
        else:
            datetime_object = datetime.strptime(
                '{} {} {}'.format('%02d' % date["day"], '%02d' % date["month"], date["year"]), '%d %m %Y')

        return cond, price, datetime_object


class CoinMarketCap:

    def __init__(self):
        self.api = Market()
        self.last_price_update = None
        self._cache()
        if not self.last_price_update:
            raise Exception("Can't connect to coinmarketcap")

    def _cache(self):
        usd_btc_price = self.api.ticker(1)
        try:
            self.usd_btc_price = int(usd_btc_price["data"]["quotes"]["USD"]["price"])
            self.last_price_update = datetime.now()
        except:
            logger.exception("CoinMarketCap error while caching")

    def get_price(self):
        if (datetime.now() - self.last_price_update).seconds > 60:
            self._cache()
        return self.usd_btc_price
