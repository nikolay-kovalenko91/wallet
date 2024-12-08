from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = JsonApiPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["label"]
    ordering_fields = ["balance"]


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = JsonApiPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["wallet"]
    ordering_fields = ["amount", "txid"]
