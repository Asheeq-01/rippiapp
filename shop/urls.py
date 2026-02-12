from django.urls import path
from shop import views

app_name='shop'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('verify-otp/', views.VerifyOTP.as_view(), name='verify-otp'),
    path('resend-otp/', views.ResendOTP.as_view(), name='resend-otp'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('product/<int:i>',views.Product.as_view(),name="product"),
    path('get-product-details/<int:i>/',views.Get_product_details.as_view(),name="get_product_details"),
   
    path('admin-home/', views.Admin_home.as_view(), name='admin-home'),
]
