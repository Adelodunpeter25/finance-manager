from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
import csv
from .models import Category, Transaction, Budget, Notification
from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer, NotificationSerializer
from .filters import TransactionFilter

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['name', 'type', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        transactions = Transaction.objects.filter(
            user=request.user,
            category__in=queryset
        ).values('category__name', 'category__type').annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        ).order_by('-total_amount')
        
        return Response(transactions)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilter
    ordering_fields = ['amount', 'date', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        total_income = queryset.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = queryset.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance = total_income - total_expenses
        
        # Monthly breakdown
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            income=Sum('amount', filter=Q(type='income')),
            expenses=Sum('amount', filter=Q(type='expense'))
        ).order_by('month')
        
        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'monthly_breakdown': monthly_data
        })
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
        
        for transaction in queryset:
            writer.writerow([
                transaction.date,
                transaction.type,
                transaction.category.name if transaction.category else '',
                transaction.amount,
                transaction.description
            ])
        
        return response

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['amount', 'start_date', 'end_date']
    ordering = ['-start_date']
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related('category')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        budget = self.get_object()
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            type='expense',
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        remaining = budget.amount - spent
        percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
        
        return Response({
            'budget_amount': budget.amount,
            'spent_amount': spent,
            'remaining_amount': remaining,
            'percentage_used': round(percentage_used, 2),
            'is_exceeded': spent > budget.amount
        })

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})
    
    @action(detail=False, methods=['patch'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all notifications marked as read'})
