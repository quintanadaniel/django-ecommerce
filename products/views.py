from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from .forms import ProductForm
from .models import Product


def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect("/products/create/")
        else:
            form.add_error(None, "User must be logged in")
    context["form"] = form
    return render(request, "products/create.html", context)


def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, "products/list.html", {"object_list": object_list})


def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = obj.user == request.user
    context = {"object": obj}
    form = ProductForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # return redirect("/products/create/")
    context["form"] = form
    return render(request, "products/detail.html", context=context)