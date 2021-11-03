from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    name =  models.CharField(max_length=25)
    sub_category = models.ManyToManyField('self',blank=True)
    is_main = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.SET_NULL, null=True)
    detail = models.CharField(max_length=150)
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product/")
    is_published = models.BooleanField(default=False)
    publish_time = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.is_published = True
        self.publish_time = timezone.now()
        self.save()

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('shop:products-detail',kwargs={'slug':self.slug})

    def __str__(self):
        return f'{self.name}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_cart(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(Cart,related_name='order_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_order(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.total_cart()
        return total

    def __str__(self):
        return f'{self.user.username} order {self.pk}'

class SuccessfulPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderitems = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}'


class ProductFilter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    price1 = models.IntegerField(blank=True, null=True)
    price2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.price1}-{self.price2}'

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    list = models.ManyToManyField(Product)
    slug = models.SlugField(allow_unicode=True,unique=True,blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.user}'

class ProductComment(models.Model):
    class Meta:
        ordering = ('is_approved','-creating_date')

    author = models.CharField(max_length=30)
    text = models.TextField(max_length=200)
    email = models.EmailField()
    # Verify_exists???
    website = models.URLField(blank=True)
    product = models.ForeignKey(Product, related_name='product_comments' ,on_delete=models.CASCADE)
    creating_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def get_absolute_url(self):
        return reverse('shop:products-view')

    def __str__(self):
        return self.text
