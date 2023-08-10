# Generated by Django 4.1.5 on 2023-08-10 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FakeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('condition_statement', models.TextField(default='')),
                ('outcome', models.BooleanField(blank=True, null=True)),
                ('price_for_position_a', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('price_for_position_b', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('minimum_price_for_position', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('celling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('pool_amount_a', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('pool_amount_b', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.market')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.fakeuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position_for', models.CharField(choices=[('a', 'A'), ('b', 'B')], max_length=1)),
                ('positions', models.PositiveBigIntegerField(default=1)),
                ('bet_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=60)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='market.market')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.fakeuser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
