from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Prefetch
from django.core.cache import cache
from tracker.models import Transaction, Budget

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    cache_key = f"dashboard_stats_{user.id}"
    
    # Try to get from cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)
    
    # Calculate totals with single query
    income_sum = Transaction.objects.filter(user=user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_sum = Transaction.objects.filter(user=user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    
    net_balance = income_sum - expense_sum
    
    # Calculate budget utilization
    total_budget = Budget.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    budget_utilization = round((float(expense_sum) / float(total_budget)) * 100, 1) if total_budget > 0 else 0
    
    data = {
        'totalIncome': float(income_sum),
        'totalExpenses': float(expense_sum),
        'netBalance': float(net_balance),
        'budgetUtilization': budget_utilization
    }
    
    # Cache for 5 minutes
    cache.set(cache_key, data, 300)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_transactions(request):
    user = request.user
    
    transactions = Transaction.objects.filter(user=user).select_related('category').order_by('-date')[:5]
    
    data = [{
        'id': t.id,
        'amount': float(t.amount),
        'type': t.type,
        'category': t.category.name if t.category else 'Uncategorized',
        'date': t.date.strftime('%Y-%m-%d'),
        'description': t.description
    } for t in transactions]
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def budget_status(request):
    user = request.user
    
    budgets = Budget.objects.filter(user=user)
    
    data = []
    for budget in budgets:
        # Calculate spent amount for this budget's category within the budget period
        spent_amount = Transaction.objects.filter(
            user=user,
            category=budget.category,
            type='expense',
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate percentage
        percentage = (float(spent_amount) / float(budget.amount)) * 100 if budget.amount > 0 else 0
        
        data.append({
            'id': budget.id,
            'category': budget.category.name,
            'budgetAmount': float(budget.amount),
            'spentAmount': float(spent_amount),
            'percentage': round(percentage, 1)
        })
    
    return Response(data)
