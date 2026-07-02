from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('finance/', views.finance_dashboard, name='finance'),
    path('student/', views.student_dashboard, name='student'),
]
