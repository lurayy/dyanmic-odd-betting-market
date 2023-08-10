from django.urls import path
from . import views

urlpatterns = [
    path('<int:market_id>/', views.market_detail, name='market_detail'),
    path('create/', views.create_market, name='create_market'),
    path('users/create/', views.create_user, name='create_user')
]
