from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Status(models.Model):
    status = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.status

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.first_name

class Send_Feedback(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.signup.user.first_name


class Food(models.Model):
    food_name = models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=30,null=True)
    price = models.IntegerField(null=True)
    food_detail = models.CharField(max_length=200,null=True)
    image = models.FileField(null=True)
    def __str__(self):
        return self.food_name

class Booking(models.Model):
    book_id = models.CharField(max_length=500,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    signup = models.ForeignKey(Signup,on_delete=models.CASCADE,null=True)
    food = models.ForeignKey(Food,on_delete=models.CASCADE,null=True)
    order_date = models.DateField(null=True)
    time = models.TimeField(null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    quantity  = models.IntegerField(null=True)
    day1 = models.IntegerField(null=True)
    address= models.CharField(max_length=100,null=True)
    city= models.CharField(max_length=100,null=True)
    total = models.IntegerField(null=True)
    def __str__(self):
        return self.signup.user.first_name+" "+self.food.food_name