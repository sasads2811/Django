from django import forms
from dashboard.models import ScoreRecord


class FilterForm(forms.Form):
    year_choices = [
        ('2020', '2020'),
        ('2021', '2021'),
    ]
    province_choices = [(province, province) for province in
                        ScoreRecord.objects.values_list('province', flat=True).distinct()]

    year = forms.ChoiceField(choices=year_choices, required=True, label='Year')
    province = forms.ChoiceField(choices=[('', 'Select Province')] + province_choices, required=False, label='Province')


class FilterFormOnlyYear(forms.Form):
    year_choices = [
        ('2020', '2020'),
        ('2021', '2021'),
    ]

    year = forms.ChoiceField(choices=year_choices, required=True, label='Year')
