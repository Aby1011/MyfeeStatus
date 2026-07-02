from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('pay/<int:fee_id>/', views.make_payment, name='make_payment'),
    path('process/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='receipt'),
    path('history/', views.payment_history, name='history'),
    path('pending/', views.pending_payments, name='pending'),
]
