import django_filters
from .models import Transaction, Category

class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    type = django_filters.ChoiceFilter(choices=Transaction.TYPE_CHOICES)
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    
    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date', 'category', 'type', 'amount_min', 'amount_max']
