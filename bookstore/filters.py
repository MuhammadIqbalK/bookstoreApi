from django_filters import rest_framework as filters
from .models import Transaction

class TransactionFilter(filters.FilterSet):
    # Rentang tanggal
    transaction_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = ['transaction_date']