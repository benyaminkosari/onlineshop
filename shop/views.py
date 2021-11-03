from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from . import models
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import PriceFilterForm, ProductCommentForm


User = get_user_model()

class ProductList(generic.ListView):
    model = models.Product
    template_name = 'shop/shop.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            a = get_object_or_404(models.ProductFilter,user=self.request.user)
            qs = queryset.filter(price__range=(a.price1,a.price2))
            a.delete()
            return qs.filter(is_published=True).order_by('-publish_time')
        except:
            pass
        return queryset.filter(is_published=True).order_by('-publish_time')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # from django.db.models import Q
        # print("\n\n\n")
        # print("Puma")
        # print(models.Product.objects.filter(category__name__iexact="Puma"))
        # print("\nNot Published")
        # print(models.Product.objects.filter(is_published=True))
        # print("\n Puma.published")
        # print(models.Product.objects.filter(category__name__iexact="Puma").filter(is_published=True))
        # print("\n Puma , Published")
        # print(models.Product.objects.filter(Q(category__name__iexact="Puma")|Q(is_published=True)))
        # print("\n\n\n")
        try:
            context['main_categories'] = models.Category.objects.filter(is_main=True)
        except:
            pass
        context['price_filter_form'] = PriceFilterForm()
        return context

    def post(self, *args, **kwargs):
        if 'price1' in self.request.POST:
            form = PriceFilterForm(self.request.POST)
            if form.is_valid():
                self.object  = form.save(commit=False)
                self.object.user = self.request.user
                form.save(commit=True)
            else:
                print("*** INVALID FORM ***")
        return redirect('shop:products-view')



class ProductDetail(LoginRequiredMixin,generic.DetailView):
    model = models.Product
    template_name = 'shop/product-details.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['product_comment_form'] = ProductCommentForm()
        try:
            product = get_object_or_404(models.Product,slug=self.kwargs.get('slug'),is_published=True)
            d = models.Cart.objects.filter(user=self.request.user,product=product)
            context['quantity_by_product'] = d[0].quantity
        except:
            pass
        try:
            context['main_categories'] = models.Category.objects.filter(is_main=True)
        except:
            pass
        try:
            this_product = get_object_or_404(models.Product,slug=self.kwargs.get('slug'),is_published=True)
            pdc = models.Product.objects.filter(category__sub_category__name__exact=this_product.category.sub_category.all()[0].name).order_by('-publish_time')
            context['related_products'] = pdc[:4]
        except:
            pass
        return context

    def post(self, *args, **kwargs):
        form = ProductCommentForm(self.request.POST)
        if form.is_valid():
            productcomment = form.save(commit=False)
            product = get_object_or_404(models.Product,slug=self.kwargs['slug'])
            productcomment.product = product
            form.save(commit=True)
        else:
            print("*** INVALID FORM ***")
        return redirect('shop:products-detail', slug=self.kwargs['slug'])


class CreateProduct(LoginRequiredMixin,generic.CreateView):
    model = models.Product
    fields = ('name','category','detail','price','image')

    # def form_valid(self,form):
    #     self.object  = form.save(commit=False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)

class DeleteProduct(LoginRequiredMixin,generic.DeleteView):
    model = models.Product
    success_url = reverse_lazy('shop:products-view')

    def delete(self,*args,**kwargs):
        print('Product Deleted')
        return super().delete(*args,**kwargs)

class CategoryView(generic.DetailView):
    model = models.Category
    template_name = 'shop/category.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['main_categories'] = models.Category.objects.filter(is_main=True)
        except:
            pass
        return context

class WishListView(generic.DetailView):
    model = models.Wishlist
    template_name = 'shop/wishlist.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['main_categories'] = models.Category.objects.filter(is_main=True)
        except:
            pass
        return context

class CartList(LoginRequiredMixin,generic.ListView):
    model = models.Cart

class CartDetail(LoginRequiredMixin,generic.DetailView):
    model = models.Cart

class OrderList(LoginRequiredMixin,generic.ListView):
    model = models.Order

class OrderDetail(LoginRequiredMixin,generic.DetailView):
    model = models.Order
    template_name = 'shop/cart.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.request.user)

