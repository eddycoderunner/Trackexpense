import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ExpenseForm, CategoryForm, RegisterForm
from .models import Expense, Category

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created succesfully! Welcome.")
            return redirect('expense-list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def expense_list(request):
    period = request.GET.get('period', 'daily')
    today = datetime.date.today()
    expenses = Expense.objects.filter(user=request.user)

    if period == 'monthly':
        expenses = expenses.filter(created_at__year=today.year, created_at__month=today.month)
        label = f"This Month ({today.strftime('%B %Y')})"
    elif period == 'annual':
        expenses = expenses.filter(created_at__year=today.year)
        label = f"This Year ({today.year})"
    else:
        period = 'daily'
        expenses = expenses.filter(created_at__date=today)
        label = f"Today ({today.strftime('%d %b %Y')})"

    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    category_totals = (
        expenses.values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    paginator = Paginator(expenses, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'total': total,
        'period': period,
        'label': label,
        'category_totals': category_totals,
    }
    return render(request, 'expenses/expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expenxe added successfully.")
            return redirect('expense-list')
        else:
            form = ExpenseForm(user=request.user)
        return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect('expense-list')
        else:
            form = ExpenseForm(instance=expense, user=request.user)
        return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense'})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted.")
        return redirect('expense-list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_vaid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Category added.")
            return redirect('category-list')
        else:
            form = CategoryForm()
        return render(request, 'expenses/category_form.html', {'form': form})

@login_required
def chart_data(request):
    period =request.GET.get('period', 'monthly')
    today = datetime.date.today()
    expenses = Expense.objects.filter(user=request.user)

    if period =='daily':
        expenses =expenses.filter(created_at__date=today)
    elif period == 'annual':
        expenses = expenses.filter(created_at__year=today.year)
    else:
        period = 'monthly'
        expenses = expenses.filter(created_at__year=today.year, created_at__month=today.month)

    data = (
        expenses.values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    labels = [d['category__name'] or 'Uncategorized' for d in data]
    totals = [float(d['total']) for d in data]
    return JsonResponse({'labels': labels, 'totals': totals})


            