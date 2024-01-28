from django.contrib import admin
from django.urls import path
from .models import *

# change header 
admin.site.site_header="Welcome Admin"
admin.site.index_title="Admin Dashboard"

# Register your models here.
admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Comment)