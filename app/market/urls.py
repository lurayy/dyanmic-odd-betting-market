from django.urls import path, include
from market.api.market import (FakeUserAPI, BankAPI, MarketAPI, TransactionAPI,
                               BetAPI)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('bank', BankAPI)

router.register('users', FakeUserAPI)

router.register('transactions', TransactionAPI)

router.register('bets', BetAPI)

router.register('', MarketAPI)

urlpatterns = [
    path('', include(router.urls)),
]
