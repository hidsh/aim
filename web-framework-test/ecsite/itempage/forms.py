# -*- coding: utf-8 -*-
from django import forms

class ItemSearchForm(forms.Form):
    item_name = forms.CharField()
