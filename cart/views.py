from django.shortcuts import render,redirect
from django.views import View
from shop.models import Product_different_model,Product_model
from .models import Cart_model

class Add_to_cart(View):
    def get(self,request,i):
        p=Product_model.objects.get(id=i)
        u=request.user
        try:
            c=Cart_model.objects.create(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart_model.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('shop:get_product_details',i=i)
