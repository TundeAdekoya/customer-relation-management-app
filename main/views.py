
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm  
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filter import OrderFilter
from .decorators import unauthenticated_user, allowed_user, admin_only

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm() 

    if request.method == 'POST':  
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account created successfully for ' + username)  
            return redirect('login')

    context = {'form':form}   

    return render(request, 'main/register.html', context=context)


@unauthenticated_user
def loginPage(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username OR password is incorrect')

        context = {}

        return render(request, 'main/login.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all() 
    customers = Customer.objects.all()

    total_customer = customers.count()
    
    total_order = orders.count()
    delivered = orders.filter(status = 'delivered').count()
    pending = orders.filter(status = 'pending').count()

    context = {
        'orders':orders, 
        'customers':customers,
        'total_order':total_order,
        'total_customer':total_customer,
        'delivered':delivered,
        'pending':pending,
    }

    return render(request, 'main/dashboard.html', context = context)



@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_order = orders.count()
    delivered = orders.filter(status = 'delivered').count()
    pending = orders.filter(status = 'pending').count()

    print('ORDERS:', orders)
    context = {
        'orders':orders,
        'total_order':total_order,
        'delivered':delivered,
        'pending':pending,
    }

    return render(request, 'main/user.html', context=context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer )

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid:
            form.save()

    context = {
        'form' : form
    }

    return render(request, 'main/account_setting.html', context=context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):  
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'main/products.html', context )  

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk_key):
    customer = Customer.objects.get(id=pk_key) 
    orders =  customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context={
        'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter, 
    }

    return render(request, 'main/customer.html', context=context)     

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk_key):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk_key):

    order = Order.objects.get(id=pk_key)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form':form
    }

    return render(request, 'main/order_form.html', context = context)  

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk_key):
    order = Order.objects.get(id=pk_key)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={
        'item':order
    }

    return render(request, 'main/delete.html', context = context)  
 