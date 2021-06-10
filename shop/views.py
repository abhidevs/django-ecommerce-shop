from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product, Contact, CartItem, Orders, Address

def getCartLength():
    cartItemsCount = 0
    for item in CartItem.objects.all():
        cartItemsCount += item.quantity

    return cartItemsCount



def index(request):
    category = Product.objects.values_list('category', flat=True)
    category = list(set(category))
    category.sort()

    productsByCat = {}
    products = []
    for cat in category: 
        productsByCat[cat] = Product.objects.filter(category=cat)

    params = {'productsByCat': productsByCat, 'cartItemsCount': getCartLength()}
    return render(request, 'shop/index.html', params)


def about(request):
    params = {'cartItemsCount': getCartLength()}
    return render(request, 'shop/about.html', params)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        contact = Contact(name=name, email=email, message=message)
        contact.save()

    params = {'cartItemsCount': getCartLength()}
    return render(request, 'shop/contact.html', params)


def track(request):
    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def product(request, id):
    # Fetch the product using id
    prod = Product.objects.filter(id=id)

    params = {'product': prod[0], 'cartItemsCount': getCartLength()}
    return render(request, 'shop/prodview.html', params)


def cart(request):
    cartItems = CartItem.objects.all()
    cartProds = []
    quantity = {}

    for item in cartItems:
        id = int(item.product_id[3:])
        prod = Product.objects.filter(id=id)
        cartProds.append(prod[0])
        quantity[id] = item.quantity
        
    cartItemsCount = 0
    for item in cartItems:
        cartItemsCount += item.quantity

    params = {'cartProds': cartProds, 'quantity': quantity, 'cartItemsCount': cartItemsCount}
    return render(request, 'shop/cart.html', params)


def updateCart(request, action):
    product_id = request.POST.get('product_id')
    item = CartItem.objects.filter(product_id=product_id)

    if action == 'increment':
        if len(item):
            item = item[0]
            item.quantity += 1
            item.save(update_fields=["quantity"]) 
        else:
            item = CartItem(product_id=product_id, quantity=1)
            item.save()
    elif action == 'decrement':
        item = item[0]
        if item.quantity == 1:
            pass
        elif item.quantity > 1:
            item.quantity -= 1
            item.save(update_fields=["quantity"]) 
    elif action == 'removeitem':
        item = item[0]
        CartItem.objects.filter(product_id=product_id).delete()

    quantity = 0
    if action != 'removeitem':
        quantity = CartItem.objects.filter(product_id=product_id)[0].quantity

    params = {'cartItemsCount': getCartLength(), 'quantity': quantity}
    return JsonResponse(params, status=200)


def checkout(request):
    if request.method == 'POST':
        customer_id = 111
        address_id = request.POST.get('address_id')
        cartItems = CartItem.objects.all()
        cartLength = len(cartItems)

        if cartLength != 0:
            for item in cartItems:
                product_id = item.product_id[3:]
                quantity = item.quantity
                pricePerItem = Product.objects.filter(id=product_id)[0].price
                order = Orders(customer_id=customer_id, address_id=address_id, product_id=product_id, quantity=quantity, pricePerItem=pricePerItem)
                order.save()
                CartItem.objects.filter(product_id=item.product_id).delete()

        if cartLength > 1:
            return redirect('/orders')
        elif cartLength == 1:
            return redirect('/order/' + str(order.order_id))

    else:
        cartItems = CartItem.objects.all()
        cartProds = []
        quantity = {}

        address = Address.objects.all()[0]

        for item in cartItems:
            id = int(item.product_id[3:])
            prod = Product.objects.filter(id=id)
            cartProds.append(prod[0])
            quantity[id] = item.quantity

        params = {'cartProds': cartProds, 'quantity': quantity, 'address': address, 'cartItemsCount': getCartLength()}
        return render(request, 'shop/checkout.html', params)


def addAddress(request):
    return render(request, 'shop/addAdress.html')


def editAddress(request):
    return render(request, 'shop/editAddress.html')


def orders(request):
    customer_id = 111
    orderItems = Orders.objects.filter(customer_id=customer_id).order_by('-order_date')
    orderedProds = []
    for item in orderItems:
        product_id = item.product_id
        prod = Product.objects.filter(id=product_id)[0]
        orderedProds.append(prod)

    params = {'orderList': zip(orderedProds, orderItems), 'cartItemsCount': getCartLength()}
    return render(request, 'shop/orders.html', params)


def order(request, orderId):
    orderItem = Orders.objects.filter(order_id=orderId)[0]
    prod = Product.objects.filter(id=orderItem.product_id)[0]
    address = Address.objects.filter(address_id=orderItem.address_id)[0]

    params = {'orderItem': orderItem, 'prod': prod, 'address': address, 'cartItemsCount': getCartLength()}
    return render(request, 'shop/order.html', params)