from django import forms
import datetime


class DateTweetForm(forms.Form):
    entity = forms.CharField(max_length=30)
    reputation_dimension = forms.CharField(max_length=30)
    date = forms.DateField(initial=datetime.date.today)

