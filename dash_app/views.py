from django.shortcuts import render,redirect
from django.views import View
from myapp.models import Seller,Category,Sub_Category,Product
from myapp.forms import MyForm,BlogForm
from django.http import JsonResponse
from .models import *
from myapp.models import Comment
import pdfkit as pdf

# Create your views here.

# for class based views use redirect eg : redirect("name_of_url")

# {{ forloop.loop }} : this use to print serial numbers in a list on HTML page

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        try:
            seller=Seller.objects.get(semail=request.POST['email'])
            request.session['semail']=seller.semail
            request.session['sname']=seller.sname
            return render(request,'home.html')
        except:
            emsg="Email or Password Is Incorrect !!!"
            return render(request,'login.html',{'emsg':emsg})
    
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    
    def post(self,request):
        try:
            seller=Seller.objects.get(semail=request.POST['email'])
            emsg="Account Already Exist !!!"
            return render(request,'register.html',{'emsg':emsg})
            
        except:
            seller=Seller.objects.create(
                sname=request.POST['name'],
                semail=request.POST['email'],
                spswd=request.POST['pswd'],
                scontact=request.POST['contact']
            )
            return render(request,'login.html')
        
class HomeView(View):
    def get(self,request):
        return render(request,'home.html')
    
class SignoutView(View):
    def get(self,request):
        del request.session['semail']
        del request.session['sname']
        return redirect('login')
    
# >>>>>>>>>>>>>>>>>>>>>>>> Product Selection <<<<<<<<<<<<<<<<<<<<<

class ProductView(View):
    def get(self,request):
        prods=Product.objects.all()
        return render(request,'admin_products.html',{'prods':prods})

class AddProductView(View):
    def get(self,request):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>in get")
        cats=Category.objects.all()
        sub_cats=Sub_Category.objects.all()
        form=MyForm()
        return render(request,'admin_add_product.html',{'cats':cats,'sub_cats':sub_cats,'form':form})
    
    def post(self,request):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>in post")
        prod=Product.objects.create(
            seller=Seller.objects.get(semail=request.session['semail']),
            p_cat=Category.objects.get(cat_name=request.POST['cat']),
            p_sub_cat=Sub_Category.objects.get(sub_cat_name=request.POST['p_sub_cat']),
            pname=request.POST['pname'],
            price=request.POST['price'],
            image=request.FILES['image'],
            qty=request.POST['qty'],
            size=request.POST['size'],
            desc=request.POST['desc'])
        
        return redirect('admin_products')
    
class DelProdView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        prod.delete()
        return redirect('admin_products')
    
class UpdateProdView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        cats=Category.objects.all()
        sub_cats=Sub_Category.objects.all()
        form=MyForm()
        return render(request,'update_prod.html',{'cats':cats,'sub_cats':sub_cats,'prod':prod,'form':form})
    
    def post(self,request,pk):
        prod=Product.objects.get(pk=pk)
        prod.seller=Seller.objects.get(semail=request.session['semail'])
        prod.p_cat=Category.objects.get(cat_name=request.POST['cat'])
        prod.p_sub_cat=Sub_Category.objects.get(sub_cat_name=request.POST['p_sub_cat'])
        prod.pname=request.POST['pname']
        prod.proce=request.POST['price']
        try:
            prod.image=request.FILES['image']
        except:
            pass
        prod.qty=request.POST['qty']
        prod.size=request.POST['size']
        prod.desc=request.POST['desc']
        prod.save()
        return redirect('admin_products')
    
# >>>>>>>>>>>>>>>>>>>>>>>> Category Selection <<<<<<<<<<<<<<<<<<<<<
   
class CatView(View):
    def get(self,request):
        cat=Category.objects.all()
        return render(request,'admin_cat.html',{'cat':cat})
    
class AddCatView(View):
    def get(self,request):
        return render(request,'add_cat.html')
    
    def post(self,request):
        cat=Category.objects.create(cat_name=request.POST['cat_name'])
        return redirect("admin_cat")
    
class DelCatView(View):
    def get(seld,request,pk):
        cat=Category.objects.get(pk=pk)
        cat.delete()
        return redirect('admin_cat')
    
class UpdateCatView(View):
    def get(self,request,pk):
        cat=Category.objects.get(pk=pk)
        return render(request,'update_cat.html',{'cat':cat})
    
    def post(self,request,pk):
        cat=Category.objects.get(pk=pk)
        cat.cat_name=request.POST['cat_name']
        cat.save()
        return redirect('admin_cat')

# >>>>>>>>>>>>>>>>>>>>>>>> sub category <<<<<<<<<<<<<<<<<<<<<

