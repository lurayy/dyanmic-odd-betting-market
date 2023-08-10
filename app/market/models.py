from django.forms import ValidationError
from core.utils.models import SingletonModel, TimeStampModel
from django.db import models
from django.db.models.signals import post_save, pre_save
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
    minimum_price_for_position = models.DecimalField(default=0.00,
                                                     max_digits=60,
                                                     decimal_places=2)
    celling_price = models.DecimalField(default=0.00,
                                        max_digits=60,
                                        decimal_places=2)
    pool_amount_a = models.DecimalField(default=0.00,
                                        max_digits=60,
                                        decimal_places=2)
    pool_amount_b = models.DecimalField(default=0.00,
                                        max_digits=60,
                                        decimal_places=2)
    is_closed = models.BooleanField(default=False)

    def update_prices(self, amount, position_for):
        setattr(self, f'pool_amount_{position_for}',
                getattr(self, f'pool_amount_{position_for}') + amount)
        self.save()
        # Ensure pool_amount_a and pool_amount_b are greater than zero
        if self.pool_amount_a <= 0 and self.pool_amount_b <= 0:
            return
        elif self.pool_amount_a <= 0:
            # Update the price fields
            self.price_for_position_a = self.minimum_price_for_position
            self.price_for_position_b = (self.celling_price -
                                         self.minimum_price_for_position)
            self.save()
            return
        elif self.pool_amount_b <= 0:
            self.price_for_position_a = (self.celling_price -
                                         self.minimum_price_for_position)
            self.price_for_position_b = self.minimum_price_for_position
            self.save()
            return

        # Calculate the ratio of pool_amount_a and pool_amount_b
        ratio_a = self.pool_amount_a / (self.pool_amount_a +
                                        self.pool_amount_b)
        ratio_b = self.pool_amount_b / (self.pool_amount_a +
                                        self.pool_amount_b)

        # Distribute the ceiling price based on the ratios
        # price_for_position_a = self.celling_price * ratio_a
        # price_for_position_b = self.celling_price * ratio_b
        price_for_position_a = self.minimum_price_for_position + (
            self.celling_price - self.minimum_price_for_position) * ratio_a
        price_for_position_b = self.minimum_price_for_position + (
            self.celling_price - self.minimum_price_for_position) * ratio_b

        # Update the price fields
        self.price_for_position_a = price_for_position_a
        self.price_for_position_b = price_for_position_b
        self.save()

    def close_up_market():
        pass


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


@receiver(pre_save, sender=Bet)
def handle_pre_save(sender, instance, **kwargs):
    if instance.market.is_closed:
        raise ValidationError('Cannot bet on closed Market.')


@receiver(post_save, sender=Bet)
def update_market_prices(sender, instance, **kwargs):
    instance.market.update_prices(instance.bet_amount, instance.position_for)


class Transaction(TimeStampModel):
    user = models.ForeignKey(FakeUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    market = models.ForeignKey(Market,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    amount = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
    fee = models.DecimalField(default=0.00, max_digits=60, decimal_places=2)
