from django.contrib import admin
from market.models import FakeUser, Bank, Market, Transaction, Bet

admin.site.register(FakeUser)

admin.site.register(Bank)
admin.site.register(Market)
admin.site.register(Transaction)
admin.site.register(Bet)
