from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from tracker.models import Transaction, Budget

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    # Calculate totals
    total_income = Transaction.objects.filter(
        user=user, 
        type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(
        user=user, 
        type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    net_balance = total_income - total_expenses
    
    # Calculate budget utilization
    budgets = Budget.objects.filter(user=user)
    total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    
    budget_utilization = 0
    if total_budget > 0:
        budget_utilization = round((float(total_expenses) / float(total_budget)) * 100, 1)
    
    return Response({
        'totalIncome': float(total_income),
        'totalExpenses': float(total_expenses),
        'netBalance': float(net_balance),
        'budgetUtilization': budget_utilization
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_transactions(request):
    user = request.user
    
    transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
    
    data = []
    for transaction in transactions:
        data.append({
            'id': transaction.id,
            'amount': float(transaction.amount),
            'type': transaction.type,
            'category': transaction.category.name if transaction.category else 'Uncategorized',
            'date': transaction.date.strftime('%Y-%m-%d'),
            'description': transaction.description
        })
    
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
