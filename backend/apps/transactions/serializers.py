from rest_framework import serializers
from tracker.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'category_id', 'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        transaction = Transaction.objects.create(**validated_data)
        if category_id:
            from tracker.models import Category
            try:
                category = Category.objects.get(id=category_id, user=transaction.user)
                transaction.category = category
                transaction.save()
            except Category.DoesNotExist:
                pass
        return transaction
