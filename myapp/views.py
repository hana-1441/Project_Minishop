from django.shortcuts import render,redirect
from django.views import View
from .models import *
from dash_app.models import *
import requests,random
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.core.mail import EmailMessage
# from twilio.rest import Client


class IndexView(View):
    def get(self,request):
        recent_prods=Product.objects.all().order_by('-id')[:8]
        return render(request,'index.html',{'recent_prods':recent_prods})

class AboutView(View):
    def get(self,request):
        return render(request,'about.html')
    
class BlogView(View):
    def get(self,request):
        blogs=Blog.objects.all()
        recent_blogs=Blog.objects.all().order_by('-id')[:5] # to retrive last 5 records
        return render(request,'blog.html',{'blogs':blogs,'recent_blogs':recent_blogs})
    
class SingleBlogView(View):
    def get(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        recent_blogs=Blog.objects.all().order_by('-id')[:5] # to retrive last 5 records
        comments=Comment.objects.filter(blog=blog)
        count=0
        for i in comments:
            count+=1
        return render(request,'blog_single.html',{'blog':blog,'recent_blogs':recent_blogs,'comments':comments,'count':count})
    
class PostCommentView(View):
    def post(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        Comment.objects.create(blog=blog,name=request.POST['name'],email=request.POST['email'],msg=request.POST['msg'])
        return redirect('blog_single',pk=pk)
    
class SearchBlogView(View):
    def post(self,request):
        text=request.POST['text']
        blog=Blog.objects.filter(title__contains=text)
        recent_blogs=Blog.objects.all().order_by('-id')[:5] # to retrive last 5 records
        return render(request,'blog.html',{'blogs':blog,'recent_blogs':recent_blogs})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Whatsapp Share On Product : ERROR <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# class WhastappShareView(View):
#     def get(self,request,pk):
#         user=User.objects.get(email=request.session['email'])
#         account_sid = 'AC42e5d38688517ee3767221b7399959c2'
#         auth_token = '58397f8942b53c8797573e657f491141'
        
#         from_whatsapp_number = 'whatsapp:+17752988586'  # Replace with your Twilio WhatsApp number

#         client = Client(account_sid, auth_token)
        
#         prod=Product.objects.get(pk=pk)
        
#         media_url = '{{ prod.image.url }}'
        
#         # Construct the message
#         message = client.messages.create(
#             body=f"Check out this product: {prod.pname}\nPrice: ${prod.price}",
#             from_=from_whatsapp_number,
#             to='whatsapp:{{ user.contact }}',  # Replace with the user's WhatsApp number
#             media_url=[media_url]
#         )
        
#         return HttpResponse(f"WhatsApp message sent with SID: {message.sid}")
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PROD <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class ProdDetailView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        
        try:
            user=User.objects.get(email=request.session['email'])
            cart=Cart.objects.get(user=user,prod=prod)
            return render(request,'prod_detail.html',{'prod':prod,'cart':cart,'user':user})
        except:
            return render(request,'prod_detail.html',{'prod':prod})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CART <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class CartView(View):
    def get(self,request):
        request.session['cart_count']=0
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user)
        global net_price
        net_price=0
        for i in cart:
            request.session['cart_count']+=1
            net_price+=i.total
            
        if net_price:
            client = razorpay.Client(auth = (settings.KEY_ID, settings.KEY_SECRET))
            payments=client.order.create({'amount':net_price*100, 'currency':'INR', 'payment_capture':1})
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",payments)

            for i in cart:
                i.razorpay_order_id=payments['id']
                i.save()

            return render(request,'cart.html',{'cart':cart,'net_price':net_price,'amount':net_price*100,'user':user,'payments':payments})
        else:
            return render(request,'cart.html',{'cart':cart,'net_price':net_price,'user':user})
    
class AddCartView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        user=User.objects.get(email=request.session['email'])
        Cart.objects.create(
            user=user,
            prod=prod,
            total=prod.price
        )
        return redirect('cart')
    
class DelCartView(View):
    def get(self,request,pk):
        cart=Cart.objects.get(pk=pk)
        cart.delete()
        return redirect('cart')
    
class ChangeQtyView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.get(user=user,prod=prod)
        cart.qty=request.GET['qty']
        cart.total=int(cart.qty)*int(cart.prod.price)
        cart.save()
        return redirect('cart')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Payment ORDER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class SuccessView(View):
    def get(self,request):
        user=User.objects.get(email=request.session['email'])
        carts=Cart.objects.filter(user=user)
        data=[]
        for i in carts:
            i.payment_status=True
            data.append(i)
            i.delete()
            
        Order.objects.create(user=user,data=data)
        return render(request,'callback.html',{'data':data,'net_price':net_price})

class OrderHistoryView(View):
    def get(self,request):
        user=User.objects.get(email=request.session['email'])
        orders=Order.objects.filter(user=user)
        return render(request,'order_history.html',{'orders':orders})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WISHLIST <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class WishlistView(View):
    def get(self,request):
        request.session['wlist_count']=0
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.values_list('prod_id',flat=True)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",cart)
        wlist=Wishlist.objects.filter(user=user)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>wlist : ")
        for i in wlist:
            print(i.prod.id)
        for i in wlist:
            request.session['wlist_count']+=1
        return render(request,'wishlist.html',{'wlist':wlist,'cart':cart})
    
class AddWishlistView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        user=User.objects.get(email=request.session['email'])
        Wishlist.objects.create(
            user=user,
            prod=prod,
            wlist_flag=True,
        )
        return redirect('wishlist')
    
class DelWishlistView(View):
    def get(self,request,pk):
        prod=Product.objects.get(pk=pk)
        wlist=Wishlist.objects.get(prod=prod)
        wlist.delete()
        return redirect('wishlist')
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   
    
class ContactView(View):
    def get(self,request):
        return render(request,'contact.html')
    
    def post(self,request):
        try:
            receiver = request.POST['email']
            mail_msg=f"Hello {receiver}, \nHope you are doing well. Here is my application for the vacancy in your company. please find the attachment.\nHave a Great Day ! \n\n--\nHeena Malek "
            email = EmailMessage('Application For Vacancy', mail_msg, settings.EMAIL_HOST_USER, [receiver,])
            email.attach_file('myapp/Python.pdf')
            print(">>>>>>>>>>>>>>>>>>>>>done ")
            email.send()
            
            return render(request,'contact.html')
        except:
            print("ERROR>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            return render(request,'contact.html')
    
class SignUpView(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        
        try:
            user=User.objects.get(email=request.POST['uemail'])
            emsg="User already Exist !!!"
            return render(request,'signup.html',{'emsg':emsg})
        except:
            OTP=random.randint(1000,9999)
            user=User.objects.create(
                name=request.POST.get('uname'),
                email=request.POST.get('uemail'),
                pswd=OTP,
                contact=request.POST.get('ucontact'),
                address=request.POST.get('uaddress'),
            )
            
            url = "https://www.fast2sms.com/dev/voice"

            querystring = {"authorization":"NVRk2utaImAEYPfci1W6KGZO9QXhel5vUjn7wDLd0s8xro3pBCZ1A2yptsi0uxNFqQVlXKmPEYJLhS5D","variables_values":OTP,"route":"otp","numbers":user.contact}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)
            
            msg="Registration Successful | You will receive OTP call for first Login"
            return render(request,'signin.html',{'msg':msg})
    
class SignInView(View):
    def get(self,request):
        return render(request,'signin.html')
    
    def post(self,request):
        try:
            user=User.objects.get(email=request.POST['uemail'],pswd=request.POST['upswd'])
            request.session['email']=user.email
            request.session['name']=user.name
            return render(request,'index.html')
        except:
            emsg="Email or Password Not Matched !!!"
            return render(request,'signin.html',{'emsg':emsg})
        
class LogoutView(View):
    def get(self,request):
        del request.session['email']
        del request.session['name']
        try:
            del request.session['cart_count']
        except:
            pass
        try:
            del request.session['wlist_count']
        except:
            pass
        return redirect('/signin/')
    
class ForgotPswdView(View):
    def get(self,request):
        return render(request,'forgot_pswd.html')
    
    def post(self,request):
        try:
            otp=random.randint(1000,9999)
            user=User.objects.get(email=request.POST['uemail'])
            subject = 'OTP for Forgot Password'
            message = f'Hi {user.name}, Your OTP is : '+str(otp)
            email_from = settings.EMAIL_HOST_USER            
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'verify_otp.html',{'email':user.email,'otp':str(otp)})
        except:
            msg="No Such User Exist !!!"
            return render(request,'forgot_pswd.html',{'emsg':msg})
    
class VerifyOtpView(View):
    def post(self,request):
        email=request.POST['uemail']
        otp=request.POST['otp']
        uotp=request.POST['uotp']
        
        if uotp==otp:
            return render(request,'change_pswd.html',{'email':email})
        else:
            msg="OTP doesn't Matched !!!"
            return render(request,'verify_otp.html',{'otp':otp,'email':email,'emsg':msg})
        
class ChangePswdView(View):
    def post(self,request):
        email=request.POST['uemail']
        np=request.POST['npswd']
        cnp=request.POST['cnpswd']
        
        if np==cnp:
            user=User.objects.get(email=email)
            user.pswd=np
            user.save()
            return render(request,'signin.html')
        else:
            msg="New & Confirm New Password Not Matched !!!"
            return render(request,'change_pswd.html',{'email':email,'emsg':msg})
        
class UpdatePswdView(View):
    def get(self,request):
        return render(request,'update_pswd.html')
    
    def post(self,request):
        user=User.objects.get(email=request.session['email'])
        ops=request.POST['ops']
        np=request.POST['np']
        cnp=request.POST['cnp']
        if ops==user.pswd and np==cnp:
            user.pswd=np
            user.save()
        return redirect('/logout/')
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Shop <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 
class ShopView(View):
    def get(self,request):
        cat=Category.objects.all()
        prods=Product.objects.all()
        wlist=Wishlist.objects.values_list('prod_id', flat=True)
        cart=Cart.objects.values_list('prod_id',flat=True)
        return render(request,'shop.html',{'cat':cat,'prods':prods,'wlist':wlist,'cart':cart})
    
class CatFilterView(View):
    def get(self,request,pk):
        main_cat=Category.objects.get(pk=pk)
        sub_cat=Sub_Category.objects.filter(cat=main_cat)
        cats=Category.objects.all()
        prods=Product.objects.filter(p_cat=main_cat)
        wlist=Wishlist.objects.values_list('prod_id', flat=True)
        cart=Cart.objects.values_list('prod_id',flat=True)
        return render(request,'shop.html',{'cat':cats,'main_cat':main_cat,'sub_cat':sub_cat,'prods':prods,'wlist':wlist,'cart':cart})
    
class SubCatFilter(View):
    def get(self,request,pk,id):
        main_cat=Category.objects.get(pk=id)
        sub_cat=Sub_Category.objects.get(pk=pk)
        prods=Product.objects.filter(p_sub_cat=sub_cat)
        cats=Category.objects.all()
        sub_cats=Sub_Category.objects.filter(cat=main_cat)
        wlist=Wishlist.objects.values_list('prod_id', flat=True)
        cart=Cart.objects.values_list('prod_id',flat=True)
        return render(request,'shop.html',{'cat':cats,'main_cat':main_cat,'sub_cat':sub_cats,'prods':prods,'wlist':wlist,'cart':cart})
    
class SearchProdView(View):
    def post(self,request):
        text=request.POST['text']
        prod=Product.objects.filter(pname__contains=text)
        cat=Category.objects.all()
        wlist=Wishlist.objects.values_list('prod_id', flat=True)
        cart=Cart.objects.values_list('prod_id',flat=True)
        return render(request,'shop.html',{'cat':cat,'prods':prod,'wlist':wlist,'cart':cart})
    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    
# value_list() : is a django built-in method to convert djangoqueryset to List
# It returns tuples when iterated over. 
# Each tuple contains the value from the respective field or expression passed into the values_list() call.

# flat = True : this gives single value instead of tuple