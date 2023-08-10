from django.shortcuts import render, get_object_or_404, redirect
from .models import Bet, Market  # Assuming you have a Market model
from .forms import BetForm, FakeUserForm, MarketForm
from decimal import Decimal


def market_detail(request, market_id):
    if request.method == 'POST':
        bet_form = BetForm(request.POST)
        if bet_form.is_valid():
            new_bet = bet_form.save(commit=False)
            market = Market.objects.get(id=market_id)
            new_bet.market = market
            new_bet.bet_amount = getattr(
                market, f'price_for_position_{new_bet.position_for}'
            ) * new_bet.positions
            new_bet.paid_amount = (new_bet.bet_amount +
                                   new_bet.bet_amount * Decimal('0.05'))
            new_bet.save()
            return redirect(f'/markets/{market_id}/', bet_id=new_bet.id
                            )  # Redirect to the detail view of the created bet
    else:
        bet_form = BetForm()
    market = get_object_or_404(Market, id=market_id)
    context = {
        'market': market,
        'bets_for': market.bets.filter(position_for='a').order_by('-id'),
        'bets_against': market.bets.filter(position_for='b').order_by('-id'),
        'bet_form': BetForm
    }
    return render(request, 'market.html', context)


def get_bets(request, market_id):
    user = request.GET.get('user', None)
    bets = Bet.objects.filter(market__id=market_id)
    if user:
        bets = bets.filter(user__id=user)


def create_market(request):
    if request.method == 'POST':
        market_form = MarketForm(request.POST)
        if market_form.is_valid():
            market_form.save()
            return redirect(
                '/')  # Redirect to the detail view of the created market
    else:
        market_form = MarketForm()
    context = {'market_form': MarketForm}
    return render(request, 'create_market.html', context)


def create_user(request):
    if request.method == 'POST':
        fake_user_form = FakeUserForm(request.POST)
        if fake_user_form.is_valid():
            fake_user_form.save()
            return redirect(
                '/')  # Redirect to the detail view of the created market
    else:
        fake_user_form = FakeUserForm()
    context = {'fake_user_form': FakeUserForm}
    return render(request, 'fake_user_create.html', context)
