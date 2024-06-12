from django.contrib import admin
from .models import Budget, Income, Expense, Employee, Salary

admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Employee)
admin.site.register(Salary)
