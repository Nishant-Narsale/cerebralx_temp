from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Customer, Product, Order, OrderItem, ShippingAddress
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt

def all_products(request):
    username = ""
    products = Product.objects.all()
    user_is_authenticated = False
    if request.user.is_authenticated:
        user_is_authenticated = True
        username = request.user.username
    
    context = {
        'products':products,
        'user_is_authenticated':user_is_authenticated,
        "username":username,
    }
    return render(request,'products.html',context)

def productDetail(request, pk):
    username = ""
    product_obj = Product.objects.get(id=pk)
    user_is_authenticated = False
    if request.user.is_authenticated:
        user_is_authenticated = True
        username = request.user.username

    context = {
        "product":product_obj,
        'user_is_authenticated':user_is_authenticated,
        "username":username,
    }
    return render(request,'product_page.html', context)

def buynow(request, pk):
    username = ''
    payment = ''
    user_is_authenticated = False
    is_through_buynow = True
    
    if request.user.is_authenticated:
        user_is_authenticated = True
        username = request.user.username
        product = Product.objects.get(id=pk)
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False,is_through_buy_now_button=True)
        order_items, created_ = OrderItem.objects.get_or_create(order=order, product=product, quantity=1)
        order_items = [order_items]

        if request.method == "POST":
            
            client = razorpay.Client(auth=("rzp_test_rY2iMC7xvq90zA", "5IS7AYvbXlITloLYxheVwsZa"))

            DATA = {
                "amount": 100,
                "currency": "INR",
                "payment_capture": "1",
                # "receipt": "receipt#1",
                # "notes": {
                #     "key1": "value3",
                #     "key2": "value2"
                # }
            }
            payment = client.order.create(data=DATA)


            try:
                data = json.loads(request.body)
                order = Order.objects.get(customer = request.user.customer,complete=False, id=data['order_id'])
                shipping_add, created = ShippingAddress.objects.get_or_create(customer=request.user.customer,order=order)

                shipping_add.address = data['address']
                shipping_add.optional_address = data['optional_address']
                shipping_add.city = data['city']
                shipping_add.state = data['state']
                shipping_add.zipcode = data['zipcode']

                shipping_add.save()
                
                return JsonResponse({
                    "Done":True
                })
            except Exception as e:
                print(e)
                return JsonResponse({
                    "Done":False
                })

        context = {
            "order_items":order_items,
            "order":order,
            'user_is_authenticated':user_is_authenticated,
            "username":username,
            "payment":payment,
            "is_through_buynow":is_through_buynow
        }
        return render(request, 'checkout.html', context)

    else:
        return redirect('account:register')

def cart(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_is_authenticated = True
        customer = request.user.customer
        try:
            order = Order.objects.filter(customer=customer,complete=False)[0]
            print(order)
        except:
            order = Order.objects.create(customer=customer, complete=False)
        
        order_items = order.orderitem_set.all()
        
    else:
        return redirect('account:register')

    context = {
        "order_items":order_items,
        'user_is_authenticated':user_is_authenticated,
        "order":order,
        "username":username,
        }
    return render(request, 'cart.html', context)

def checkout(request):
    username = ""
    payment = ""
    user_is_authenticated = False
    is_through_buynow = False
    if request.user.is_authenticated:
        if request.method == "POST":
        
            client = razorpay.Client(auth=("rzp_test_rY2iMC7xvq90zA", "5IS7AYvbXlITloLYxheVwsZa"))

            DATA = {
                "amount": 100,
                "currency": "INR",
                "payment_capture": "1",
                # "receipt": "receipt#1",
                # "notes": {
                #     "key1": "value3",
                #     "key2": "value2"
                # }
            }
            payment = client.order.create(data=DATA)


            try:
                data = json.loads(request.body)
                order = Order.objects.filter(customer = request.user.customer,complete=False)[0]
                shipping_add, created = ShippingAddress.objects.get_or_create(customer=request.user.customer,order=order)

                shipping_add.address = data['address']
                shipping_add.optional_address = data['optional_address']
                shipping_add.city = data['city']
                shipping_add.state = data['state']
                shipping_add.zipcode = data['zipcode']

                shipping_add.save()
                
                return JsonResponse({
                    "Done":True
                })
            except Exception as e:
                print(e)
                return JsonResponse({
                    "Done":False
                })

        else:
            user_is_authenticated = True
            username = request.user.username
            customer = request.user.customer
            try:
                order = Order.objects.filter(customer=customer,complete=False)[0]
            except:
                order = Order.objects.create(customer=customer)

            order_items = order.orderitem_set.all()
        
    else:
        return redirect('account:register')

    context = {
        "order_items":order_items,
        "order":order,
        'user_is_authenticated':user_is_authenticated,
        "username":username,
        "payment":payment,
        "is_through_buynow":is_through_buynow
    }
    return render(request, 'checkout.html', context)

def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    product = Product.objects.get(id=productId)
    customer = request.user.customer
    try:
        order = Order.objects.filter(customer=customer,complete=False)[0]
    except:
        order = Order.objects.create(customer=customer,complete=False)

    try:
        orderItem = OrderItem.objects.get(order=order, product=product)
    except:
        orderItem = OrderItem.objects.create(order=order, product=product, quantity=0)

    if action=='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if action=='removeItem':
        orderItem.delete()
        return JsonResponse("Item is removed", safe=False)

    if orderItem.quantity <= 0:
        orderItem.delete()
        return JsonResponse("Item is removed", safe=False)

    return JsonResponse("Item is updated", safe=False)

def all_order_items(request):
    order_items_ids = []
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.filter(customer=customer,complete=False)[0]
            order_items_querysets = OrderItem.objects.filter(order=order)
            for order_item_queryset in order_items_querysets:
                order_items_ids.append(order_item_queryset.product.id)
        except:
            return JsonResponse({
                "status":"NOT OK"
            })

    json_object = {
        "status":"200 OK",
        "order_items_ids": order_items_ids
    }
    return JsonResponse(json_object)

@csrf_exempt
def order_success(request,order_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            customer = request.user.customer
            order = Order.objects.get(customer=customer,id=order_id)
            order.transaction_id = data['razorpay_payment_id']
            order.complete = True
            order.save()
            
            return JsonResponse({
                'response':'done'
            })
        else:
            return redirect('api:index')
    else:
        return JsonResponse({
            'response':'not authenticated'
        })
