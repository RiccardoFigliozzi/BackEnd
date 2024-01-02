from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Product, OrderDetail
from django.conf import settings
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
from .forms import ProductForm, UserRegistrationForm
from django.db.models import Sum
import datetime
# Create your views here.


def index(req):
    products = Product.objects.all()

    return render(req, 'index.html', {"products": products})


def detail(req, id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(req, 'detail.html', {"product": product, "stripe_publishable_key": stripe_publishable_key})


@csrf_exempt
def create_checkout_session(req, id):
    request_data = json.loads(req.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name
                    },
                    'unit_amount': int(product.price) * 100
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=req.build_absolute_uri(reverse('success')) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=req.build_absolute_uri(reverse('failed')),
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price)
    order.save()

    return JsonResponse({'sessionId': checkout_session.id})


def payment_success_view(req):
    session_id = req.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(
        OrderDetail, stripe_payment_intent=session.payment_intent)
    order.has_paid = True
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount = product.total_sales_amount + int(product.price)
    product.total_sales += 1
    order.save()
    return render(req, 'payment_success.html', {'order': order})


def payment_failed_view(req):
    return render(req, 'payment_failed.html')


def create_product(req):
    if req.method == 'POST':
        product_form = ProductForm(req.POST, req.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.seller = req.user
            new_product.save()
            return redirect('index')
    product_form = ProductForm()
    return render(req, 'create_product.html', {'product_form': product_form})


def product_edit(req, id):
    product = Product.objects.get(id=id)
    if product.seller != req.user:
        return redirect('invalid')
    product_form = ProductForm(
        req.POST or None, req.FILES or None, instance=product)
    if req.method == 'POST':
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(req, 'product_edit.html', {'product_form': product_form, 'product': product})


def product_delete(req, id):
    product = Product.objects.get(id=id)
    if product.seller != req.user:
        return redirect('invalid')
    if req.method == 'POST':
        if product.delete():
            return redirect('index')
    return render(req, 'product_delete.html', {'product': product})


def dashboard(req):
    products = Product.objects.filter(seller=req.user)
    return render(req, 'dashboard.html', {'products': products})


def register(req):
    if req.method == 'POST':
        user_form = UserRegistrationForm(req.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form = UserRegistrationForm(req.POST)
    return render(req, 'register.html', {'user_form': user_form})

def invalid(req):
    return render(req, 'invalid.html')

def my_purchases(req):
    orders = OrderDetail.objects.filter(customer_email=req.user.email)
    return render(req, 'purchases.html', {'orders':orders})

def sales(req):
    orders = OrderDetail.objects.filter(product__seller=req.user)
    total_sales = orders.aggregate(Sum('amount'))
    
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = OrderDetail.objects.filter(product__seller=req.user, created_on__gt = last_year)
    yearly_sales = data.aggregate(Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = OrderDetail.objects.filter(product__seller=req.user, created_on__gt = last_month)
    monthly_sales = data.aggregate(Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = OrderDetail.objects.filter(product__seller=req.user, created_on__gt = last_week)
    weekly_sales = data.aggregate(Sum('amount'))

    daily_sales_sums = OrderDetail.objects.filter(product__seller=req.user).values('created_on__date').order_by('created_on__date').annotate(sum=(Sum('amount')))
    product_sales_sums = OrderDetail.objects.filter(product__seller=req.user).values('product__name').order_by('product__name').annotate(sum=(Sum('amount')))
    return render(req, 'sales.html', {'total_sales':total_sales, 'yearly_sales':yearly_sales, 'monthly_sales':monthly_sales, 'weekly_sales':weekly_sales, 'daily_sales_sums':daily_sales_sums, 'product_sales_sums':product_sales_sums})