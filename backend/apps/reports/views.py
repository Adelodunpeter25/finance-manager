import csv
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.db.models import Sum, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tracker.models import Transaction, Category

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_data(request):
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Default to last 3 months if no dates provided
    if not start_date:
        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Filter transactions by date range
    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Calculate totals
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expenses
    
    # Category breakdown
    category_breakdown = []
    categories = Category.objects.filter(user=user)
    
    for category in categories:
        amount = transactions.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
        if amount > 0:
            total_for_type = total_income if category.type == 'income' else total_expenses
            percentage = (float(amount) / float(total_for_type)) * 100 if total_for_type > 0 else 0
            category_breakdown.append({
                'category': category.name,
                'amount': float(amount),
                'percentage': round(percentage, 1),
                'type': category.type
            })
    
    # Monthly trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_transactions = transactions.filter(
            date__gte=month_start.date(),
            date__lte=month_end.date()
        )
        
        month_income = month_transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        month_expenses = month_transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        monthly_trends.append({
            'month': month_start.strftime('%b %Y'),
            'income': float(month_income),
            'expenses': float(month_expenses),
            'net': float(month_income - month_expenses)
        })
    
    monthly_trends.reverse()  # Show oldest to newest
    
    return Response({
        'totalIncome': float(total_income),
        'totalExpenses': float(total_expenses),
        'netBalance': float(net_balance),
        'categoryBreakdown': category_breakdown,
        'monthlyTrends': monthly_trends,
        'incomeVsExpenses': monthly_trends  # Same data for now
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_transactions(request):
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    transactions = Transaction.objects.filter(user=user)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Category', 'Type', 'Amount'])
    
    for transaction in transactions.order_by('-date'):
        writer.writerow([
            transaction.date,
            transaction.description,
            transaction.category.name if transaction.category else 'Uncategorized',
            transaction.type,
            transaction.amount
        ])
    
    return response
