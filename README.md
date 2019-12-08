# OuroborosTeam
Our project is  `E-Shop` made on Django Framework
# Technical Part
## How works our shop
There are 2 types of users. Client and Administrator. The site has a basket. Through it, the user can buy a product.
o enter the site you need to create a complex password consisting of beeches and numbers. In the product you can see the comments left by other users, you can also leave it and give a rating to the product. To buy a product you need to add it to the basket and do the operation in it Shopping in the basket there is a special counter that calculates the total amount. Also after the purchase you have your own history of purchases.
### In `AddGood`:
1.Fields for entering data of product
2.Button for add Image and button to save entered data
### In `MainPage`:
List of Products which added by user or admin
LogOut button
Field for search
### In `UserProfile`:
Main information about User
His photo
### In `AdminPage`:
All class name which you can change 
### In `product-pages`:
Model of Product
Price of Product
Country of Product
Year of Product
Rating of Product
Comments to Product
Button `Add To Cart`





## Installed App's
```
 'shopkz.apps.ShopkzConfig',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
```
## Routing of files
```
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR , 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
```
**In the `shopkz` app `urls.py`**:
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopkz/', include('shopkz.urls')),
    path('jet', include('jet.urls')),
]
```
**In the `myproject` app `urls.py`**:
```
 path('home/' , views.index , name='index'),
    path('product/<int:good_id>/', views.product, name='product'),
    path('product/<int:good_id>/comment', views.addComment, name='addComment'),
    path('login' , views.loginView , name='login'),
    path('register/', views.registerView, name="registration"),
    path('' , auth_views.LoginView.as_view(template_name='shopkz/login.html') , name='login'),
    path('rate_good/<int:good_id>', views.rate_good, name="rate_good"),
    path('logout/' , auth_views.LoginView.as_view(template_name='shopkz/login.html') , name='logout'),
    path('profile/' , views.profile , name='profile'),
    path('addgood/' , views.GoodCreate , name='addgood'),
    path('delete/<int:good_id>/' , views.Delete , name='delete'),
    path('products/' , views.all_product , name = 'products'),
    path('profile/edit/' , views.edit_profile , name='edit_profile'),
    path('changepassword/', views.change_password, name='change_password'),
    path('editGood/<int:good_id>', views.edit_good, name='editGood')
```

## Templating system
```
shopkz/templates/shopkz

addGood.html
base.html
blank.html
change_password.html
checkout.html
delete.html
edit_profile.html
editGood.html
index.html
index1.html
login.html
product-page.html
products.html
profile.html
register.html
```
## Models
**`shopkz.models.Good`**
```
class Good(models.Model):
    price = models.DecimalField(decimal_places=1 , max_digits=100)
    new_price = models.DecimalField(decimal_places=1 , max_digits=100 ,default=0)
    model = models.CharField(max_length=100)
    count = models.IntegerField()
    country = models.CharField(null=True , max_length=100)
    description = models.TextField(null=True)
    color = models.CharField(max_length=20)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , default=None)
    year=models.DecimalField(max_digits=5 , decimal_places=1)
    img = models.ImageField(default='default.jpg' , blank=True)
    img1 = models.ImageField(default='default.jpg', blank=True)
    img2 = models.ImageField(default='default.jpg', blank=True)
    main_rating = models.FloatField(default=0.0)
    numberOfClicks = models.IntegerField(default=0)
    comments_numb = models.IntegerField(default=0)

```

**`shopkz.models.Comment`**
```
class Comment(models.Model):
    comments_text = models.TextField()
    good = models.ForeignKey(Good , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    comment_rating = models.FloatField(default=0.0)
    date_posted = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.comments_text
```

**`shopkz.models.QuantityOfViews`**
```
class QuantityOfViews(models.Model):
    number_of_views = models.IntegerField()
    link_to_hidden_ad = models.TextField()

    def getNumberOfViews(self):
        return self.number_of_views
```

**`shopkz.models.Rating`**
```
class Rating(models.Model):
    good_rating = models.ForeignKey(Good , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField()
```

**`shopkz.models.Rating`**
```
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
```            
# Reasons to create project
## Why this topic was chosen.
The reason for choosing this topic was our interest in the field of marketing. Because it is easier for us to present our project in this form. We also want to contribute to our Kazakhstan through this site and make it acceptable in the future in the field web marketing.
## Project auditory.  
Our audience is for people of any age categories. Since the site has a wide range of products


# Contact with us
If you have questions about project.
Tel: 87081711507 Ilyas
     87476586045 Erden
     87002200724 Aibek
Our E-mail:shaman_yo@list.ru     
