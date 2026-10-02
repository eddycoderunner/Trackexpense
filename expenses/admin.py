from django.contrib import admin
from .models import Expense, Category

@admin.register(Category)
class CategortyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'user', 'created_at')
    list_filter = ('user', 'category', 'created_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'