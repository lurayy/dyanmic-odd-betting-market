from core.utils.viewsets import DefaultViewSet
from market.api.serializers import (BankSerializer, BetSerializer,
                                    FakeUserSerializer, MarketSerializer)
from market.models import (Bank, Bet, FakeUser, Market, Transaction)


class FakeUserAPI(DefaultViewSet):
    serializer_class = FakeUserSerializer
    search_field = ['name']
    queryset = FakeUser.objects.filter()


class BankAPI(DefaultViewSet):
    serializer_class = BankSerializer
    queryset = Bank.objects.filter()


class MarketAPI(DefaultViewSet):
    serializer_class = MarketSerializer
    search_field = ['name', 'condition_statement']
    queryset = Market.objects.filter()


class TransactionAPI(DefaultViewSet):
    serializer_class = Transaction
    search_field = ['action']
    queryset = Transaction.objects.filter()


class BetAPI(DefaultViewSet):
    serializer_class = BetSerializer
    queryset = Bet.objects.filter()
