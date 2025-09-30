from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from tracker.models import Budget, Transaction
from .serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
