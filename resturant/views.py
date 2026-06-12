from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Item,Order, OrderItem
from django.db.models import Q
from .forms import AddToCartForm, UpdateCartForm
from cart import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    categories = Category.objects.all()
    featured_items = Item.objects.filter(is_retired=False).order_by('?')[:8]
    return render(request,'resturant/home.html',{
        'categories':categories,
        'featured_items': featured_items
    })

def item_list(request):
    category_slug = request.GET.get('category')
    search_q = request.GET.get('q', '').strip()
    if request.user.is_authenticated and request.user.is_admin:
        item = Item.objects.all()
    else:
        item = Item.objects.filter(is_retired=False)

    categories = Category.objects.all()
    active_category =  None
    if category_slug:
        active_category =get_object_or_404(Category, slug =category_slug)
        item = item.filter(categories=active_category)
    if search_q:
        item =item.filter(Q(title__icontains=search_q))| Q(description__icontains=search_q)
    items = item.prefetch_related('categories')
    return render(request,'resturant/item_list.html',{'items':items,'categories':categories,'active_category':active_category,"search_q":search_q})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    can_add = not item.is_retired
    form = AddToCartForm(initial={"item_id":pk})
    return render(request, 'resturant/item_detail.html',{"item":item,"can_add":can_add,"form":form})

def cart_view(request):
    cart_items = get_cart_items()
    total = get_cart_total()
    return render(request,'resturant/cart.html',{"cart_items":cart_items,"total":total})

def cart_add(request,item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.is_retired:
        messages.error(request, "Requested Item in unavailable")
        return redirect('item_detail',pk=item_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            messages.success(request,'item add successfully')
        else:
            messages.error(request,'Invalid quantity')
    return redirect('cart')

def cart_update(request, item_id):
    if request.method == 'POST':
        form = UpdateCartForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            update_cart(request,item_id,qty)
        else:
            messages.error(request,'Invalid Form details')
    return redirect('cart')

def cart_remove(request,item_id):
    remove_from_cart(request,item_id)
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        messages.error(request,'Your cart is empty')
        return redirect('cart')
    for i in cart_items:
        if i['item'].is_retired:
            messages.error(request,f'{i['item']} is no longer available')
            return redirect('cart')
    if request.method == 'POST':
        order = Order.objects.create(user = request.user, status = 'ordered')
        for i in cart_items:
            OrderItem.objects.create(
                order=order,
                item = i['item'],
                quantity = i['quantity'],
                price_at_purchase = i['item'].price


            )
            clear_cart(request)
            messages.success('request','order placed successfully')
            return redirect('order_detail',pk=order.pk)
        total = get_cart_total(request)
        return render(request, 'resturant/checkout.html', {"cart_items":cart_items,"total":total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__order')
    return render(request,'resturant/order_history.html',{'order':orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
        



    







            


        



