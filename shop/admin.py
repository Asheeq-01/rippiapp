from django.contrib import admin
from .models import OneTimePassword,Category_model,Product_model,Product_different_model


admin.site.register(Category_model)
admin.site.register(Product_model)
admin.site.register(Product_different_model)