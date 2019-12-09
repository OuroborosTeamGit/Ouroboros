from django.urls import path
from django.contrib.auth.views import auth_login
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('product/<int:good_id>/', views.product, name='product'),
    path('product/<int:good_id>/comment', views.addComment, name='addComment'),
    path('login/', views.loginView, name='login'),
    path('search/', views.search, name="search"),
    path('register/', views.registerView, name="registration"),
    path('', auth_views.LoginView.as_view(template_name='shopkz/login.html'), name='login'),
    path('rate_good/<int:good_id>', views.rate_good, name="rate_good"),
    path('logout/', auth_views.LoginView.as_view(template_name='shopkz/login.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('addgood/', views.GoodCreate, name='addgood'),
    path('delete/<int:good_id>/', views.Delete, name='delete'),
    path('products/', views.all_product, name='products'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('changepassword/', views.change_password, name='change_password'),
    path('editGood/<int:good_id>', views.edit_good, name='editGood'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.category_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', views.product_view, name='product_detail'),
    #path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    url(r'^add_to_cart/$', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', views.change_item_qty, name='change_item_qty'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/', views.order_create_view, name='create_order'),
    path('make_order/', views.make_order_view, name='make_order'),
    path('payment/', views.payment, name='payment'),
    url(r'^thank_you/$', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    url(r'^account/$', views.account_view, name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
