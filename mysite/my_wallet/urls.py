from django.urls import path
from . import views


urlpatterns = [
    #path('investor-data/', views.getData2, name='investor-data'),
    #path('add-investor/', views.addInvestor, name='add-investor'),
    path('stock-data/', views.getData, name='stock-data'),
    path('add-stock/', views.addStock, name='add-stock'),
    path('transaction-data/', views.getData1, name='transaction-data'),
    path('add-transaction/', views.addTransaction, name='add-transaction'),
    #path('update-transaction/', views.updateTransaction, name='update-transaction'),
    path('patch-transaction/', views.updateTransaction1, name='patch-transaction'),
    path('delete-transaction/', views.deleteTransaction, name='delete-transaction' ),
    path('transactions/<int:month>/<int:year>/', views.get_transactions_by_month_year, name='transactions_by_month_year'),
    path('stock-put/', views.putStock, name='stock-put')
]