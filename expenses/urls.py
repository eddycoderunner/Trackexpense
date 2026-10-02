from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense-list'),
    path('add/', views.add_expense, name='add-expense'),
    path('edit/<int:pk>/', views.delete_expense, name='delete-expense'),

    path('categories/', views.category_list, name='category-list'),
    path('categories/add/', views.add_category, name='add_category'),

    path('chart-data/', views.chart_data, name='chart-data'),
    path('register/', views.register, name='register'),
]