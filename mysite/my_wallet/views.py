from django.shortcuts import render
from .models import Stock, Transaction
from. serializers import  StockSerializer, TransactionSerializer, InvestorSerializer
from accounts.models import Investor

#from  mysite.accounts.models import Investor
from django.http import JsonResponse
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse


@csrf_exempt
def investor_list(request):
     if request.method == 'GET':
          investors = Investor.objects.all()
          serializer = InvestorSerializer(investors, many=True, context={'request': request})
          return JsonResponse(serializer.data, safe=False)
     elif request.method == 'POST':
          data = JSONParser().parse(request)
          serializer = InvestorSerializer(data=data)
          if serializer.is_valid():
               serializer.save()
               return JsonResponse(serializer.data, status=201)
          return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def investor_detail(request, pk):
     try:
          investor = Investor.objects.get(pk=pk)
     except Investor.DoesNotExist:
        return HttpResponse(status=404)

     if request.method == 'GET':
        serializer = InvestorSerializer(investor)
        return JsonResponse(serializer.data)

     elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InvestorSerializer(investor, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)   

     elif request.method == 'DELETE':
        investor.delete()
        return HttpResponse(status=204)  

@csrf_exempt
def stock_list(request):
     if request.method == 'GET':
          stocks = Stock.objects.all()
          serializer = StockSerializer(stocks, many=True, context={'request': request})
          return JsonResponse(serializer.data, safe=False)
     elif request.method == 'POST':
          data = JSONParser().parse(request)
          serializer = StockSerializer(data=data)
          if serializer.is_valid():
               serializer.save()
               return JsonResponse(serializer.data, status=201)
          return JsonResponse(serializer.erros, status=400)

@csrf_exempt
def stock_detail(request, pk):
     try:
          stock = Stock.objects.get(pk=pk)
     except Stock.DoesNotExist:
        return HttpResponse(status=404)

     if request.method == 'GET':
        serializer = StockSerializer(stock)
        return JsonResponse(serializer.data)

     elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StockSerializer(stock, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erros, status=400)   

     elif request.method == 'DELETE':
        stock.delete()
        return HttpResponse(status=204)   

@csrf_exempt
def transaction_list(request):
     if request.method == 'GET':
          transactions = Transaction.objects.all()
          serializer = TransactionSerializer(transactions, many=True, context={'request': request})
          return JsonResponse(serializer.data, safe=False)
     elif request.method == 'POST':
          data = JSONParser().parse(request)
          serializer = TransactionSerializer(data=data)
          if serializer.is_valid():
               serializer.save()
               return JsonResponse(serializer.data, status=201)
          return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def transaction_detail(request, pk):
     try:
          transaction = Transaction.objects.get(pk=pk)
     except Stock.DoesNotExist:
        return HttpResponse(status=404)
        
     try:
          transaction = Transaction.objects.get(pk=pk)
     except Investor.DoesNotExist:
            return HttpResponse(status=404)


     if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

     elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)   

     elif request.method == 'DELETE':
        transaction.delete()
        return HttpResponse(status=204)    


@login_required
@api_view(['GET'])
def get_transactions_by_month_year(request, month, year):
    transactions = Transaction.objects.filter(date__month=month, date__year=year, user=request.user).order_by('date')
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def transacoes_investidor_stock(request, stock_code):
    investidor = request.user
    try:
        stock = Stock.objects.get(code=stock_code)
    except Stock.DoesNotExist:
        return JsonResponse({'message': 'Ação não encontrada'}, status=404)

    transactions = Transaction.objects.filter(user=investidor, stock=stock).order_by('date')

    resultados = []

    for transaction in transactions:
        resultado = {
            'user': transaction.user,
            'stock': transaction.stock_id,
            'code': transaction.code,
            'date': transaction.date,
            'value': float(transaction.value),
            'amount': transaction.amount,
            'brokerage': float(transaction.brokerage),
            'type': transaction.type,
            'preco_medio': float(transaction.preco_medio()),
            'lucro_prejuizo': float(transaction.lucro_prejuizo()),
            'taxa_b3': float(transaction.taxab3()),
            'total_value': float(transaction.total_value()),
            'total_taxas': float(transaction.total_taxas()),
            'total_final': float(transaction.total_final())
        }
        resultados.append(resultado)

    lucro_prejuizo_total = Transaction.objects.filter(user=investidor, stock=stock, type='V').aggregate(Sum('lucro_prejuizo'))['lucro_prejuizo__sum']

    data = {
        'transacoes': resultados,
        'lucro_prejuizo_total': lucro_prejuizo_total
    }
    return JsonResponse(data)


@login_required
@api_view(['GET'])
def user_posicao(request):
    user = request.user

    positions = Transaction.objects.filter(user=user).values('stock').annotate(quant=Sum('amount'), preco_medio=Sum(F('amount')*F('value'))/Sum('amount'),valor_tot=F('amount')* F('value'))

    posicoes_tot = []
    lucro_prejuizo_tot = 0

    for position in positions:
        stock = Stock.objects.get(pk=position['stock'])
        lucro_prejuizo = stock.preco_medio()*position['quant'] - position['valor_tot']

    posicao_tot = {
         'stock': stock.code,
         'quantidade': position['quant'],
         'preco_medio': float(position['preco_medio']),
         'valor_total': float(position['valor_tot']),
         'lucro_prejuizo': float(lucro_prejuizo)
     }
    
    posicoes_tot.append(posicao_tot)
    lucro_prejuizo_tot += lucro_prejuizo

    wallet = {
        'posicoes': posicao_tot,
        'lucro_prjuizo_total': float(lucro_prejuizo_tot)
    }

    return JsonResponse(wallet)


