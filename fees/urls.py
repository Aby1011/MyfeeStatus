from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fee_list, name='list'),
    path('structure/', views.fee_structure_list, name='structure_list'),
    path('structure/create/', views.fee_structure_create, name='structure_create'),
    path('structure/<int:pk>/edit/', views.fee_structure_edit, name='structure_edit'),
    path('structure/<int:pk>/delete/', views.fee_structure_delete, name='structure_delete'),
    path('assign/', views.assign_fees, name='assign'),
    path('student/<int:student_id>/', views.student_fee_detail, name='student_detail'),
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/create/', views.create_reminder, name='create_reminder'),
    path('overdue/', views.overdue_fees, name='overdue'),
]
