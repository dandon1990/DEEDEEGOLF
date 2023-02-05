from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your shopping bag")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MY8auI3BX4NATntWnk2N9N8aaic0dK7dDJLXTRegbLmTKcPc64JoZq3oAqyfxdUfA73iLzkS3aI4BrYfYvyyPzt00uOS8hDQ0',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)