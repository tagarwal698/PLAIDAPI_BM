from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='plaid-home'),
    
    path('get_access_token/', views.ExchangeAccessToken.as_view()),
    path('get_public_token/', views.PublicTokenCreate.as_view()),
    path('get_transactions/', views.GetTransactions.as_view()),
    path('get_identity/',views.GetIdentity.as_view()),
    path('get_account_balance/', views.GetBalance.as_view()),
    path('webhook_transactions/', views.WebHookTransaction.as_view())
]