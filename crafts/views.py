from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import ArtisanUserForm, ArtisanForm, CustomerUserForm, CustomerForm, ProductForm, ArtisanLoginForm, \
    CustomerLoginForm
from .models import Product, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


def homepage(request):
    return render(request, 'home.html')


def registration_page(request):
    return render(request, 'register.html')


def artisan_signup(request):
    if request.method == 'POST':
        user_form = ArtisanUserForm(request.POST)
        artisan_form = ArtisanForm(request.POST, request.FILES)

        if user_form.is_valid() and artisan_form.is_valid():
            user = user_form.save(commit=False)

            user.set_password(user_form.cleaned_data['password'])
            user.save()

            artisan = artisan_form.save(commit=False)
            artisan.user = user
            artisan.save()

            return redirect('artisan_login')

    else:
        user_form = ArtisanUserForm()
        artisan_form = ArtisanForm()

    return render(request, 'artisan_signup.html', {'user_form': user_form, 'artisan_form': artisan_form})


def customer_signup(request):
    if request.method == 'POST':
        user_form = CustomerUserForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            return redirect('customer_login')

    else:
        user_form = CustomerUserForm()
        customer_form = CustomerForm()

    return render(request, 'customer_signup.html', {'user_form': user_form, 'customer_form': customer_form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            artisan = request.user.artisan
            product = form.save(commit=False)

            product.artisan = artisan
            product.save()

            return redirect('shop')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def artisan_login(request):
    if request.method == 'POST':
        form = ArtisanLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if hasattr(user, 'artisan') and user.artisan is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error = 'User has no artisan profile.'
            else:
                error = 'Invalid login credentials'
        else:
            error = 'Invalid form data'
    else:
        form = ArtisanLoginForm()
        error = None

    return render(request, 'artisan_login.html', {'form': form, 'error': error})


def customer_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.customer is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Invalid login credentials'
        else:
            error = 'Invalid form data'
    else:
        form = CustomerLoginForm()
        error = None

    return render(request, 'customer_login.html', {'form': form, 'error': error})


def shop(request):
    products = Product.objects.all().order_by('-updated_at')
    return render(request, 'shop.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    sort_option = request.GET.get('sort', '')
    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')

    # Searching
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {'products': products, 'user': request.user}
    return render(request, 'shop.html', context)


@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        mail_subject = 'User Query'
        mail_message = f"Hello admin,a query has been raised and here are the details:\nName: {name}\nEmail: {email}\nMessage: {message}"
        to_email = ["vasanthpatel2111@gmail.com"]

        from_email = "vasanthnani2111@gmail.com"

        send_mail(mail_subject, mail_message, from_email, to_email, fail_silently=False)

        return redirect('home')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Initialize the cart in the session if not already present
    if 'cart' not in request.session:
        request.session['cart'] = {}

    # Update the quantity of the product in the cart
    cart = request.session['cart']
    cart[product_id] = cart.get(product_id, 0) + 1

    request.session.modified = True  # Mark the session as modified to ensure it's saved

    messages.success(request, f"{product.name} added to the cart.")

    return redirect('cart')  # Redirect to the cart or shop page


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total_quantity = 0
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        cart_items.append({'product': product, 'quantity': quantity})

        # Update total quantity and total price
        total_quantity += quantity
        total_price += quantity * product.price

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        for product_id, quantity in request.POST.items():
            if product_id.startswith('quantity_'):
                product_id = product_id.replace('quantity_', '')
                cart[product_id] = int(quantity)

        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Cart updated successfully.')

    return redirect('cart')


def remove_from_cart(request, product_id):
    product_id = int(product_id)

    if 'cart' in request.session:
        cart = request.session['cart']

        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session.modified = True
            messages.success(request, 'Item removed from your cart.')
        else:
            messages.warning(request, 'Item not found in your cart.')
    else:
        messages.warning(request, 'Your cart is empty.')

    return redirect('cart')


def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        customer = request.user.customer  # Assuming the user is logged in and has a customer profile

        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            price = product.price
            order = Order.objects.create(
                product=product,
                customer=customer,
                quantity=quantity,
                price=price,
                address=request.POST.get('address', ''),
                phone=request.POST.get('phone', ''),
                date=datetime.today(),
                status='pending',
            )

        request.session['cart'] = {}

        return redirect('order_list')

    return render(request, 'cart.html')


def order_list(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'order_list.html', {'orders': orders})


def admin_dashboard(request):
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders})


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f'Order {order_id} is {new_status}.')
        return redirect('admin_dashboard')

    return render(request, 'update_order_status.html', {'order_id': order_id})


def cancel_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)

            # Check if the order is cancelable (e.g., in a 'pending' state)
            if order.status == 'pending':
                # Update the order status to 'cancelled'
                order.status = 'cancelled'
                order.save()

                messages.success(request, 'Order successfully canceled.')
            else:
                messages.error(request, 'This order cannot be canceled.')

        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')

    return redirect('order_list')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('shop')
