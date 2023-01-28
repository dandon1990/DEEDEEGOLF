# from decimal import Decimal
# from django.conf import settings
# from django.shortcuts import get_object_or_404
# from products.models import Product

# def bag_contents(request):

#     bag_items = []
#     total = 0
#     product_count = 0
#     bag = request.session.get('bag', {})
#     # d_size = 0
#     # if 'product_d_loft' in request.POST:
#     #     d_size = request.POST['product_d_loft']
#     # w_size = 0
#     # if 'product_w_loft' in request.POST:
#     #     w_size = request.POST['product_w_loft']
#     # # d_size = request.POST.get('product_d_loft')
#     # # w_size = request.POST.get('product_w_loft')

#     # for item_id, item_data in bag.items():

#     #     if isinstance(item_data, int):
#     #         product = get_object_or_404(Product, pk=item_id)
#     #         total += item_data * product.price
#     #         product_count += item_data
#     #         bag_items.append({
#     #             'item_id': item_id,
#     #             'quantity': item_data,
#     #             'product': product,
#     #         })
#     #     else:
#     #         if d_size:
#     #             product = get_object_or_404(Product, pk=item_id)
#     #             for d_size, quantity in item_data['items_by_d_size'].items():
#     #                 total += quantity * product.price
#     #                 product_count += quantity
#     #                 bag_items.append({
#     #                     'item_id': item_id,
#     #                     'quantity': item_data,
#     #                     'product': product,
#     #                     'd_size': d_size,
#     #                 })
#     #         elif w_size:        
#     #             for w_size, quantity in item_data['items_by_w_size'].items():
#     #                 total += quantity * product.price
#     #                 product_count += quantity
#     #                 bag_items.append({
#     #                     'item_id': item_id,
#     #                     'quantity': item_data,
#     #                     'product': product,
#     #                     'w_size': w_size, 
#     #                 })
#     for item_id, item_data in bag.items():
#         if isinstance(item_data, int):
#             product = get_object_or_404(Product, pk=item_id)
#             total += item_data * product.price
#             product_count += item_data
#             bag_items.append({
#                 'item_id': item_id,
#                 'quantity': item_data,
#                 'product': product,
#             })
#         else:
#             product = get_object_or_404(Product, pk=item_id)
#             for size, quantity in item_data['items_by_size'].items():
#                 total += quantity * product.price
#                 product_count += quantity
#                 bag_items.append({
#                     'item_id': item_id,
#                     'quantity': item_data,
#                     'product': product,
#                     'size': size,
#                 })

#     if total < settings.FREE_DELIVERY_THRESHOLD:
#         delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
#         free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
#     else:
#         delivery = 0
#         free_delivery_delta = 0
    
#     grand_total = delivery + total

#     context = {
#         'bag_items': bag_items,
#         'total': total,
#         'product_count': product_count,
#         'delivery': delivery,
#         'free_delivery_delta': free_delivery_delta,
#         'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
#         'grand_total': grand_total,
#     }

#     return context

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['club_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context