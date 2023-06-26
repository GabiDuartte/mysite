from django.shortcuts import render
from .models import Stock, Transaction
from. serializers import  StockSerializer, TransactionSerializer #InvestorSerializer
#from  mysite.accounts.models import Investor
from django.http import JsonResponse
from django.db.models import Sum

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from django.http import HttpResponse, JsonResponse
'''
@api_view(['GET'])
def getData2(request):
       investors = Investor.objects.all()
       serializer = InvestorSerializer(investors, many=True)
       return Response(serializer.data)

@api_view(['POST'])
def addInvestor(request):
       serializer = InvestorSerializer(data=request.data)
       if serializer.is_valid():
              serializer.save()
       return Response(serializer.data)
'''


@api_view(['GET'])
def getData(request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=Fa)

   
@api_view(['POST'])
def addStock(request):
        data = JSONParser().parse(request)
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
def getData1(request):
       transactions = Transaction.objects.all()
       serializer = TransactionSerializer(transactions, many=True)
       return Response(serializer.data)

@api_view(['POST'])
def addTransaction(request):
       serializer = TransactionSerializer(data=request.data)
       if serializer.is_valid():
              serializer.save()
       return Response(serializer.data)

@api_view(['PUT'])
def putStock(request, pk):
     try:
          stocks = Stock.objects.get(pk=pk)
     except Stock.DoesNotExist:
        return Response({'message': 'Transaction não encontrada'}, status=404)
     data = JSONParser().parse(request)
     serializer = StockSerializer(stocks, data=data)
     if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
     return JsonResponse(serializer.errors, status=400)

'''
@api_view(['PUT'])
def updateTransaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({'message': 'Transaction não encontrada'}, status=404)

    serializer = TransactionSerializer(transaction, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
'''

@api_view(['PATCH'])
def updateTransaction1(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({'message': 'Transação não encontrada'}, status=404)

    serializer = TransactionSerializer(transaction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteTransaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({'message': 'Transação não encontrada'}, status=404)

    transaction.delete()
    return Response({'message': 'Transação excluída com sucesso'}, status=204)


@api_view(['GET'])
def get_transactions_by_month_year(request, month, year):
    transactions = Transaction.objects.filter(date__month=month, date__year=year, user=request.user).order_by('date')
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)

'''
def transacoes_investidor_stock(request, codigo_stock):
    investidor = request.user
    try:
        stock = Stock.objects.get(code=codigo_stock)
    except Stock.DoesNotExist:
        return JsonResponse({'message': 'Ação não encontrada'}, status=404)

    transacoes = Transaction.objects.filter(user=investidor, stock=stock).order_by('date')

    resultados = []

    for transacao in transacoes:
        resultado = {
            'code': transacao.code,
            'date': transacao.date,
            'value': transacao.value,
            'amount': transacao.amount,
            'brokerage': transacao.brokerage,
            'type': transacao.type,
            'preco_medio': transacao.preco_medio(),
            'lucro_prejuizo': transacao.lucro_prejuizo()
        }
        resultados.append(resultado)

    lucro_prejuizo_total = Transaction.objects.filter(user=investidor, stock=stock, type='V').aggregate(Sum('lucro_prejuizo'))['lucro_prejuizo__sum']

    data = {
        'transacoes': resultados,
        'lucro_prejuizo_total': lucro_prejuizo_total
    }
    return JsonResponse(data)

'''
