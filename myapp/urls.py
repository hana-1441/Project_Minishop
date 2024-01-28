from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('about/',AboutView.as_view(),name='about'),
    path('blog/',BlogView.as_view(),name='blog'),
    path('blog_single/<int:pk>/',SingleBlogView.as_view(),name='blog_single'),
    path('post_comment/<int:pk>/',PostCommentView.as_view(),name='post_comment'),
    path('search_blog/',SearchBlogView.as_view(),name='search_blog'),
    
    #====================CART=================
    path('cart/',CartView.as_view(),name='cart'),
    path('add_to_cart/<int:pk>/',AddCartView.as_view(),name='add_to_cart'),
    path('del_from_cart/<int:pk>/',DelCartView.as_view(),name='del_from_cart'),
    path('change_qty/<int:pk>/',ChangeQtyView.as_view(),name='change_qty'),
    
    
    #===============Payment Orders=====================
    path('success',SuccessView.as_view(),name='success'),
    path('order_history',OrderHistoryView.as_view(),name='order_history'),
    
    #==================WISHLIST=======================
    path('wishlist/',WishlistView.as_view(),name='wishlist'),
    path('add_to_wishlist/<int:pk>/',AddWishlistView.as_view(),name='add_to_wishlist'),
    path('del_from_wishlist/<int:pk>/',DelWishlistView.as_view(),name='del_from_wishlist'),
    
    #=====================PRODUCTS==========================
    path('prod_detail/<int:pk>/',ProdDetailView.as_view(),name='prod_detail'),
    
    path('contact/',ContactView.as_view(),name='contact'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('signin/',SignInView.as_view(),name='signin'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('forgot_pswd/',ForgotPswdView.as_view(),name='forgot_pswd'),
    path('verify_otp',VerifyOtpView.as_view(),name='verify_otp'),
    path('change_pswd/',ChangePswdView.as_view(),name='change_pswd'),
    path('update_pswd/',UpdatePswdView.as_view(),name='update_pswd'),
    
    #===================== SHOP ===========================
    path('shop/',ShopView.as_view(),name='shop'),
    path('cat_filter/<int:pk>/',CatFilterView.as_view(),name='cat_filter'),
    path('sub_cat_filter/<int:pk>/<int:id>/',SubCatFilter.as_view(),name='sub_cat_filter'),
    path('search_prod/',SearchProdView.as_view(),name='search_prod'),
    
    # path('whatsapp_share/<int:pk>/',WhastappShareView.as_view(),name="whatsapp_share"),
]
