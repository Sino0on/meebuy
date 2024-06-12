from django.urls import path
from . import views

urlpatterns = [
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/<int:pk>/', views.budget_detail, name='budget_detail'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
]
