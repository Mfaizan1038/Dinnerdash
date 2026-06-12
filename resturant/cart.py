from .models import Item

CART_SESSION_KEY = 'cart'

def get_cart(request):
    return request.session.get(CART_SESSION_KEY,{})

def save_cart(request,cart):
    request.session[CART_SESSION_KEY]= cart 
    #Save the session changes to db every time a request end
    request.session.modified = True

def add_to_cart(request,item_id, quantity=1):
    cart = get_cart(request)
    key = str(item_id)
    cart[key] = cart.get(key,0) + quantity
    save_cart(request, cart)

def remove_from_cart(request,item_id):
    cart = get_cart(request)
    key = str(item_id)
    if key in cart:
        del cart[key]
    save_cart(request,cart)

def update_cart(request,item_id, quantity):
    cart = get_cart(request)
    key = str(item_id)
    #If quantity of an item after update is 0, remove that item from cart
    if quantity<=0:
        if key in cart:
            del cart[key]
    else:
        cart[key] = quantity
    save_cart(request,cart)

def clear_cart(request):
    request.session[CART_SESSION_KEY]= {}
    request.session.modified = True

def get_cart_items(request):
    cart = get_cart(request)
    if not cart:
        return []
    item_ids = [int(i) for i in cart.keys()]
    items = Item.objects.filters(pk__in=item_ids)
    item_map = {str(item.pk):item for item in items}
    result = []
    for item_id, qty in cart.items():
        item = item_map.get(item_id)
        if item:
            result.append({
                "item":item,
                "quantity" : qty,
                "subtotal" : item.price*qty
            })
    return result

def get_cart_total(request):
    result = get_cart_items()
    return sum(i['subtotal'] for i in result)

def get_cart_count(request):
    carts = get_cart(request)
    return sum(carts.values())

    



