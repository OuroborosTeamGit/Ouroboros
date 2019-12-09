from __future__ import unicode_literals

from django.db.models import Sum
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import SimpleUserForm, SimpleUserChangeForm, UpdateProfileForm
from .models import User
from django.contrib.auth import update_session_auth_hash
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from .models import Category, CartItem, Cart, Order
from django.views.generic import View
from django.contrib.auth.models import User


def index(request):
    new_goods = Good.objects.order_by('year')[:4]
    latest_goods =Good.objects.order_by('-year')[:4]
    hot_deal = Good.objects.order_by('price')[:4]
    banner1 = Good.objects.order_by('price')[:1]
    banner2 = Good.objects.order_by('-price')[:1]
    banner3 = Good.objects.order_by('numberOfClicks')[:1]
    banner4 = Good.objects.order_by('-numberOfClicks')[:1]
    popular_goods = Good.objects.filter(numberOfClicks__gt=3).order_by('-numberOfClicks')[:4]

    context = {
        "new_goods":new_goods,
        "latest_goods":latest_goods,
        "popular_goods":popular_goods,
        "hot_deal":hot_deal,
        "banner1":banner1,
        "banner2": banner2,
        "banner3": banner3,
        "banner4": banner4,
    }

    """Using render() to laod the template"""
    return render(request, "shopkz/index.html", context)
def loginView(request):
    print("Index")
    return render(request , "shopkz/index1.html")
def showComments(request, good_id):
    try:
        comments = Comment.objects.filter(good=Good.objects.get(pk=good_id))
        return comments
    except:
        return "No comments yet"
def edit_good(request,good_id):
    good=get_object_or_404(Good,pk=good_id)
    form=EditGoodForm(request.POST or None,request.FILES or None,instance=good)
    if request.method =='POST':
        form.save()
        return redirect('index')
    return render(request,"shopkz/editGood.html",{'form':form})
def search(request):
    user = None
    try:
        user = User.objects.get(pk=request.user.id)

    except:
        pass
    try:

        searched_text = request.POST['searched_text'].lower()
        found_good = []
        goods  = Good.objects.all()
        for good in goods:
            if good.model.lower().count(searched_text) > 3 or good.description.lower().count(searched_text) > 3:
                found_good.append(good)
        return render(request, "shopkz/search.html", {'found_good': found_good, 'user': user})
    except:
        messages.warning(request, "Not found!")
        return render(request ,"shopkz/index.html" )


def Delete(request, good_id):
    gd = get_object_or_404(Good, pk=good_id)
    owner = gd.owner
    if request.method == "POST":
        if request.user.username is owner:
            gd.delete()
            messages.success(request, "Product successfully deleted!")
            return redirect("index")
        else:
            messages.warning(request,"You are not added this product!")
            return redirect("index")
    context = {'good': gd,
               'owner': owner,
               }
    return render(request, 'shopkz/delete.html', context)
def get_rating_in_stars_list(rating):
    counter = int(rating)
    stars = [2 for i in range(counter)]
    if counter < rating:
        stars.append(1 if rating >= float(counter) + 0.5 else 0)
    if counter < rating:
        counter += 1
    for i in range(5 - counter):
        stars.append(0)
    return stars


def product(request , good_id):
    gd = get_object_or_404(Good, pk=good_id)
    gd.numberOfClicks += 1
    owner = gd.owner
    comments = showComments(request , good_id)
    stars = get_rating_in_stars_list(gd.main_rating)
    gd.save()
    if request.method == 'POST':
        try :
            ratings = Rating.objects.filter(good_rating=gd)
            userx = User.objects.get(pk=request.user.id)
            rating_number = int(request.POST['new_rating'])
            new_rating = Rating(user=userx, good_rating=gd, stars=rating_number)
            new_rating.save()
            sum_of_rating = gd.main_rating * len(ratings) + rating_number
            gd.main_rating = sum_of_rating / (len(ratings) + 1)
            txt = request.POST.get("comments_text")
            print(request.POST)
            comment = Comment(comments_text = txt ,
                              comment_rating = rating_number ,
                              good = Good.objects.get(pk = good_id) ,user = request.user)
            gd.comments_numb +=1
            gd.save()
            comment.save()

        except:
            print('the comment cannot be added')
    return render(request, "shopkz/product-page.html" ,{"good":gd , "comments":comments , "stars":stars ,"owner":owner , "goods": Good.objects.order_by('price')[:4] })
def rate_good(request, good_id):
    goodx = get_object_or_404(Good, pk=good_id)
    try:
        ratings = Rating.objects.filter(good=goodx)
        userx = User.objects.get(pk=request.session['user_id'])
        for i in ratings:
            if i.rating_user == userx:
                return HttpResponseRedirect(reverse('product', args=(good_id, )))
        rating_number = int(request.POST['new_rating'])
        new_rating = Rating(user=userx, good=goodx, stars=rating_number)
        new_rating.save()
        sum_of_rating = goodx.main_rating * len(ratings) + rating_number
        goodx.main_rating = sum_of_rating / (len(ratings) + 1)
        goodx.save()
    except:
        pass
    return HttpResponseRedirect(reverse('product', args=(good_id, )))
