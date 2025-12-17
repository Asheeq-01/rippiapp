from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

class OneTimePassword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps"
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    resent_count = models.PositiveIntegerField(default=0)
    last_sent_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_otp(cls, user, ttl_minutes=10):
        """Generate a new OTP"""
        code = f"{random.randint(0, 999999):06d}"
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=ttl_minutes)
        )

    def is_valid(self):
        """Check if OTP is still valid"""
        return (
            not self.is_used
            and timezone.now() <= self.expires_at
            and self.attempts < 5
        )

    def mark_used(self):
        """Mark OTP as used"""
        self.is_used = True
        self.save(update_fields=["is_used"])

    def __str__(self):
        return f"OTP {self.code} for {self.user.username}"
    
    
    
class Category_model(models.Model):
    name=models.CharField(("category name"), max_length=50)
    image=models.ImageField(("upload image"), upload_to='images', height_field=None, width_field=None, max_length=None)
    descriptions=models.TextField(("description"))
    
    def __str__(self):
      return self.name



class Product_model(models.Model):
    name=models.CharField(("product name"), max_length=50)
    image=models.ImageField(("upload image"), upload_to='images', height_field=None, width_field=None, max_length=None)
    descriptions=models.TextField(("description"))
    price=models.FloatField(("price"))
    stock=models.IntegerField(("stock"))
    available=models.BooleanField(("available"),default=True)
    created=models.DateTimeField(("created"),auto_now_add=True)
    updated=models.DateTimeField(("updated"),auto_now_add=True)
    category=models.ForeignKey(Category_model,on_delete=models.CASCADE,related_name='category')
    
    def __str__(self):
      return self.name
  

class Product_different_model(models.Model):
    name=models.CharField(("product name"), max_length=50)
    image=models.ImageField(("upload image"), upload_to='images', height_field=None, width_field=None, max_length=None)
    descriptions=models.TextField(("description"))
    price=models.FloatField(("price"))
    stock=models.IntegerField(("stock"))
    available=models.BooleanField(("available"),default=True)
    created=models.DateTimeField(("created"),auto_now_add=True)
    updated=models.DateTimeField(("updated"),auto_now_add=True)
    
    
    def __str__(self):
      return self.name