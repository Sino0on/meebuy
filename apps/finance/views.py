from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Budget, Income, Expense, Employee, Salary

def budget_list(request):
    budgets = Budget.objects.all()
    employees = Employee.objects.all()
    return render(request, 'finance/budget_list.html', {'budgets': budgets, 'employees': employees})

def budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    incomes = budget.incomes.all()
    expenses = budget.expenses.all()
    return render(request, 'finance/budget_detail.html', {
        'budget': budget,
        'incomes': incomes,
        'expenses': expenses,
        'total_income': budget.incomes.aggregate(total=Sum('amount'))['total'],
        'total_expense': budget.expenses.aggregate(total=Sum('amount'))['total']
    })


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'finance/employee_list.html', {'employees': employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    salaries = employee.salaries.all()
    return render(request, 'finance/employee_detail.html', {
        'employee': employee,
        'salaries': salaries,
        'total_salaries': salaries.aggregate(total=Sum('amount'))['total'],
    })