class FilterView(View):
    def get(self,request):
        cats=Category.objects.all()
        try:
            cat=Category.objects.get(cat_name=request.GET['cat_name'])
            sub_cat=Sub_Category.objects.filter(cat=cat)
            return render(request,'admin_sub_cat.html',{'sub_cat':sub_cat,'cats':cats,'cat':cat})
        except:
            sub_cat=Sub_Category.objects.all()
            return render(request,'admin_sub_cat.html',{'sub_cat':sub_cat,'cats':cats})
            
class SubCatView(View):
    def get(self,request):
        cats=Category.objects.all()
        sub_cat=Sub_Category.objects.all()
        return render(request,'admin_sub_cat.html',{'sub_cat':sub_cat,'cats':cats})
    
class AddSubCatView(View):
    def get(self,request,pk):
        cat=Category.objects.get(pk=pk)
        return render(request,'add_sub_cat.html',{'cat':cat})
    
    def post(self,request,pk):
        cat=Category.objects.get(pk=pk)
        sub_cat_create=Sub_Category.objects.create(cat=cat,sub_cat_name=request.POST['sub_cat_name'])
        sub_cat=Sub_Category.objects.filter(cat=cat)
        return render(request,'admin_sub_cat.html',{'sub_cat':sub_cat,'cat':cat})
    
class DelSubCatView(View):
    def get(seld,request,pk):
        sub_cat=Sub_Category.objects.get(pk=pk)
        sub_cat.delete()
        return redirect('admin_sub_cat')
    
class UpdateSubCatView(View):
    def get(self,request,pk):
        sub_cat=Sub_Category.objects.get(pk=pk)
        return render(request,'update_sub_cat.html',{'sub_cat':sub_cat})
    
    def post(self,request,pk):
        sub_cat=Sub_Category.objects.get(pk=pk)
        cat=Category.objects.get(cat_name=sub_cat.cat.cat_name)
        sub_cat.cat=cat
        sub_cat.sub_cat_name=request.POST['sub_cat_name']
        sub_cat.save()
        return redirect('admin_sub_cat')
    
class AddNewView(View):
    def post(self,request,pk):
        cat=Category.objects.get(pk=pk)
        sub_cat=Sub_Category.objects.create(cat=cat,sub_cat_name=request.POST['sub_cat_name'])
        return redirect('add_sub_cat',pk=pk)
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Blogs <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class AllBlogView(View):
    def get(self,request):
        blogs=Blog.objects.all()
        return render(request,'all_blogs.html',{'blogs':blogs})
    
class AdminSearchBlogView(View):
    def post(self,request):
        text=request.POST['text']
        blog=Blog.objects.filter(title__contains=text)
        return render(request,'all_blogs.html',{'blogs':blog,'text':text})

class AddBlogView(View):
    def get(self,request):
        form=BlogForm()
        return render(request,'admin_add_blog.html',{'form':form})
    
    def post(self,request):
        form=BlogForm()
        blog=Blog.objects.create(
            title=request.POST['title'],
            image=request.FILES['image'],
            desc=request.POST['desc']
            )
        
        # f = open(f"{blog.title}.html",'w')
        # f.write(f"<center><h1></h1>{blog.title}</center><br><hr><br>")
        # f.write(f"<img src={blog.image}/><br><br>")
        # f.write(f"<p>{blog.desc}</p>")
        # f.close()
        
        # pdf.from_string(blog.title+'\n\n',f"{blog.title}.pdf")
        # pdf.from_string(blog.desc,f"{blog.title}.pdf")
        
        # blog.blog_pdf=f"{blog.title}.pdf"
        # blog.save()
        
        msg="Blog Added Successfully !"
        return render(request,'admin_add_blog.html',{'form':form,'msg':msg})
    
class EditBlogView(View):
    def get(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        form = BlogForm()
        return render(request,'admin_edit_blog.html',{'blog':blog,'form':form})
    
    def post(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        blog.title=request.POST['title']
        try:
            blog.image=request.FILES['image']
        except:
            pass
        blog.desc=request.POST['desc']
        blog.save()
        return redirect('all_blogs')

class DeleteBlogView(View):
    def get(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        blog.delete()
        return redirect('all_blogs')
    
# class DownloadView(View):
#     def get(self,request,pk):
#         blog=Blog.objects.get(pk=pk)
#         pdf.from_file('dash_app\\templates\\admin_blog_single.html','C:\\Users\\HEENA\\OneDrive\\Desktop\\blog.pdf')        
#         return redirect('all_blogs')
        
# class BlogSingleView(View):
#     def get(self,request,pk):
#         blog=Blog.objects.get(pk=pk)
#         return render(request,'admin_blog_single.html',{'blog':blog})
        
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
