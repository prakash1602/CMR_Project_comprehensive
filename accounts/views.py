from django.shortcuts import render, redirect
from .models import Customer, Product, Order
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unathenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unathenticated_user
def register_page(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return redirect('login')
    return render(request, 'accounts/register.html', context)


@unathenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    product = Product.objects.all()
    order = Order.objects.all()

    total_orders = len(order)
    pending_orders = order.filter(status='Pending').count()
    delivered_order = order.filter(status='Delivered').count()
    out_for_delivery = order.filter(status='OutForDelivery').count()

    context = {
        'customers': customers,
        'product': product,
        'order': order,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_order': delivered_order,
        'out_for_delivery': out_for_delivery
    }
    return render(request, 'accounts/dashboard.html', context)


# @login_required(login_url='login')
def user_page(request):
    return render(request, 'accounts/user.html')


# @login_required(login_url='login')
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, "accounts/orders.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    total_orders = len(orders)
    pending_orders = orders.filter(status='Pending').count()
    delivered_order = orders.filter(status='Delivered').count()
    out_for_delivery = orders.filter(status='OutForDelivery').count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_order': delivered_order,
        'out_for_delivery': out_for_delivery
    }

    return render(request, 'customer.html', context)

# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')


# def login_page(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.info(request, 'Username or Password is incorrect')
#         return render(request, 'accounts/login.html')


# def logoutUser(request):
#     logout(request)
#     return redirect('login')


# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')

# def products(request):
#     products = Product.objects.all()
#     order = Order.objects.all()
#     context = {'products': products, 'order': order}
#     return render(request, 'accounts/products.html', context)


# def orders(request):
#     orders = Order.objects.all()
#     context = {'orders': orders}
#     return render(request, 'accounts/orders.html', context)


# def customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     orders = customer.order_set.all()
#
#     total_orders = len(orders)
#     pending_orders = orders.filter(status='Pending').count()
#     delivered_order = orders.filter(status='Delivered').count()
#     out_for_delivery = orders.filter(status='OutForDelivery').count()
#
#     context = {
#         'customer': customer,
#         # 'product': product,
#         'orders': orders,
#         'total_orders': total_orders,
#         'pending_orders': pending_orders,
#         'delivered_order': delivered_order,
#         'out_for_delivery': out_for_delivery
#     }
#
#     return render(request, 'customer.html', context)

# def register_page(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = CreateUserForm()
#         context = {'form': form}
#         if request.method == "POST":
#           form = CreateUserForm(request.POST)
#           if form.is_valid():
#             form.save()
#             return redirect('login')
#         return render(request, 'accounts/register.html', context)

# def login_page(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Username or Password is incorrect')
#
#     return render(request, 'accounts/login.html')
