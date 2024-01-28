from .models import *
from dash_app.models import Blog
from django import forms
from ckeditor.widgets import CKEditorWidget



class UserForm(forms.ModelForm):
    pswd=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields='__all__'
        
class SellerForm(forms.ModelForm):
    spswd=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=Seller
        fields='__all__'
        
class MyForm(forms.ModelForm):
    desc = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Product
        fields = ('desc',)
        
class BlogForm(forms.ModelForm):
    desc = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Blog
        fields = ('desc',)
        