class PublishList(LoginRequiredMixin,generic.ListView):
    model = models.Product
    template_name = 'shop/publish.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=False)

class PublishView(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('shop:publish-view')

    def get(self,*args,**kwargs):
        product = get_object_or_404(models.Product,slug=self.kwargs.get('slug'))
        product.publish()
        return super().get(self.request,*args,**kwargs)

class CheckoutTemplateView(generic.TemplateView):
    template_name = 'shop/checkout.html'


@login_required
def PaymentView(request,pk):
    order = get_object_or_404(models.Order,pk=pk)
    sp, spc = models.SuccessfulPayment.objects.get_or_create(user=request.user)
    text = ''
    for i in order.orderitems.all():
        text += str(i)+'\n'
    text += '--------------\n'
    text += sp.orderitems
    sp.orderitems = text
    sp.save()
    models.Cart.objects.filter(user=request.user).delete()
    order.delete()
    return redirect('shop:orders-view')

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(models.Product,slug=slug,is_published=True)
    order_item,created_cart = models.Cart.objects.get_or_create(product=product,user=request.user)
    order_qs,created_order = models.Order.objects.get_or_create(user=request.user)
    # IS THERE AN ORDER?:
    if not created_order:
        # IS THERE A CART WITH THIS PRODUCT
        if order_qs.orderitems.filter(product__slug=product.slug).exists():
            print("add to cart ", order_item, " reuslt quantity = ", order_item.quantity+1)
            order_item.quantity += 1
            order_item.save()
        # THERE IS AN ORDER BUT NO SAME CART
        else:
            order_qs.orderitems.add(order_item)
            print("New item (", order_item ,") added to cart and now add to order ",order_qs)
    # THERE IS NO CART IN ACTIVE ORDER:
    else:
        order_qs.orderitems.add(order_item)
        print("New order (", order_qs ,") created and item (", order_item ,") added to orderitems")
    return redirect('shop:orders-detail',pk=order_qs.pk)

@login_required
def decrease_from_cart(request,slug):
    product = get_object_or_404(models.Product,slug=slug,is_published=True)
    order_item = get_object_or_404(models.Cart, product=product,user=request.user)
    order_qs = get_object_or_404(models.Order,user=request.user)

    # IS THERE A CART WITH THIS PRODUCT WITH QUANTITY OF MORE THAN 1
    if not order_qs.orderitems.filter(product__slug=product.slug).filter(quantity__lte=1).exists():
        print("decrease from cart ", order_item, " reuslt quantity = ", order_item.quantity-1)
        order_item.quantity -= 1
        order_item.save()
    # CART WITH THIS PRODUCT WITH QUANTITY OF 1
    else:
        print("Product quantity was one and the cart is deleted")
        order_item.delete()
        # IS THERE JUST ONE CART?:
        if (models.Cart.objects.filter(user=request.user).count() == 0):
            print("There was only one cart and the order is deleted")
            order_qs.delete()
            return redirect('shop:orders-view')
    return redirect('shop:orders-detail',pk=order_qs.pk)

@login_required
def remove_from_cart(request,slug):
    product = get_object_or_404(models.Product,slug=slug,is_published=True)
    models.Cart.objects.filter(user=request.user,product=product).delete()
    order = get_object_or_404(models.Order,user=request.user)
    # order = models.Order.objects.filter(user=request.user)
    if (models.Cart.objects.filter(user=request.user).count() == 0):
        order.delete()
        return redirect('shop:products-view')
    return redirect('shop:orders-detail', pk=order.pk)

@login_required
def add_to_wishlist(request,slug):
    product = get_object_or_404(models.Product,slug=slug,is_published=True)
    wishlist_item,is_created = models.Wishlist.objects.get_or_create(user=request.user)
    wishlist_item.list.add(product)
    return redirect('shop:wishlist-view', slug=request.user.username)

@login_required
def remove_from_wishlist(request,slug):
    wishlist_item = get_object_or_404(models.Wishlist, user=request.user)
    wishlist_item.list.remove(get_object_or_404(wishlist_item.list,slug__exact=slug))
    return redirect('shop:wishlist-view', slug=request.user.username)