def addComment(request, good_id):

    try:
        if request.method == "POST":
            txt = request.POST.get("comments_text")
            print("addcomment")
            comment = Comment.objects.get_or_create(comments_text=txt,
                              good=Good.objects.get(pk=good_id) )

            comment.save()
        return render(request, "shopkz/product-page.html",
                                {"good":Good.objects.get(pk=good_id)})
    except:
        return HttpResponse("No such articles")
def registerView(request):
    if request.method == 'POST':
        form = SimpleUserForm(request.POST)
        if form.is_valid():
            print('created')
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = SimpleUserForm()
        print("not")
    return render(request, 'registration/register.html', {'form': form})
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request , form.user)
            return redirect('profile')
        else :
            return redirect( 'change_password' )
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request , 'shopkz/change_password.html' , {'form': form})
def edit_profile(request):
    if request.method=='POST':
        form = SimpleUserChangeForm(request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SimpleUserChangeForm(instance=request.user)

        return render(request , 'shopkz/edit_profile.html' , {'form': form})
@login_required
def GoodCreate(request):
    if request.method =='POST':
        form = CreateGood(request.POST , request.FILES)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect('index')
    else :
        form = CreateGood()
    return render(request, 'shopkz/addGood.html' , {'form': form})
@login_required
def profile (request):
    if request.method == 'POST':
        u_form = SimpleUserChangeForm(request.POST , instance=request.user)
        p_form = UpdateProfileForm(request.POST , request.FILES , instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You account has been updated !!')
            return redirect('profile')
    else :
        u_form = SimpleUserChangeForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    return render(request , 'shopkz/profile.html' , context)
def all_product(request):

    return render(request , 'shopkz/products.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = SimpleUserChangeForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You account has been updated !!')
            return redirect('profile')
    else:
        u_form = SimpleUserChangeForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

    return render(request, 'shopkz/profile.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Good.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'shopkz/product.html', context)


def category_view(request, category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    category = Category.objects.get(slug=category_slug)
    price_filter_type = request.GET.get('price_filter_type')
    print(price_filter_type)
    products_of_category = Good.objects.filter(category=category)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'cart': cart
    }
    return render(request, 'shopkz/category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'shopkz/cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    products = Good.objects.get(slug=product_slug)
    cart.add_to_cart(products.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Good.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse(
        {'cart_total': cart.items.count(),
         'item_total': cart_item.item_total,
         'cart_total_price': cart.cart_total})


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'shopkz/checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'shopkz/order.html', context)


# def make_order_view(request):
#     try:
#         cart_id = request.session['cart_id']
#         cart = Cart.objects.get(id=cart_id)
#         request.session['total'] = cart.items.count()
#     except:
#         cart = Cart()
#         cart.save()
#         cart_id = cart.id
#         request.session['cart_id'] = cart_id
#         cart = Cart.objects.get(id=cart_id)
#     form = OrderForm(request.POST or None)
#     categories = Category.objects.all()
#     if form.is_valid():
#         name = form.cleaned_data['name']
#         last_name = form.cleaned_data['last_name']
#         email = form.cleaned_data['email']
#         address = form.cleaned_data['address']
#         city = form.cleaned_data['city']
#         country = form.cleaned_data['country']
#         zip_code = form.cleaned_data['zip_code']
#         phone = form.cleaned_data['phone']
#         #buying_type = form.cleaned_data['buying_type']
#         #comments = form.cleaned_data['comments']
#         new_order = Order.objects.create(
#             user=request.user,
#             items=cart,
#             total=cart.cart_total,
#             first_name=name,
#             last_name=last_name,
#             email=email,
#             address=address,
#             city=city,
#             country=country,
#             zip_code=zip_code,
#             phone=phone
#             #buying_type=buying_type,
#             #comments=comments
#         )
#         del request.session['cart_id']
#         del request.session['total']
#         return HttpResponseRedirect(reverse('shopkz/thank_you'))
#     return render(request, 'shopkz/order.html', {'categories': categories})

def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comments=comments
        )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('shopkz/thank_you'))
    return render(request, 'shopkz/checkout.html', {'categories': categories})


def payment(request):
    sums_of_cart = Cart.objects.aggregate(Sum('items'))
    return render(request, 'shopkz/payment.html', {'sum': sums_of_cart})


def account_view(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
    for item in order:
        for new_item in item.items.items.all():
            print(new_item.item_total)
    context = {
        'order': order,
        'categories': categories
    }
    return render(request, 'shopkz/account.html', context)
