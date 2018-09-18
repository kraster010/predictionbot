# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from .models import Prediction


class PredictionView(ListView):
    model = Prediction
    paginate_by = 100  # if pagination is desired
    template_name = "pbot/prediction.html"
