from rest_framework import serializers
from django.db.models import Sum
from tracker.models import Budget, Transaction

class BudgetSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    spent_amount = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    period = serializers.CharField()

    class Meta:
        model = Budget
        fields = ['id', 'category', 'category_id', 'amount', 'period', 'start_date', 'end_date', 'spent_amount', 'percentage', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_spent_amount(self, obj):
        spent = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            type='expense',
            date__gte=obj.start_date,
            date__lte=obj.end_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return float(spent)

    def get_percentage(self, obj):
        spent_amount = self.get_spent_amount(obj)
        if obj.amount > 0:
            return round((spent_amount / float(obj.amount)) * 100, 1)
        return 0

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        from tracker.models import Category
        try:
            category = Category.objects.get(id=category_id, user=validated_data['user'])
            validated_data['category'] = category
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category not found")
        
        # Convert period string to timedelta for the model
        period_str = validated_data.pop('period', 'monthly')
        from datetime import timedelta
        if period_str == 'weekly':
            validated_data['period'] = timedelta(weeks=1)
        elif period_str == 'yearly':
            validated_data['period'] = timedelta(days=365)
        else:  # monthly
            validated_data['period'] = timedelta(days=30)
            
        return Budget.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert period back to string for frontend
        if instance.period.days == 7:
            data['period'] = 'weekly'
        elif instance.period.days >= 365:
            data['period'] = 'yearly'
        else:
            data['period'] = 'monthly'
        return data
