from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, Good
from django.utils import timezone


class SimpleUserForm(UserCreationForm):
    email = forms.EmailField()
    # userImg = models.ImageField(upload_to='user_avas/', default='NULL')
    user_address = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password1'
        ]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'imge'
        ]


class CreateGood(forms.ModelForm):
    class Meta:
        model = Good
        fields = [
            'img',
            'model',
            'price',
            'color',
            'count',
            'country',
            'description',
            'year',
            'owner',
        ]


class EditGoodForm(forms.ModelForm):
    class Meta:
        model=Good
        fields = [
            'img',
            'img1',
            'img2',
            'model',
            'price',
            'new_price',
            'color',
            'count',
            'country',
            'description',
            'year',
        ]

class SimpleUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email',
                  'first_name',
                  'last_name')


# class OrderForm(forms.Form):
#
#     name = forms.CharField()
#     last_name = forms.CharField(required=False)
#     phone = forms.CharField()
#     #buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовывоз"),("delivery", "Доставка")]))
#     date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
#     address = forms.CharField(required=False)
#     city = forms.CharField(required=False)
#     country = forms.CharField(required=False)
#     email = forms.EmailField()
#     zip_code = forms.CharField()
#     #comments = forms.CharField(widget=forms.Textarea, required=False)
#
#
#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label = 'First Name'
#         self.fields['last_name'].label = 'Фамилия'
#         self.fields['phone'].label = 'Контактный телефон'
#         self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться'
#         #self.fields['buying_type'].label = 'Способ получения'
#         self.fields['email'].label = 'Email'
#         self.fields['country'].label = 'Country'
#         self.fields['zip_code'].label = 'Zip Code'
#         self.fields['city'].label = 'City'
#         self.fields['address'].label = 'Адрес доставки'
#         self.fields['address'].help_text = '*Обязательно указывайте улицу!'
#         #self.fields['comments'].label = 'Комментарии к заказу'
#         self.fields['date'].label = 'Дата доставки'
#         self.fields['date'].help_text = 'Доставка производится на следущий день после оформления заказа. Менеджер с Вами предварительно свяжется!'


class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Самовывоз"), ("delivery", "Доставка")]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields[
            'phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Адрес доставки'
        self.fields['address'].help_text = '*Обязательно указывайте город!'
        self.fields['comments'].label = 'Комментарии к заказу'
        self.fields['date'].label = 'Дата доставки'
        self.fields[
            'date'].help_text = 'Доставка производится на следущий день после оформления заказа. Менеджер с Вами предварительно свяжется!'
