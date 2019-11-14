from django.db import models
from django.forms import ModelForm

class Good(models.Model):
    product_name=models.CharField(max_length=50)
    price = models.IntegerField(max_length=20)
    model = models.CharField(max_length=20)
    count = models.IntegerField(max_length=10)
    data_add = models.DateTimeField('data of add')
    color = models.CharField(max_length=20)
    year=models.DecimalField(max_digits=4 , decimal_places=1)

class Editor(models.Model):
	editor_name = models.CharField(max_length = 100)
	editor_surname = models.CharField(max_length = 100)

	def __str__(self):
		return self.editor_name + " " + self.editor_surname



class User(models.Model):
    user_name = models.CharField(max_length = 100)
    user_surname = models.CharField(max_length = 100)
    user_dob = models.DateTimeField('date of birth')
  #  user_password= models.PasswrodField()
    user_mail = models.CharField(max_length=150)
    user_male = models.CharField(max_length=10)
    user_address = models.CharField(max_length=100)


class QuantityOfViews(models.Model):
    number_of_views = models.IntegerField()
    link_to_hidden_ad = models.TextField()

    def getNumberOfViews(self):
        return self.number_of_views



