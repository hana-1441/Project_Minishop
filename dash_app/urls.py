from django.urls import path
from dash_app.views import *

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('home/',HomeView.as_view(),name='home'),
    path('signout/',SignoutView.as_view(),name='signout'),
    
    # ======================= PRODUCTS ========================
    path('admin_products/',ProductView.as_view(),name='admin_products'),
    path('admin_add_product/',AddProductView.as_view(),name='admin_add_product'),
    path('del_prod/<int:pk>/',DelProdView.as_view(),name='del_prod'),
    path('update_prod/<int:pk>/',UpdateProdView.as_view(),name='update_prod'),
    
    # ======================= CATEGORY ========================
    path('admin_cat/',CatView.as_view(),name='admin_cat'),
    path('add_cat/',AddCatView.as_view(),name='add_cat'),
    path('del_cat/<int:pk>/',DelCatView.as_view(),name='del_cat'),
    path('update_cat/<int:pk>/',UpdateCatView.as_view(),name='update_cat'),
    
    # ======================= SUB CATEGORY ========================
    path('admin_sub_cat/',SubCatView.as_view(),name='admin_sub_cat'),
    path('add_sub_cat/<int:pk>',AddSubCatView.as_view(),name='add_sub_cat'),
    path('update_sub_cat/<int:pk>/',UpdateSubCatView.as_view(),name='update_sub_cat'),
    path('del_sub_cat/<int:pk>/',DelSubCatView.as_view(),name='del_sub_cat'),
    path('add_new/<int:pk>/',AddNewView.as_view(),name='add_new'),
    
    # ========================= FILTER ==============================
    path('filter/',FilterView.as_view(),name='filter'),
    
    # =========================== BLOG ================================
    path("all_blogs/", AllBlogView.as_view(), name="all_blogs"),
    path('admin_add_blog/',AddBlogView.as_view(),name='admin_add_blog'),
    path('admin_edit_blog/<int:pk>/',EditBlogView.as_view(),name='admin_edit_blog'),
    path('admin_delete_blog/<int:pk>/',DeleteBlogView.as_view(),name='admin_delete_blog'),
    path('admin_search_blog/',AdminSearchBlogView.as_view(),name='admin_search_blog'),
    # path('download_blog/<int:pk>/',DownloadView.as_view(),name='download_blog'),
    # path('admin_blog_single/<int:pk>/',BlogSingleView.as_view(),name='admin_blog_single'),
]
