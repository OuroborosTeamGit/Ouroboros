from decimal import Decimal

from appdirs import unicode
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from notifications.signals import notify
from transliterate import translit


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    imge = models.ImageField(default='default.jpg' , upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self , *args , **kwargs):
        super(Profile,self).save(*args , **kwargs)
        img = Image.open(self.imge.path)
        if img.height >300 or img.width >300:
            output_size= (300 , 300)
            img.thumbnail(output_size)
            img.save(self.imge.path)



class Good(models.Model):
    price = models.DecimalField(decimal_places=1 , max_digits=100)
    new_price = models.DecimalField(decimal_places=1 , max_digits=100 ,default=0)
    model = models.CharField(max_length=100)
    count = models.IntegerField()
    country = models.CharField(null=True , max_length=100)
    description = models.TextField(null=True)
    color = models.CharField(max_length=20)
    slug = models.SlugField(null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , default=None)
    year=models.DecimalField(max_digits=5 , decimal_places=1)
    img = models.ImageField(default='default.jpg' , blank=True)
    img1 = models.ImageField(default='default.jpg', blank=True)
    img2 = models.ImageField(default='default.jpg', blank=True)
    main_rating = models.FloatField(default=0.0)
    numberOfClicks = models.IntegerField(default=0)
    comments_numb = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.model

    def rate_good(self, new_rate):
        if self.rating == 0.0:
            self.rating = new_rate
            return self.rating
        else:
            return (self.rating + new_rate) / 2

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'product_slug': self.slug})


class Comment(models.Model):
    comments_text = models.TextField()
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comments_text


class Editor(models.Model):
    editor_name = models.CharField(max_length=100)
    editor_surname = models.CharField(max_length=100)

    def __str__(self):
        return self.editor_name + " " + self.editor_surname


class Rating(models.Model):
    good_rating = models.ForeignKey(Good , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField()

class Users(models.Model):
    surname = models.CharField('surname', max_length=100)
    user_dob = models.DateTimeField('date of birth')
    user_mail = models.EmailField(max_length=100)
    # userImg = models.ImageField(upload_to='user_avas/', default='NULL')
    user_address = models.CharField(max_length=100)


class QuantityOfViews(models.Model):
    number_of_views = models.IntegerField()
    link_to_hidden_ad = models.TextField()

    def getNumberOfViews(self):
        return self.number_of_views


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(unicode(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


def product_available_notification(sender, instance, *args, **kwargs):
    if instance.available:
        await_for_notify = [notification for notification in MiddlwareNotification.objects.filter(
            product=instance)]
        for notification in await_for_notify:
            notify.send(
                instance,
                recipient=[notification.user_name],
                verb='Уважаемый {0}! {1}, который Вы ждете, поступил'.format(
                    notification.user_name.username,
                    instance.title),
                description=instance.slug
            )
            notification.delete()


post_save.connect(product_available_notification, sender=Good)


class CartItem(models.Model):
    product = models.ForeignKey(Good, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return "Cart item for product {0}".format(self.product.model)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __unicode__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Good.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        cart_items = [item.product for item in cart.items.all()]
        if new_item.product not in cart_items:
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Good.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()




# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     items = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     phone = models.CharField(max_length=20)
#     address = models.CharField(max_length=255)
#     email = models.EmailField(max_length=100, null=True)
#     city = models.CharField(max_length=100, null=True)
#     country = models.CharField(max_length=100,  null=True)
#     zip_code = models.CharField(max_length=100,  null=True)
#     # buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'),('Доставка', 'Доставка')), default='Самовывоз')
#     date = models.DateTimeField(auto_now_add=True)
#     # comments = models.TextField()
#     status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])
#
#     def __unicode__(self):
#         return "Заказ №{0}".format(str(self.id))

ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'),
                                                           ('Доставка', 'Доставка')), default='Самовывоз')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __unicode__(self):
        return "Заказ №{0}".format(str(self.id))



class MiddlwareNotification(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Good, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)

    def __unicode__(self):
        return "Нотификация для пользователя {0} о поступлении товара {1}".format(
            self.user_name.name,
            self.product.model
        )
