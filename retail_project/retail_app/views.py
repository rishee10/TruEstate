from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all().order_by("-id")
    serializer_class = SaleSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]

    # ✅ ONLY REAL DATABASE FIELDS ARE ALLOWED HERE
    filterset_fields = {
        "order_status": ["exact"],
        "payment_method": ["exact"],
        "customer__region": ["exact"],     # ✅ FIXED
        "customer__customer_type": ["exact"],  # ✅ FIXED
        "product__category": ["exact"],    # ✅ FIXED
        "product__brand": ["exact"],       # ✅ OPTIONAL
    }

    search_fields = [
        "transaction_id",
        "customer__name",
        "product__name",
    ]


