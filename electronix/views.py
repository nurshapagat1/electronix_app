from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from allauth.account.views import LoginView, SignupView
from .models import Product, Customer, Order, OrderProduct, Review, FounderInfo, ReviewLike
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.http import HttpResponse

# --- Forms ---
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter review title'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Share your experience...', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'form-input'})
        }
        labels = {
            'title': 'Review Title',
            'content': 'Your Review',
            'rating': 'Rating'
        }

# --- Helper function ---
def get_or_create_customer(user):
    """Helper function to get or create customer for user"""
    customer, created = Customer.objects.get_or_create(user=user)
    return customer

# --- Basic Views ---
def main(request):
    return render(request, "electronics/first.html")

def forgotpass(request):
    return render(request, "electronics/forgotpass.html")

@login_required(login_url='account_login')
def laptops(request):
    products = Product.objects.filter(is_active=True).order_by('-created_date')
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()

    if order:
        order_items = order.order_items.all()
        order_items_dict = {item.product.id: item for item in order_items}
        for product in products:
            product.cart_item = order_items_dict.get(product.id)
    else:
        for product in products:
            product.cart_item = None

    cart_item_count = order.order_items.count() if order else 0

    return render(request, "electronics/products_page.html", {
        'products': products,
        'cart_item_count': cart_item_count
    })

def about_us(request):
    founders = FounderInfo.objects.filter(is_active=True).order_by('created_date')
    total_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.filter(status__in=['processing', 'shipped', 'completed']).count()
    total_reviews = Review.objects.filter(is_approved=True).count()
    
    context = {
        'founders': founders,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
    }
    return render(request, 'electronics/about_us.html', context)

# --- Cart and Order Logic ---
@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_or_create_customer(request.user)
    
    order, created = Order.objects.get_or_create(
        customer=customer, 
        status='cart',
        defaults={'total_price': 0}
    )
    
    order_item, item_created = OrderProduct.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )
    
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    
    order.update_total() # Calling the method from models.py
    messages.success(request, f"✅ {product.name} added to cart!")
    return redirect('laptops-list')

@login_required
def update_cart(request, product_id, action):
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()
    if not order:
        order = Order.objects.create(customer=customer, status='cart', total_price=0)
    
    product = get_object_or_404(Product, id=product_id)
    order_item, created = OrderProduct.objects.get_or_create(
        order=order, product=product, defaults={'quantity': 1, 'price': product.price}
    )
    
    if action == 'add':
        order_item.quantity += 1
        order_item.save()
        messages.success(request, f"➕ Added {product.name}")
    elif action == 'subtract':
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            messages.success(request, f"➖ Removed {product.name}")
        else:
            order_item.delete()
            messages.success(request, f"🗑️ Removed {product.name}")
    
    if order.order_items.count() == 0:
        order.delete()
    else:
        order.update_total()
    return redirect('laptops-list')

@login_required
def update_cart_in_cart(request, product_id, action):
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()
    product = get_object_or_404(Product, id=product_id)
    order_item = get_object_or_404(OrderProduct, order=order, product=product)
    
    if action == 'add':
        order_item.quantity += 1
        order_item.save()
    elif action == 'subtract':
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
    
    if order.order_items.count() == 0:
        order.delete()
    else:
        order.update_total()
    return redirect('electronics-cart')

@login_required
def cart(request):
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()
    if not order or order.order_items.count() == 0:
        return render(request, 'electronics/cart.html', {'empty_cart': True})
    
    items = order.order_items.all()
    total_items = sum(item.quantity for item in items)
    return render(request, 'electronics/cart.html', {
        'order': order, 'items': items, 'total_items': total_items, 'empty_cart': False
    })

@login_required
def remove_from_cart(request, item_id):
    customer = get_or_create_customer(request.user)
    try:
        order_item = OrderProduct.objects.get(id=item_id, order__customer=customer)
        order = order_item.order
        order_item.delete()
        if order.order_items.count() == 0:
            order.delete()
        else:
            order.update_total()
        messages.success(request, "🗑️ Item removed")
    except OrderProduct.DoesNotExist:
        messages.error(request, "Item not found")
    return redirect('electronics-cart')

@login_required
def clear_cart(request):
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()
    if order:
        order.delete()
        messages.success(request, "🗑️ Cart cleared")
    return redirect('electronics-cart')

@login_required
def checkout(request):
    customer = get_or_create_customer(request.user)
    order = Order.objects.filter(customer=customer, status='cart').first()
    if not order or order.order_items.count() == 0:
        return redirect('electronics-cart')
    if request.method == 'POST':
        order.status = 'pending'
        order.save()
        return redirect('order_success')
    return render(request, 'electronics/checkout.html', {'order': order})

@login_required
def order_success(request):
    return render(request, 'electronics/order_success.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(is_active=True).exclude(id=product.id).order_by('?')[:4]
    return render(request, 'electronics/detail.html', {'product': product, 'related_products': related_products})

# --- Reviews Views ---
class SubmitReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'electronics/review_form.html'
    success_url = reverse_lazy('review_thanks')
    def form_valid(self, form):
        form.instance.customer = get_or_create_customer(self.request.user)
        return super().form_valid(form)

class ReviewThanksView(TemplateView):
    template_name = 'electronics/review_thanks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Thank you! Your review has been submitted."
        return context

class ListReviewsView(ListView):
    model = Review
    template_name = 'electronics/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    def get_queryset(self):
        return Review.objects.filter(is_approved=True).order_by('-created_date')

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'electronics/review_detail.html'
    context_object_name = 'review'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = get_or_create_customer(self.request.user)
            context['has_liked'] = ReviewLike.objects.filter(review=self.object, customer=customer).exists()
        else:
            context['has_liked'] = False
        return context

@login_required
def toggle_review_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    customer = get_or_create_customer(request.user)
    like, created = ReviewLike.objects.get_or_create(review=review, customer=customer)
    if not created:
        like.delete()
        messages.info(request, "Removed like")
    else:
        messages.success(request, "Liked review!")
    review.likes = ReviewLike.objects.filter(review=review).count()
    review.save()
    return redirect('review_detail', pk=review_id)

# --- Account / Social Views ---
@login_required
def google_connection_view(request):
    google_connected = request.user.socialaccount_set.filter(provider="google").exists()
    return render(request, "socialaccount/connections.html", {"google_connected": google_connected})

@login_required
def socialaccount_connections(request):
    messages.info(request, "🔧 Account Connections coming soon!")
    emailaddresses = request.user.emailaddress_set.all() if hasattr(request.user, 'emailaddress_set') else []
    return render(request, "electronics/email_addresses.html", {"emailaddresses": emailaddresses})

class CustomSignupView(SignupView):
    success_url = reverse_lazy('laptops-list')
    def form_valid(self, form):
        response = super().form_valid(form)
        get_or_create_customer(self.user)
        return response

def debug_google_url(request):
    return HttpResponse("Debug: Google callback check.")
def create_admin_account(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'YourPassword123')
        return HttpResponse("Admin created successfully!")
    return HttpResponse("Admin already exists.")