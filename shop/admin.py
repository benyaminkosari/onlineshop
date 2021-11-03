from django.contrib import admin
from . import models

admin.site.register(models.Product)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.SuccessfulPayment)
admin.site.register(models.Category)
admin.site.register(models.ProductFilter)
admin.site.register(models.Wishlist)
admin.site.register(models.ProductComment)
