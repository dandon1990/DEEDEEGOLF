from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Comment
from .forms import ProductForm, CommentForm


def all_products(request):
    """A view to show all products, sorting and search queries"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__friendly_name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search info submitted,")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query
            ) | Q(
                description__icontains=query
            ) | Q(
                brand__icontains=query
            )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to show individual products and the more
    information about the product"""

    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.order_by("-created_on")
    form = CommentForm()

    if request.method == 'POST':

        form = CommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()

    context = {
        'product': product,
        'form': form,
        'comments': comments,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    Add a product to the store
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                Please ensure the form is valid')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit a product from the store
    """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Invalid entry, \
                please ensure your form is valid!')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a porduct from the store"""

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Succesfully deleted product!')
    return redirect(reverse('products'))


@login_required
def update_comment(request, pk):
    """ Update comments on the products detail page"""

    comment = get_object_or_404(Comment, pk=pk)
    form_class = CommentForm
    context_object_name = 'comment'
    template_name = 'product_detail.html'

    if request.method == 'POST':
        # Update the comment with the new data
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

    return redirect(reverse('product_detail', args=[comment.product.id]))


@login_required
def delete_comment(request, pk):
    """ Delete comments on product_detail.html """

    comment = get_object_or_404(Comment, pk=pk)
    form_class = CommentForm
    template_name = 'product_detail.html'
    context_object_name = 'comment'

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        post = comment.product
        comment.delete()
        # Return a success URL
        return redirect(reverse('product_detail', args=[post.id]))
