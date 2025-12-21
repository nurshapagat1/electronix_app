from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='customers/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Cart'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"
    
    # ДОБАВЬТЕ ЭТОТ МЕТОД:
    def update_total(self):
        """Calculate and update total price from order items"""
        total = sum(item.quantity * item.price for item in self.order_items.all())
        self.total_price = total
        self.save()
        return total
    
    # ДОБАВЬТЕ ЭТОТ PROPERTY:
    @property
    def item_count(self):
        """Total number of items in order"""
        return sum(item.quantity for item in self.order_items.all())


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    @property
    def subtotal(self):
        """Вычисляемое поле для суммы позиции"""
        return self.quantity * self.price
# NEW: Модель для отзывов/обратной связи
class Review(models.Model):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    likes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} by {self.customer.user.username}"

# NEW: Модель для информации о Founder/About Us
class FounderInfo(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='founders/')
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# NEW: Модель для подсчета лайков отзывов
class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_likes')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'customer']  # Один лайк на отзыв от пользователя
    
    def __str__(self):
        return f"Like for {self.review.title} by {self.customer.user.username}"