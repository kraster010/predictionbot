# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djmoney.models.fields import MoneyField


class Prediction(models.Model):
    PREDICTION_TYPES = (
        ("at", "At"),
        ("above", "Above"),
        ("lower", "Lower"),
    )
    registered_date = models.DateField(auto_now=True)
    registered_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    prediction_type = models.CharField(max_length=10, choices=PREDICTION_TYPES, default="at")
    target_date = models.DateField(auto_now=True)
    target_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

