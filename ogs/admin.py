from django.contrib import admin

from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    ContactMessage,
    EmailOTP,
    Coupon,
    Wishlist,
    Address,
    Recipe,
    RecipeIngredient,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "is_active", "product_count")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "mrp", "stock", "available", "brand", "created_at")
    list_filter = ("available", "category", "brand", "organic")
    search_fields = ("name", "brand", "description", "flavour")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "stock", "available")
    ordering = ("-created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("subtotal",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone", "total_amount", "payment_method", "payment_status", "status", "created_at")
    list_filter = ("status", "payment_status", "payment_method", "created_at")
    search_fields = ("id", "full_name", "phone", "address", "user__username", "user__email")
    list_editable = ("status", "payment_status")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "sentiment", "verified_purchase", "created_at")
    list_filter = ("rating", "sentiment", "verified_purchase", "created_at")
    search_fields = ("product__name", "user__username", "review")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "discount", "minimum_amount", "expiry_date", "active")
    list_filter = ("active", "discount_type", "expiry_date")
    search_fields = ("code",)
    list_editable = ("active",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone", "city", "address_type", "is_default")
    list_filter = ("address_type", "is_default", "city")
    search_fields = ("full_name", "phone", "address", "city", "user__username")


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "prep_time", "servings", "calories_per_serving", "health_tag")
    search_fields = ("name", "description")
    inlines = [RecipeIngredientInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    search_fields = ("name", "email", "subject")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)


admin.site.register(EmailOTP)
admin.site.register(Wishlist)