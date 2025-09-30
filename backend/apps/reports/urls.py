from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_data, name='report_data'),
    path('export/', views.export_transactions, name='export_transactions'),
]
