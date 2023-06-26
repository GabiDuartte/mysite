from django.urls import path
from . import views


urlpatterns = [
    #path('investor-data/', views.getData2, name='investor-data'),
    #path('add-investor/', views.addInvestor, name='add-investor'),
    path('stock-data/', views.stock_list, name='stock-data'),
    path('stock/<int:pk>/', views.stock_detail, name='stock-detail'),
    path('transaction-data/', views.transaction_list, name='transaction-data'),
    path('transaction/<int:pk>/', views.transaction_detail, name='add-transaction'),
   
    path('transactions/<int:month>/<int:year>/', views.get_transactions_by_month_year, name='transactions_by_month_year'),
]