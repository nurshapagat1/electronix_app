from django.contrib import admin
from .models import Product, Customer, Order, OrderProduct, Review, FounderInfo, ReviewLike

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'created_date')
    list_filter = ('is_active',)
    search_fields = ('name', 'details')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_date')
    search_fields = ('user__username', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_date')
    list_filter = ('status',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'rating', 'is_approved')
    list_filter = ('is_approved', 'rating')

@admin.register(FounderInfo)
class FounderInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_active')

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('review', 'customer', 'created_date')