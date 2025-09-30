from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
from .models import Transaction, Budget, Notification

@receiver(post_save, sender=Transaction)
def check_budget_on_transaction(sender, instance, created, **kwargs):
    if created and instance.type == 'expense' and instance.category:
        # Check for active budgets for this category
        budgets = Budget.objects.filter(
            user=instance.user,
            category=instance.category,
            start_date__lte=instance.date,
            end_date__gte=instance.date
        )
        
        for budget in budgets:
            # Calculate total spent in budget period
            spent = Transaction.objects.filter(
                user=instance.user,
                category=budget.category,
                type='expense',
                date__gte=budget.start_date,
                date__lte=budget.end_date
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
            
            # Budget exceeded notification
            if spent > budget.amount:
                Notification.objects.create(
                    user=instance.user,
                    type='budget_exceeded',
                    title='Budget Exceeded!',
                    message=f'Your budget for {budget.category.name} has been exceeded. '
                           f'Spent: ${spent}, Budget: ${budget.amount}'
                )
                
                # Send email notification
                if hasattr(settings, 'EMAIL_HOST') and instance.user.email:
                    send_mail(
                        'Budget Exceeded - Finance Manager',
                        f'Your budget for {budget.category.name} has been exceeded.',
                        settings.DEFAULT_FROM_EMAIL,
                        [instance.user.email],
                        fail_silently=True,
                    )
            
            # Budget warning at 80%
            elif percentage_used >= 80:
                # Check if warning already sent
                existing_warning = Notification.objects.filter(
                    user=instance.user,
                    type='budget_warning',
                    message__contains=budget.category.name,
                    created_at__gte=budget.start_date
                ).exists()
                
                if not existing_warning:
                    Notification.objects.create(
                        user=instance.user,
                        type='budget_warning',
                        title='Budget Warning',
                        message=f'You have used {percentage_used:.1f}% of your budget for {budget.category.name}. '
                               f'Spent: ${spent}, Budget: ${budget.amount}'
                    )

@receiver(post_save, sender=Transaction)
def new_transaction_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            type='new_transaction',
            title='New Transaction Added',
            message=f'New {instance.type}: ${instance.amount} for {instance.category.name if instance.category else "No Category"}'
        )
