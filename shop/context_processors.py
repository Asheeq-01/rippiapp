from random import sample
from .models import Category_model,Product_model

def random_category_products(request):
    all_products = list(Product_model.objects.filter(available=True))
    random_products = sample(all_products, min(len(all_products), 6))

    return {
        'random_products': random_products
    }
