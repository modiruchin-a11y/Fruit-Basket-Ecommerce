from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from shop.models import OrderItem, Product, Checkout, Categories
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def admin_login(request):

    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid Admin Credentials")

    return render(request, "admin_panel/admin_log.html")


def admin_logout(request):

    logout(request)

    return redirect("admin_log")





@login_required
def dashboard(request):

    if not request.user.is_superuser:
        return redirect("admin_log")

    total_users = User.objects.count()

    total_products = Product.objects.count()

    total_orders = Checkout.objects.count()

    revenue = sum(order.total_amount for order in Checkout.objects.all())

    pending_orders = Checkout.objects.filter(
        status="PENDING"
    ).count()

    delivered_orders = Checkout.objects.filter(
        status="DELIVERED"
    ).count()

    recent_orders = Checkout.objects.order_by("-id")[:5]

    context = {
    "total_users": total_users,
    "total_products": total_products,
    "total_orders": total_orders,
    "revenue": revenue,
    "pending_orders": pending_orders,
    "delivered_orders": delivered_orders,
    "recent_orders": recent_orders,
}
    return render(request,"admin_panel/dashboard.html",context)


@login_required
def categories(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    categories = Categories.objects.all()

    context = {
        "categories": categories
    }

    return render(request, "admin_panel/categories.html", context)


@login_required
def add_category(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    if request.method == "POST":

        cat_name = request.POST.get("cat_name")

        if cat_name:

            Categories.objects.create(
                cat_name=cat_name
            )

            return redirect("categories")

    return render(request, "admin_panel/add_categories.html")

@login_required
def edit_category(request, id):

    if not request.user.is_superuser:
        return redirect("admin_login")

    category = Categories.objects.get(id=id)

    if request.method == "POST":

        category.cat_name = request.POST.get("cat_name")
        category.save()

        return redirect("categories")

    context = {
        "category": category
    }

    return render(request, "admin_panel/edit_categories.html", context)


@login_required
def delete_category(request, id):

    if not request.user.is_superuser:
        return redirect("admin_login")
    category = Categories.objects.get(id=id)

    category.delete()

    return redirect("categories")

def products(request):

    if not request.user.is_superuser:
        return redirect("admin_login")
    products = Product.objects.all()
    context = {
        "products": products
    }

    return render(request, "admin_panel/products.html", context)


@login_required
def add_product(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    categories = Categories.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        category = Categories.objects.get(id=category_id)

        Product.objects.create(
            cat=category,
            name=name,
            price=price,
            quantity=quantity,
            description=description,
            image=image
        )

        return redirect("products")

    context = {
        "categories": categories
    }

    return render(request, "admin_panel/add_product.html", context)


@login_required
def edit_product(request, id):

    if not request.user.is_superuser:
        return redirect("admin_login")

    product = Product.objects.get(id=id)
    categories = Categories.objects.all()

    if request.method == "POST":

        product.name = request.POST.get("name")

        category_id = request.POST.get("category")
        product.cat = Categories.objects.get(id=category_id)

        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()

        return redirect("products")

    context = {
        "product": product,
        "categories": categories,
    }

    return render(request, "admin_panel/edit_product.html", context)


@login_required
def delete_product(request, id):

    if not request.user.is_superuser:
        return redirect("admin_login")
    product = Product.objects.get(id=id)

    product.delete()

    return redirect("products")

@login_required
def orders(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    orders = Checkout.objects.all().order_by("-id")

    context = {
        "orders": orders
    }

    return render(request,"admin_panel/orders.html",context)

@login_required
def order_details(request, id):

    if not request.user.is_superuser:
        return redirect("admin_login")

    order = get_object_or_404(Checkout, id=id)

    order_items = OrderItem.objects.filter(order=order)

    if request.method == "POST":

        order.status = request.POST.get("status")

        order.save()

        return redirect("order_details", id=order.id)

    context = {

        "order": order,
        "order_items": order_items,

    }

    return render(request,"admin_panel/order_details.html",context)


@login_required
def users(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    users = User.objects.all().order_by("-id")

    context = {
        "users": users
    }

    return render(request,"admin_panel/users.html",context)
