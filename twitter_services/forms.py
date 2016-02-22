from django import forms
import datetime


class DateTweetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        entity = kwargs.pop('entity')
        reputation_dimension = kwargs.pop('reputation_dimension')
        super(DateTweetForm, self).__init__(*args, **kwargs)
        self.fields['entity'].initial = entity
        self.fields['reputation_dimension'].initial = reputation_dimension

    entity = forms.CharField(max_length=30, widget=forms.HiddenInput)
    reputation_dimension = forms.CharField(max_length=30, required=False, widget=forms.HiddenInput)
    date = forms.DateField(initial=datetime.date.today)

