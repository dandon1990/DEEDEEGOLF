# from django.shortcuts import render, redirect

# # Create your views here.

# def view_bag(request):
#     """A view that renders the shopping bag contents"""

#     return render(request, 'bag/bag.html')

# def add_to_bag(request, item_id):
#     """Add a quantity of the specified product to the shopping bag """

#     # quantity = int(request.POST.get('quantity'))
#     # redirect_url = request.POST.get('redirect_url')
#     # d_size = 0
#     # if 'product_d_loft' in request.POST:
#     #     d_size = request.POST['product_d_loft']
#     # w_size = 0
#     # if 'product_w_loft' in request.POST:
#     #     w_size = request.POST['product_w_loft']
#     # bag = request.session.get('bag', {})

#     # if d_size:
#     #     if item_id in list(bag.keys()):
#     #         if d_size in bag[item_id]['items_by_d_size'].keys():
#     #             bag[item_id]['items_by_d_size'][d_size] += quantity
#     #         else:
#     #             bag[item_id]['items_by_d_size'][d_size] = quantity
#     #     else:
#     #         bag[item_id] = {'items_by_d_size': {d_size: quantity}}

#     # elif w_size:
#     #     if item_id in list(bag.keys()):
#     #         if w_size in bag[item_id]['items_by_w_size'].keys():
#     #             bag[item_id]['items_by_w_size'][w_size] += quantity
#     #         else:
#     #             bag[item_id]['items_by_w_size'][w_size] = quantity
#     #     else:
#     #         bag[item_id] = {'items_by_w_size': {w_size: quantity}}  

#     # else:
#     #     if item_id in list(bag.keys()):
#     #             bag[item_id] += quantity
#     #     else:
#     #         bag[item_id] = quantity
    
#     # print(bag)

#     request.session['bag'] = bag
#     # print(request.POST)
#     return redirect(redirect_url)
from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    d_size = None
    if 'product_loft' in request.POST:
        d_size = request.POST['product_loft']
    bag = request.session.get('bag', {})

    if d_size:
        if item_id in list(bag.keys()):
            if d_size in bag[item_id]['club_by_size'].keys():
                bag[item_id]['club_by_size'][d_size] += quantity
            else:
                bag[item_id]['club_by_size'][d_size] = quantity
        else:
            bag[item_id] = {'club_by_size': {d_size: quantity}}
    # elif w_size:
    #     if item_id in list(bag.keys()):
    #         if w_size in bag[item_id]['items_by_size'].keys():
    #             bag[item_id]['items_by_size_w'][w_size] += quantity
    #         else:
    #             bag[item_id]['items_by_size_w'][w_size] = quantity
    #     else:
    #         bag[item_id] = {'items_by_size_w': {w_size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)