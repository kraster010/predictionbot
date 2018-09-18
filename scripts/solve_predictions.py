from datetime import datetime

from pbot.models import Prediction
from coinmarketcap import Market


# registered_date = models.DateField(auto_now=True)
# registered_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
# prediction_type = models.CharField(max_length=10, choices=PREDICTION_TYPES, default="at")
# target_date = models.DateField(auto_now=True)
# target_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

def run():
    qs = Prediction.objects.all()
    for p in qs:
        print p
