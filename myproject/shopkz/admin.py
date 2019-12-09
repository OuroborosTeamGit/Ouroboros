from django.contrib import admin, auth
from django.contrib.auth import get_user_model
from .forms import *
from .models import *

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')


make_payed.short_description = "Пометить как оплаченные"
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


admin.site.register(Users)
admin.site.register(Good)
admin.site.register(Editor)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.site_header='Ouroboros Administration'