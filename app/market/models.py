from decimal import Decimal

from core.utils.models import SingletonModel, TimeStampModel
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


class FakeUser(TimeStampModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bank(SingletonModel):
    amount = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
    profit = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)


class Market(TimeStampModel):
    name = models.CharField(max_length=255, default='')
    condition_statement = models.TextField(default='')
    outcome = models.BooleanField(null=True, blank=True)
    price_for_position_a = models.DecimalField(default=0.00,
                                               max_digits=60,
                                               decimal_places=2)

    price_for_position_b = models.DecimalField(default=0.00,
                                               max_digits=60,
                                               decimal_places=2)

    def update_prices(self):
        total_pooled_amount_a = sum(
            bet.bet_amount for bet in self.bets.filter(position_for='a'))
        total_pooled_amount_b = sum(
            bet.bet_amount for bet in self.bets.filter(position_for='b'))

        if total_pooled_amount_a == 0 or total_pooled_amount_b == 0:
            # Handle the case where there are no bets on one side
            pass
            # Reset prices to default or a preferred value
            # self.price_for_position_a = Decimal('0.00')
            # self.price_for_position_b = Decimal('0.00')
        else:
            # Calculate ratios and update prices
            total_ratio = total_pooled_amount_a / total_pooled_amount_b

            # You can choose a constant or a formula to calculate prices
            # based on the ratios and your desired logic
            new_price_for_position_a = self.price_for_position_a * total_ratio
            new_price_for_position_b = self.price_for_position_b * total_ratio

            self.price_for_position_a = new_price_for_position_a
            self.price_for_position_b = new_price_for_position_b

        self.save()


class Bet(TimeStampModel):
    user = models.ForeignKey(FakeUser, on_delete=models.CASCADE)
    market = models.ForeignKey(Market,
                               on_delete=models.CASCADE,
                               related_name='bets')

    position_for = models.CharField(max_length=1,
                                    choices=[('a', 'A'), ('b', 'B')])
    positions = models.PositiveBigIntegerField(default=1)
    bet_amount = models.DecimalField(default=0.00,
                                     max_digits=60,
                                     decimal_places=2)
    paid_amount = models.DecimalField(default=0.00,
                                      max_digits=60,
                                      decimal_places=2)


@receiver(post_save, sender=Bet)
def update_market_prices(sender, instance, **kwargs):
    instance.market.update_prices()


class Transaction(TimeStampModel):
    user = models.ForeignKey(FakeUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    market = models.ForeignKey(Market,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    amount = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
    fee = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
