from shop.models import Cart, Categories, Checkout, OrderItem, Product, Profile
from django.contrib.auth import  authenticate,login as auth_user, logout
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import re
# Create your views here.
def index(request):
    c=Categories.objects.all()
    f=Product.objects.all()
    context={
        'c':c,
        'f':f
    }
    return render(request,'index.html',context)

def fruits_show(request,id):
    c=Categories.objects.all()
    category = get_object_or_404(Categories, id=id)
    f=Product.objects.filter(cat=category)
    context={
        'c':c,
        'f':f
    }
    
    return render(request,'index.html',context)


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contact=request.POST['contact']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            return redirect('/')
        
        
         # Password match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Password length
        # if len(pass1) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        #     return redirect("signup")

        # # Uppercase
        # if not re.search(r"[A-Z]", pass1):
        #     messages.error(request, "Password must contain at least one uppercase letter.")
        #     return redirect("signup")

        # # Lowercase
        # if not re.search(r"[a-z]", pass1):
        #     messages.error(request, "Password must contain at least one lowercase letter.")
        #     return redirect("signup")

        # # Number
        # if not re.search(r"\d", pass1):
        #     messages.error(request, "Password must contain at least one number.")
        #     return redirect("signup")

        # # Special Character
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pass1):
        #     messages.error(request, "Password must contain at least one special character.")
        #     return redirect("signup")
        
        
         # Create User
        # user = User.objects.create_user(
        #     username=username,
        #     password=pass1
        # )


        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        
        Profile.objects.create(user=user,contact=contact)

        messages.success(request,"Your account is successfully created.")

        return redirect('/login')
    return render(request,'Register/signup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            auth_user(request, user)
            return redirect("index")
        else:
            return redirect("login")  # Galat details par login page par hi rakhna better hota hai
            
    return render(request, "Register/login.html")


def signout(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('/')



@login_required(login_url='login')
def buy(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    try:
        item = Cart.objects.get(cart_item=product, user=user)
    except Cart.DoesNotExist:
        item = Cart.objects.create(
            user=user,
            cart_item=product,
            name=product.name,
            image=product.image,
            price=product.price,
            quantity=1,
            total_price=product.price
        )
    return redirect("show_buy")

@login_required(login_url='login')
def show_buy(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(i.total_price for i in items)
    return render(request,"buy.html",{"items":items,"total":total})
    
    
def increase_qty(request,id):
    item = Cart.objects.get(id=id)
    item.quantity += 1
    item.total_price = item.price * item.quantity
    item.save()
    return redirect("show_buy")



def decrease_qty(request,id):
    item = Cart.objects.get(id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.total_price = item.price * item.quantity
        item.save()
    return redirect("show_buy")

def remove(request,id):
    Cart.objects.filter(id=id).delete()
    return redirect("show_buy")




@login_required
def checkout(request):
    user = request.user

    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect("show_buy")

    profile = Profile.objects.filter(user=user).first()

    full_name = user.first_name + " " + user.last_name
    contact = profile.contact if profile else ""

    total_amount = sum(item.total_price for item in cart_items)

    if request.method == "POST":

        # Order Save
        order = Checkout.objects.create(
            user=user,
            name=full_name,
            email=user.email,
            numbers=contact,
            address=request.POST.get("address"),
            total_amount=total_amount,
            payment_method="COD",
            status="CONFIRMED"
        )

        # Order Items Save
        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.cart_item,
                quantity=item.quantity,
                price=item.price,
                total_price=item.total_price
            )

        # Buy List Empty
        cart_items.delete()

        return redirect("order_success")

    context = {
        "name": full_name,
        "email": user.email,
        "contact": contact,
        "cart_items": cart_items,
        "total_amount": total_amount,
    }

    return render(request, "checkout.html", context)



    
@login_required
def order_success(request):

    order = Checkout.objects.filter(user=request.user).order_by("-id").first()

    context = {
        "order": order
    }

    return render(request, "order_success.html", context)




@login_required
def Reorder(request):

    orders = Checkout.objects.filter(user=request.user).order_by("-id")

    context = {
        "orders": orders
    }

    return render(request, "Reorder.html", context)


@login_required
def reorder_items(request, id):

    order = get_object_or_404(Checkout, id=id,user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        try:
            cart_item = Cart.objects.get(
                user=request.user,
                cart_item=item.product
            )

            # Product pehle se Buy list me hai
            cart_item.quantity += item.quantity
            cart_item.total_price = cart_item.price * cart_item.quantity
            cart_item.save()

        except Cart.DoesNotExist:

            # Product Buy list me nahi hai
            Cart.objects.create(
                user=request.user,
                cart_item=item.product,
                name=item.product.name,
                image=item.product.image,
                price=item.price,
                quantity=item.quantity,
                total_price=item.total_price
            )

    return redirect("show_buy")

def profile(request):
    return render(request,"profile.html")

@login_required
def settings(request):
    return render(request,"settings.html")



@login_required
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

      
        if not check_password(current_password, request.user.password):

            messages.error(request, "Current password is incorrect.")

            return redirect("change_password")

      
        if new_password != confirm_password:

            messages.error(request, "New passwords do not match.")

            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")

        return redirect("settings")

    return render(request, "Register/change_password.html")


@login_required
def delete_account(request):

    if request.method == "POST":

        password = request.POST.get("password")

        if not check_password(password, request.user.password):

            messages.error(request, "Incorrect Password.")

            return redirect("delete_account")

        user = request.user

        logout(request)

        user.delete()

        messages.success(request, "Your account has been deleted successfully.")

        return redirect("signup")

    return render(request, "Register/delete_account.html")


def search(request):

    query = request.GET.get("search", "").strip()

    f = Product.objects.all()

    if query:

        f = Product.objects.filter(

            Q(name__icontains=query) |

            Q(description__icontains=query) |

            Q(cat__cat_name__icontains=query)

        ).distinct()

    categories = Categories.objects.all()

    context = {

        "f": f,

        "c": categories,

        "search": query,

    }

    return render(request, "index.html", context)