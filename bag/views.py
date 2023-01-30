from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    loft = None
    if 'product_loft' in request.POST:
        loft = request.POST['product_loft']
    bag = request.session.get('bag', {})

    if loft:
        if item_id in list(bag.keys()):
            if loft in bag[item_id]['clubs_by_loft'].keys():
                bag[item_id]['clubs_by_loft'][loft] += quantity
            else:
                bag[item_id]['clubs_by_loft'][loft] = quantity
        else:
            bag[item_id] = {'clubs_by_loft': {loft: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the speicified amount """

    quantity = int(request.POST.get('quantity'))
    loft = None
    if 'product_loft' in request.POST:
        loft = request.POST['product_loft']
    bag = request.session.get('bag', {})

    if loft:
        if quantity > 0:
            bag[item_id]['clubs_by_loft'][loft] = quantity
        else:
            del bag[item_id]['clubs_by_loft'][loft]
            if not bag[item_id]['clubs_by_loft']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bagS """
    try:
        loft = None
        if 'product_loft' in request.POST:
            loft = request.POST['product_loft']
        bag = request.session.get('bag', {})

        if loft:
            del bag[item_id]['clubs_by_loft'][loft]
            if not bag[item_id]['clubs_by_loft']:
                bag.pop(item_id)

        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
    