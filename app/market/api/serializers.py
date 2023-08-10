from rest_framework import serializers

from market.models import Bank, Bet, FakeUser, Market, Transaction


class FakeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FakeUser
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market
        fields = '__all__'


class BetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bet
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'
