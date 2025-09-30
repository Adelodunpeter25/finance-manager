from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.dashboard_stats, name='dashboard_stats'),
    path('recent-transactions/', views.recent_transactions, name='recent_transactions'),
    path('budget-status/', views.budget_status, name='budget_status'),
]
