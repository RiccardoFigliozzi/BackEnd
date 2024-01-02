from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
# Create your views here.

def index(req):

    if req.method == "POST":
        expense = ExpenseForm(req.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expense.objects.all()
    tot_amount = expenses.aggregate(Sum('amount'))

    # calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sum = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sum = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    res = render(req, "myapp/index.html", {'expense_form':expense_form, 'expenses':expenses, 'total_amount': tot_amount, 'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum, 'daily_sum':daily_sum, 'categorical_sum':categorical_sum })
    return res

def edit(req, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if req.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(req.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(req, 'myapp/edit.html', {'expense_form':expense_form})

def delete(req, id):
    if req.method == "POST" and 'delete' in req.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()

    return redirect('index')