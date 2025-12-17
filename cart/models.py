from django.db import models
from django.contrib.auth.models import User
from shop.models import Product_model,Product_different_model

class Cart_model(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product_model, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.product*self.quantity
