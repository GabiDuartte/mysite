from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('investor-data/', views.investor_list, name='investor-data'),
    path('investor/<int:pk>/', views.investor_detail, name='add-investor'),
    path('accounts/pos-investor/', views.user_posicao, name='pos-investor'),
    path('stock-data/', views.stock_list, name='stock-data'),
    path('stock/<int:pk>/', views.stock_detail, name='stock-detail'),
    path('transaction-data/', views.transaction_list, name='transaction-data'),
    path('transaction/<int:pk>/', views.transaction_detail, name='add-transaction'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('my-wallet/transactions/<int:month>/<int:year>/', views.get_transactions_by_month_year, name='transactions_by_month_year'),
    path('transactions/<int:stock_code>/', views.transacoes_investidor_stock, name='transacoes')
]
