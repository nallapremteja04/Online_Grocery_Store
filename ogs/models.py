from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ===========================
# Category
# ===========================

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.product_set.filter(available=True).count()

    @property
    def image_url(self):
        if self.image:
            val = str(self.image)
            if val.startswith(('http://', 'https://')):
                return val
            try:
                return self.image.url
            except ValueError:
                if val and not val.startswith('/'):
                    return f'/static/ogs/images/{val}'
        return '/static/ogs/images/default_product.png'

    def __str__(self):
        return self.name


# ===========================
# Product
# ===========================

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.PositiveIntegerField(default=0)

    available = models.BooleanField(default=True)

    brand = models.CharField(max_length=100, default="Grocery Store")

    weight = models.CharField(max_length=50, default="500 g")

    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    expiry_date = models.CharField(max_length=100, blank=True)

    country_of_origin = models.CharField(max_length=100, default="India")

    organic = models.BooleanField(default=True)
    unit = models.CharField(
        max_length=30,
        default="Pack"
    )

    flavour = models.CharField(
        max_length=100,
        blank=True
    )

    storage_instruction = models.CharField(
        max_length=200,
        default="Keep Refrigerated"
    )

    manufacturer = models.CharField(
        max_length=200,
        default="Grocery Store Pvt Ltd"
    )

    calories = models.PositiveIntegerField(default=100)
    protein_g = models.DecimalField(max_digits=5, decimal_places=1, default=2.0)
    fat_g = models.DecimalField(max_digits=5, decimal_places=1, default=1.0)
    carbs_g = models.DecimalField(max_digits=5, decimal_places=1, default=15.0)
    health_score = models.PositiveIntegerField(default=80)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        if self.image:
            val = str(self.image)
            if val.startswith(('http://', 'https://')):
                return val
            try:
                return self.image.url
            except ValueError:
                if val and not val.startswith('/'):
                    return f'/static/ogs/images/{val}'
        return '/static/ogs/images/default_product.png'

    @property
    def discount_percentage(self):

        if self.mrp > self.price:

            return round(
                ((self.mrp - self.price) / self.mrp) * 100
            )

        return 0

    returnable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):

        reviews = self.review_set.all()

        if reviews.exists():

            return round(
                sum(r.rating for r in reviews) / reviews.count(),
                1
            )

        return 0

    def review_count(self):

        return self.review_set.count()

    def __str__(self):

        return self.name


# ===========================
# Cart
# ===========================

class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):

        return self.user.username


# ===========================
# Cart Item
# ===========================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):

        return self.product.price * self.quantity

    def __str__(self):

        return self.product.name


# ===========================
# Order
# ===========================

class Order(models.Model):

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Packed', 'Packed'),

        ('Shipped', 'Shipped'),

        ('Delivered', 'Delivered'),

        ('Cancelled', 'Cancelled'),

    ]

    PAYMENT_STATUS = [

        ('Pending', 'Pending'),

        ('Paid', 'Paid'),

        ('Failed', 'Failed'),

        ('Refunded', 'Refunded'),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=50)

    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(max_length=30)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    razorpay_order_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    expected_delivery = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Order #{self.id}"


# ===========================
# Order Item
# ===========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):

        return self.quantity * self.price

    def __str__(self):

        return f"{self.product.name} ({self.quantity})"


# ===========================
# Review
# ===========================

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField()

    review = models.TextField()
    sentiment = models.CharField(
    max_length=20,
    default="Neutral"
    )

    image = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True
    )

    verified_purchase = models.BooleanField(default=False)

    helpful = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        unique_together = ("product", "user")

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"

# ===========================
# Wishlist
# ===========================

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# ===========================
# Coupon
# ===========================

class Coupon(models.Model):

    DISCOUNT_TYPE = [

        ("Flat", "Flat"),

        ("Percentage", "Percentage"),

    ]

    code = models.CharField(
        max_length=20,
        unique=True
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    expiry_date = models.DateField()

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

# ===========================
# Address
# ===========================

class Address(models.Model):

    ADDRESS_TYPE = [
        ("Home", "Home"),
        ("Office", "Office"),
        ("Hostel", "Hostel"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    pincode = models.CharField(max_length=10)

    landmark = models.CharField(
        max_length=100,
        blank=True
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE,
        default="Home"
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"
    
# ===========================
# Contact Messages
# ===========================

class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):

        return self.subject


# ===========================
# Email OTP
# ===========================

class EmailOTP(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    last_sent = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.user.username


# ===========================
# Recipe
# ===========================

class Recipe(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    prep_time = models.CharField(max_length=50, default="15 mins")
    servings = models.PositiveIntegerField(default=2)
    calories_per_serving = models.PositiveIntegerField(default=250)
    health_tag = models.CharField(max_length=50, default="Healthy & Fresh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_bundle_price(self):
        return sum(item.product.price * item.quantity for item in self.ingredients.all())


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    unit_note = models.CharField(
        max_length=50,
        blank=True,
        default="1 pack"
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name}"