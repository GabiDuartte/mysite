from rest_framework import serializers
from .models import  Stock, Transaction
#from mysite.accounts.models import Investor

'''
class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'
'''

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

        def validate(self, attrs):
            code = attrs.get('code')
            if not code:
                raise serializers.ValidationError("O campo 'code' é obrigatório.")
            return attrs

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'