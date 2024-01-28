from django.db import models
from ckeditor.fields import RichTextField
from dash_app.models import *

# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    pswd=models.CharField(max_length=20,blank=True)
    contact=models.IntegerField()
    address=RichTextField(blank=True,null=True)
    # address=models.TextField()
    
    def __str__(self):
        return self.name+" - "+self.email
    
class Seller(models.Model):
    sname=models.CharField(max_length=100)
    semail=models.EmailField()
    spswd=models.CharField(max_length=20)
    scontact=models.IntegerField()
        
    def __str__(self):
        return self.sname+' - '+self.semail
    
class Category(models.Model):
    cat_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.cat_name
    
class Sub_Category(models.Model):
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_cat_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.sub_cat_name+' - '+self.cat.cat_name
    
    
class Product(models.Model):
    SIZE_CHOICE=[
        ("small",'SMALL'),
        ("medium",'MEDIUM',),
        ("large",'LARGE'),
        ("extra large",'EXTRA LARGE')
    ]
    seller=models.ForeignKey(Seller, on_delete=models.CASCADE)
    p_cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    p_sub_cat=models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    pname=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to='product_imgs/',blank=True)
    qty=models.IntegerField()
    size=models.CharField(max_length=20,choices=SIZE_CHOICE)
    desc=RichTextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.pname+' - '+str(self.price)
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    total=models.IntegerField()
    payment_status=models.BooleanField(default=False)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.prod.pname+" "+self.user.name
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE)
    wlist_flag=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prod.pname+" "+self.user.name
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    data=models.CharField(max_length=200,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    msg=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)