from django import forms
from .models import FakeUser, Market, Bet


class FakeUserForm(forms.ModelForm):

    class Meta:
        model = FakeUser
        fields = ['name']


class MarketForm(forms.ModelForm):

    class Meta:
        model = Market
        fields = [
            'name', 'condition_statement', 'price_for_position_a',
            'price_for_position_b'
        ]


class BetForm(forms.ModelForm):

    class Meta:
        model = Bet
        fields = ['user', 'position_for', 'positions']
