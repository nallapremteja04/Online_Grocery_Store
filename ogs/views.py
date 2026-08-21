import random
from datetime import timedelta

import cv2
import numpy as np
import pytesseract
import razorpay
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .ai_assistant import ask_ai
from .forms import OCRUploadForm
from .models import (
    Address,
    Cart,
    CartItem,
    Category,
    ContactMessage,
    Coupon,
    EmailOTP,
    Order,
    OrderItem,
    Product,
    Recipe,
    RecipeIngredient,
    Review,
    Wishlist,
)
from .utils import analyze_sentiment


# Home Page + Search

def home(request):
    categories = Category.objects.filter(is_active=True)
    query = request.GET.get('q', '').strip()
    related_products = Product.objects.none()

    if query:
        q_lower = query.lower()
        matching_qs = Product.objects.filter(
            Q(name__icontains=q_lower) |
            Q(category__name__icontains=q_lower) |
            Q(brand__icontains=q_lower) |
            Q(description__icontains=q_lower) |
            Q(flavour__icontains=q_lower),
            available=True
        ).distinct()

        if matching_qs.exists():
            products = matching_qs
            matched_cat_ids = matching_qs.values_list('category_id', flat=True)
            matched_prod_ids = matching_qs.values_list('id', flat=True)
            related_products = Product.objects.filter(
                category_id__in=matched_cat_ids,
                available=True
            ).exclude(id__in=matched_prod_ids).distinct()[:6]
        else:
            products = Product.objects.none()
            messages.info(request, f"No exact products found for '{query}'. Here are some popular recommendations.")
            related_products = Product.objects.filter(available=True)[:6]
    else:
        products = Product.objects.filter(available=True)[:8]

    featured_products = Product.objects.filter(available=True, health_score__gte=85)[:8]
    discount_products = [p for p in Product.objects.filter(available=True) if p.discount_percentage > 0][:8]
    if not discount_products:
        discount_products = Product.objects.filter(available=True)[:8]
    popular_products = Product.objects.filter(available=True).order_by('-stock')[:8]

    return render(request, 'ogs/home.html', {
        'categories': categories,
        'products': products,
        'featured_products': featured_products,
        'discount_products': discount_products,
        'popular_products': popular_products,
        'related_products': related_products,
        'query': query,
    })


# Products Page (Filtering, Sorting, Pagination)
def products(request):
    product_qs = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_active=True)

    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        product_qs = product_qs.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(flavour__icontains=query)
        ).distinct()

    # Category filter
    category_param = request.GET.get('category', '').strip()
    selected_category = None
    if category_param:
        if category_param.isdigit():
            selected_category = Category.objects.filter(id=int(category_param)).first()
        else:
            selected_category = Category.objects.filter(slug=category_param).first()

        if selected_category:
            product_qs = product_qs.filter(category=selected_category)

    # Price range filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            product_qs = product_qs.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            product_qs = product_qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Stock filter
    in_stock = request.GET.get('in_stock', '').strip()
    if in_stock in ('true', '1'):
        product_qs = product_qs.filter(stock__gt=0)

    # Sorting
    sort_param = request.GET.get('sort', '').strip()
    if sort_param == 'price_asc':
        product_qs = product_qs.order_by('price')
    elif sort_param == 'price_desc':
        product_qs = product_qs.order_by('-price')
    elif sort_param == 'newest':
        product_qs = product_qs.order_by('-created_at')
    elif sort_param == 'rating':
        product_qs = product_qs.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    else:
        product_qs = product_qs.order_by('-id')

    # Pagination
    total_count = product_qs.count()
    paginator = Paginator(product_qs, 12)
    page_number = request.GET.get('page')
    try:
        products_page = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        products_page = paginator.get_page(1)

    return render(request, 'ogs/products.html', {
        'products': products_page,
        'categories': categories,
        'selected_category': selected_category,
        'category_param': category_param,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort': sort_param,
        'total_count': total_count,
    })


# Categories Page
def categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'ogs/category.html', {
        'categories': categories,
    })


# Category-wise Products
def category_products(request, id=None, slug=None):
    if slug:
        category = get_object_or_404(Category, slug=slug)
    else:
        category = get_object_or_404(Category, id=id)

    return redirect(f"{reverse('products')}?category={category.slug or category.id}")


# Product Details (Supports ID or Slug)
def product_detail(request, id=None, slug=None):
    if slug:
        product = get_object_or_404(Product, slug=slug)
    else:
        product = get_object_or_404(Product, id=id)

    reviews = Review.objects.filter(product=product).order_by("-created_at")
    review_count = reviews.count()
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    recommended_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    return render(request, "ogs/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "review_count": review_count,
        "average_rating": round(average_rating, 1),
        "recommended_products": recommended_products,
    })
def add_to_cart(request, id):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            "Please register and login to add products to your cart."
        )

        return redirect('login')

    product = get_object_or_404(Product, id=id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def increase_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required
def remove_cart(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    item.delete()

    messages.success(request, "Item removed from cart.")

    return redirect('cart')

# About
def about(request):
    return render(request, 'ogs/about.html')


# Contact
def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(

            name=request.POST['name'],

            email=request.POST['email'],

            subject=request.POST['subject'],

            message=request.POST['message']

        )

        messages.success(
            request,
            "Thank you! Your message has been sent successfully."
        )

        return redirect('contact')

    return render(request, 'ogs/contact.html')


# Register
def register(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        print(f"\n🔑 [OTP LOG] Registration OTP generated for {email} ({username}): {otp}\n")

        # Store pending user details in session (USER IS NOT CREATED IN DATABASE YET)
        request.session['pending_registration'] = {
            'first_name': (first_name or '').strip(),
            'username': username,
            'email': email,
            'password': password,
            'otp': otp,
            'created_at': timezone.now().timestamp()
        }

        # Send OTP email
        try:
            send_mail(
                subject="Online Grocery Store - Email Verification",
                message=f"""
Welcome to Online Grocery Store!

Your Email Verification OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank you,
Online Grocery Store Team
""",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"⚠️ [EMAIL ERROR]: {e}")

        messages.success(
            request,
            f"OTP has been sent to {email}. (Check terminal console if testing locally)"
        )

        return redirect('verify_otp')

    return render(request, 'ogs/register.html')


# OTP verify
def verify_otp(request, user_id=None):

    pending = request.session.get('pending_registration')

    if not pending and user_id:
        user = get_object_or_404(User, id=user_id)
        otp_obj = get_object_or_404(EmailOTP, user=user)

        if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
            otp_obj.delete()
            user.delete()
            messages.error(request, "OTP expired. Please register again.")
            return redirect("register")

        if request.method == "POST":
            entered_otp = request.POST.get("otp")
            if entered_otp == otp_obj.otp:
                user.is_active = True
                user.save()
                otp_obj.delete()
                messages.success(request, "Email verified successfully. Please login.")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP. Please try again.")

        return render(request, "ogs/verify_otp.html", {"user": user})

    if not pending:
        messages.error(request, "No pending registration found. Please register.")
        return redirect("register")

    # Check 5-minute expiration
    created_at = pending.get('created_at', 0)
    if timezone.now().timestamp() - created_at > 300:
        del request.session['pending_registration']
        messages.error(request, "OTP expired. Please register again.")
        return redirect("register")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if entered_otp == pending.get('otp'):
            # ONLY NOW CREATE THE USER IN DATABASE AFTER SUCCESSFUL OTP VERIFICATION
            user = User.objects.create_user(
                username=pending['username'],
                first_name=pending['first_name'],
                email=pending['email'],
                password=pending['password'],
                is_active=True
            )

            del request.session['pending_registration']

            messages.success(
                request,
                "Email verified successfully! Account created. Please login."
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Please check your email or terminal console.")

    return render(request, "ogs/verify_otp.html", {"email": pending.get('email')})


# Resend OTP
def resend_otp(request, user_id=None):

    pending = request.session.get('pending_registration')

    if not pending and user_id:
        user = get_object_or_404(User, id=user_id)
        EmailOTP.objects.filter(user=user).delete()
        otp = str(random.randint(100000, 999999))
        print(f"\n🔑 [OTP LOG] Resent OTP for {user.email}: {otp}\n")
        EmailOTP.objects.create(user=user, otp=otp)
        try:
            send_mail(
                subject="Online Grocery Store - New OTP",
                message=f"Your new OTP is: {otp}",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(request, f"A new OTP has been sent to {user.email}.")
        return redirect('verify_otp_user', user_id=user.id)

    if not pending:
        messages.error(request, "No pending registration found. Please register.")
        return redirect("register")

    # Generate new OTP for pending session
    otp = str(random.randint(100000, 999999))
    print(f"\n🔑 [OTP LOG] Resent OTP for {pending['email']}: {otp}\n")
    pending['otp'] = otp
    pending['created_at'] = timezone.now().timestamp()
    request.session['pending_registration'] = pending

    try:
        send_mail(
            subject="Online Grocery Store - New OTP",
            message=f"Your new OTP is: {otp}",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
            recipient_list=[pending['email']],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(request, f"A new OTP has been sent to {pending['email']}.")
    return redirect('verify_otp')


# Login
def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Please verify your email before logging in."
                )
                return redirect('login')

            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')

        messages.error(request, "Invalid Username or Password")

    return render(request, 'ogs/login.html')


# Logout
def logout_page(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')


# Forgot Password Views
def forgot_password(request):
    if request.method == "POST":
        email_or_user = request.POST.get("email", "").strip()
        user = User.objects.filter(Q(email=email_or_user) | Q(username=email_or_user)).first()

        if user:
            otp = str(random.randint(100000, 999999))
            print(f"\n🔑 [OTP LOG] Password Reset OTP for {user.username} ({user.email}): {otp}\n")
            
            EmailOTP.objects.filter(user=user).delete()
            EmailOTP.objects.create(user=user, otp=otp)

            try:
                send_mail(
                    subject="Online Grocery Store - Password Reset OTP",
                    message=f"Hello {user.username},\n\nYour OTP to reset your Online Grocery Store account password is: {otp}\n\nThis OTP is valid for 5 minutes.",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"⚠️ [EMAIL ERROR]: {e}")

            messages.success(request, f"OTP sent to {user.email}. Check your inbox or terminal output.")
            return redirect('verify_reset_otp', user_id=user.id)
        else:
            messages.error(request, "No account found matching that username or email address.")

    return render(request, 'ogs/forgot_password.html')


def verify_reset_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    otp_obj = EmailOTP.objects.filter(user=user).first()

    if not otp_obj:
        messages.error(request, "No active password reset request found. Please request again.")
        return redirect('forgot_password')

    if timezone.now() > otp_obj.created_at + timedelta(minutes=10):
        otp_obj.delete()
        messages.error(request, "OTP expired. Please try again.")
        return redirect('forgot_password')

    if request.method == "POST":
        entered_otp = request.POST.get("otp", "").strip()
        if entered_otp == otp_obj.otp:
            request.session['reset_verified_user_id'] = user.id
            messages.success(request, "OTP verified! Please set a new password.")
            return redirect('reset_password', user_id=user.id)
        else:
            messages.error(request, "Invalid OTP code.")

    return render(request, 'ogs/verify_reset_otp.html', {'user': user})


def reset_password(request, user_id):
    verified_id = request.session.get('reset_verified_user_id')
    if verified_id != user_id:
        messages.error(request, "Unauthorized password reset attempt.")
        return redirect('forgot_password')

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_pass = request.POST.get("password")
        confirm_pass = request.POST.get("confirm_password")

        if new_pass != confirm_pass:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password', user_id=user.id)

        user.set_password(new_pass)
        user.save()
        
        EmailOTP.objects.filter(user=user).delete()
        request.session.pop('reset_verified_user_id', None)

        messages.success(request, "Password reset successfully! Please login with your new password.")
        return redirect('login')

    return render(request, 'ogs/reset_password.html', {'user': user})


# User Profile View
@login_required
def profile(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_profile":
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()

            user = request.user
            user.first_name = first_name
            user.last_name = last_name

            if email and email != user.email:
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    messages.error(request, "Email is already in use by another account.")
                else:
                    user.email = email
                    user.save()
                    messages.success(request, "Profile updated successfully.")
            else:
                user.save()
                messages.success(request, "Profile updated successfully.")
            return redirect('profile')

        elif action == "add_address":
            Address.objects.create(
                user=request.user,
                full_name=request.POST.get("full_name", "").strip(),
                phone=request.POST.get("phone", "").strip(),
                address=request.POST.get("address", "").strip(),
                city=request.POST.get("city", "").strip(),
                state=request.POST.get("state", "Telangana").strip(),
                pincode=request.POST.get("pincode", "").strip(),
                landmark=request.POST.get("landmark", "").strip(),
                address_type=request.POST.get("address_type", "Home"),
                is_default=request.POST.get("is_default") == "on"
            )
            messages.success(request, "New delivery address added successfully.")
            return redirect('profile')

        elif action == "delete_address":
            address_id = request.POST.get("address_id")
            Address.objects.filter(id=address_id, user=request.user).delete()
            messages.success(request, "Address deleted.")
            return redirect('profile')

    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    return render(request, 'ogs/profile.html', {
        'recent_orders': recent_orders,
        'addresses': addresses,
    })


# Cart View
def cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please register and login to access the cart.")
        return redirect('login')

    cart_obj, created = Cart.objects.get_or_create(user=request.user)

    # Coupon action
    if request.method == "POST" and "apply_coupon" in request.POST:
        code = request.POST.get("coupon_code", "").strip()
        if code:
            try:
                coupon = Coupon.objects.get(code=code, active=True)
                if coupon.expiry_date >= timezone.now().date():
                    request.session["coupon"] = code
                    messages.success(request, f"Coupon '{code}' applied successfully!")
                else:
                    messages.error(request, "Coupon has expired.")
            except Coupon.DoesNotExist:
                messages.error(request, "Invalid coupon code.")
        return redirect('cart')

    if request.method == "POST" and "remove_coupon" in request.POST:
        request.session.pop("coupon", None)
        messages.info(request, "Coupon removed.")
        return redirect('cart')

    items = CartItem.objects.filter(cart=cart_obj)

    subtotal = 0
    total_calories = 0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    weighted_health_sum = 0
    total_item_count = 0

    for item in items:
        item_subtotal = item.product.price * item.quantity
        subtotal += item_subtotal
        total_calories += (item.product.calories * item.quantity)
        total_protein += float(item.product.protein_g * item.quantity)
        total_carbs += float(item.product.carbs_g * item.quantity)
        total_fat += float(item.product.fat_g * item.quantity)
        weighted_health_sum += (item.product.health_score * item.quantity)
        total_item_count += item.quantity

    # Calculate discount from coupon
    discount = 0
    coupon_obj = None
    coupon_code = request.session.get("coupon")
    if coupon_code:
        try:
            coupon_obj = Coupon.objects.get(code=coupon_code, active=True)
            if coupon_obj.expiry_date >= timezone.now().date() and subtotal >= coupon_obj.minimum_amount:
                if coupon_obj.discount_type == "Flat":
                    discount = coupon_obj.discount
                else:
                    discount = (subtotal * coupon_obj.discount) / 100
        except Coupon.DoesNotExist:
            request.session.pop("coupon", None)

    # Delivery Charge calculation (Free above 500)
    delivery_charge = 0 if subtotal >= 500 or subtotal == 0 else 40
    grand_total = max(0, subtotal - discount + delivery_charge)

    health_score = round(weighted_health_sum / total_item_count) if total_item_count > 0 else 0

    if health_score >= 80:
        health_badge = {"label": "Super Healthy 🥑", "class": "bg-success", "message": "Excellent choice! Your cart is packed with nutrient-dense foods."}
    elif health_score >= 60:
        health_badge = {"label": "Balanced Cart ⚖️", "class": "bg-info", "message": "Good balance of proteins and daily essential groceries."}
    elif health_score > 0:
        health_badge = {"label": "Needs Greens 🍏", "class": "bg-warning text-dark", "message": "Consider adding fresh fruits or organic vegetables to boost your score."}
    else:
        health_badge = {"label": "Empty Cart", "class": "bg-secondary", "message": "Add items to calculate your health score."}

    return render(request, 'ogs/cart.html', {
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
        'coupon': coupon_obj,
        'total_calories': total_calories,
        'total_protein': round(total_protein, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fat': round(total_fat, 1),
        'health_score': health_score,
        'health_badge': health_badge,
    })

def chatbot(request):

    message = request.GET.get("message", "").strip()

    try:

        reply = ask_ai(message, request.user)

        return JsonResponse({
            "reply": reply
        })

    except Exception as e:

        return JsonResponse({
            "reply": str(e)
        }, status=500)

# Checkout View
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect('login')

    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_obj)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add some products before checkout.")
        return redirect('cart')

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    discount = 0
    coupon_code = request.session.get("coupon")
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            if coupon.expiry_date >= timezone.now().date() and subtotal >= coupon.minimum_amount:
                if coupon.discount_type == "Flat":
                    discount = coupon.discount
                else:
                    discount = (subtotal * coupon.discount) / 100
        except Coupon.DoesNotExist:
            pass

    delivery_charge = 0 if subtotal >= 500 else 40
    grand_total = max(0, subtotal - discount + delivery_charge)

    saved_addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    if request.method == "POST":
        payment_method = request.POST.get("payment_method", "COD")
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_text = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not (full_name and phone and address_text and city and pincode):
            messages.error(request, "Please fill in all delivery details.")
            return redirect('checkout')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address_text,
            city=city,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=grand_total,
            status="Pending",
            payment_status="Pending",
            expected_delivery=timezone.now().date() + timedelta(days=2)
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        if payment_method == "COD" or not (settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET):
            for item in cart_items:
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            cart_items.delete()
            request.session.pop("coupon", None)
            order.payment_status = "Pending" if payment_method == "COD" else "Paid"
            order.save()

            messages.success(request, f"Order #{order.id} placed successfully! Thank you for shopping with us.")
            return redirect("my_orders")

        # Razorpay Payment Flow
        try:
            client = razorpay.Client(
                auth=(
                    settings.RAZORPAY_KEY_ID.strip(),
                    settings.RAZORPAY_KEY_SECRET.strip()
                )
            )
            payment = client.order.create({
                "amount": int(grand_total * 100),
                "currency": "INR",
                "payment_capture": 1
            })
            order.razorpay_order_id = payment["id"]
            order.save()

            return render(request, "ogs/payment.html", {
                "order": order,
                "cart_items": cart_items,
                "payment": payment,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "subtotal": subtotal,
                "discount": discount,
                "delivery_charge": delivery_charge,
                "grand_total": grand_total
            })
        except Exception as e:
            # Fall back to COD if Razorpay API fails
            for item in cart_items:
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            cart_items.delete()
            request.session.pop("coupon", None)
            order.payment_method = "COD"
            order.save()
            messages.success(request, f"Order #{order.id} placed successfully via Cash on Delivery!")
            return redirect("my_orders")

    return render(request, "ogs/checkout.html", {
        "items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "delivery_charge": delivery_charge,
        "grand_total": grand_total,
        "saved_addresses": saved_addresses,
    })

# my_orders

def my_orders(request):

    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your orders.")
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'ogs/my_orders.html', {
        'orders': orders
    })


def cancel_order(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    if order.status == "Pending":

        order.status = "Cancelled"
        order.save()

        messages.success(
            request,
            "Your order has been cancelled successfully."
        )

    elif order.status == "Cancelled":

        messages.info(
            request,
            "This order is already cancelled."
        )

    else:

        messages.warning(
            request,
            "Delivered or shipped orders cannot be cancelled."
        )

    return redirect('my_orders')


def order_detail(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    items = OrderItem.objects.filter(order=order)

    return render(request, 'ogs/order_detail.html', {
        'order': order,
        'items': items
    })

def invoice_pdf(request, id):

    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect('login')

    order = get_object_or_404(Order, id=id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Invoice_{order.id}.pdf'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, y, "ONLINE GROCERY STORE")

    y -= 40

    p.setFont("Helvetica", 12)

    p.drawString(50, y, f"Invoice No : {order.id}")

    y -= 20
    p.drawString(50, y, f"Customer : {order.full_name}")

    y -= 20
    p.drawString(50, y, f"Phone : {order.phone}")

    y -= 20
    p.drawString(50, y, f"Payment : {order.payment_method}")

    y -= 20
    p.drawString(50, y, f"Status : {order.status}")

    y -= 20
    p.drawString(50, y, "Address :")

    y -= 20
    p.drawString(70, y, order.address)

    y -= 20
    p.drawString(70, y, f"{order.city} - {order.pincode}")

    y -= 40

    p.setFont("Helvetica-Bold", 12)

    p.drawString(50, y, "Product")
    p.drawString(260, y, "Qty")
    p.drawString(330, y, "Price")
    p.drawString(430, y, "Subtotal")

    y -= 20

    p.line(50, y, 550, y)

    y -= 20

    total = 0

    p.setFont("Helvetica", 11)

    for item in items:

        subtotal = item.price * item.quantity
        total += subtotal

        p.drawString(50, y, item.product.name)
        p.drawString(270, y, str(item.quantity))
        p.drawString(330, y, f"₹{item.price}")
        p.drawString(430, y, f"₹{subtotal}")

        y -= 20

        if y < 80:
            p.showPage()
            y = 800

    y -= 20

    p.line(50, y, 550, y)

    y -= 30

    p.setFont("Helvetica-Bold", 14)

    p.drawString(350, y, f"Grand Total : ₹{total}")

    y -= 40

    p.setFont("Helvetica", 12)

    p.drawString(150, y, "Thank You For Shopping With Us!")

    p.save()

    return response

# forgot_password
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            # Delete old OTP
            EmailOTP.objects.filter(user=user).delete()

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP
            EmailOTP.objects.create(
                user=user,
                otp=otp
            )

            # Send Email
            try:
                send_mail(
                    subject="Password Reset OTP",
                    message=f"Your OTP is: {otp}",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass


            messages.success(request, "OTP has been sent to your email.")

            return redirect("verify_reset_otp", user_id=user.id)

        except User.DoesNotExist:
            messages.error(request, "Email is not registered.")

    return render(request, "ogs/forgot_password.html")

#verify_reset_otp
def verify_reset_otp(request, user_id):

    user = get_object_or_404(User, id=user_id)
    otp_obj = get_object_or_404(EmailOTP, user=user)

    # OTP expires after 5 minutes
    if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
        otp_obj.delete()

        messages.error(
            request,
            "OTP expired. Please request a new OTP."
        )

        return redirect("forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        if entered_otp == otp_obj.otp:

            otp_obj.delete()

            return redirect("reset_password", user_id=user.id)

        else:

            messages.error(request, "Invalid OTP")

    return render(
        request,
        "ogs/verify_reset_otp.html",
        {
            "user": user
        }
    )
# reset_password
def reset_password(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password", user_id=user.id)

        user.set_password(password)
        user.save()

        messages.success(
            request,
            "Password reset successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "ogs/reset_password.html"
    )

# payment_success
@csrf_exempt
def payment_success(request):

    payment_id = request.GET.get("payment_id")
    razorpay_order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID.strip(),
            settings.RAZORPAY_KEY_SECRET.strip()
        )
    )

    try:

        client.utility.verify_payment_signature({

            "razorpay_order_id": razorpay_order_id,

            "razorpay_payment_id": payment_id,

            "razorpay_signature": signature

        })

        order = Order.objects.get(
            razorpay_order_id=razorpay_order_id
        )

        order.payment_status = "Paid"
        order.status = "Confirmed"
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.save()

        # Reduce stock
        items = OrderItem.objects.filter(order=order)

        for item in items:
            item.product.stock -= item.quantity
            item.product.save()

        # Empty Cart
        CartItem.objects.filter(cart__user=order.user).delete()

        messages.success(
            request,
            "Payment Successful!"
        )

        return redirect("my_orders")

    except:

        messages.error(
            request,
            "Payment Failed."
        )

        return redirect("checkout")

@login_required
def add_review(request, id):

    product = get_object_or_404(Product, id=id)

    purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status="Delivered"
    ).exists()

    if not purchased:

        messages.error(
            request,
            "Only customers who purchased this product can review it."
        )

        return redirect(
            "product_detail",
            id=id
        )

    review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()

    if request.method == "POST":

        rating = request.POST["rating"]

        review_text = request.POST["review"]

        # -------- AI Sentiment Analysis --------
        sentiment = analyze_sentiment(review_text)

        image = request.FILES.get("image")

        if review:

            review.rating = rating
            review.review = review_text
            review.sentiment = sentiment

            if image:
                review.image = image

            review.save()

            messages.success(
                request,
                "Review updated successfully."
            )

        else:

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                review=review_text,
                sentiment=sentiment,
                image=image,
                verified_purchase=True
            )

            messages.success(
                request,
                "Review submitted successfully."
            )

    return redirect(
        "product_detail",
        id=id
    )
@login_required
def delete_review(request, id):

    review = get_object_or_404(
        Review,
        id=id,
        user=request.user
    )

    product_id = review.product.id

    review.delete()

    messages.success(
        request,
        "Review deleted successfully."
    )

    return redirect(
        "product_detail",
        id=product_id
    )

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(request, "ogs/wishlist.html", {
        "items": items
    })


@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(request, "Product added to Wishlist ❤️")

    return redirect("product_detail", id=id)


@login_required
def remove_wishlist(request, id):

    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    messages.success(request, "Removed from Wishlist")

    return redirect("wishlist")


@login_required
def wishlist_to_cart(request, id):

    wishlist_item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=wishlist_item.product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    wishlist_item.delete()

    messages.success(
        request,
        "Product moved to Cart successfully."
    )

    return redirect("wishlist")


@staff_member_required
def admin_dashboard(request):

    total_orders = Order.objects.count()

    total_products = Product.objects.count()

    total_users = User.objects.count()

    total_reviews = Review.objects.count()

    total_revenue = Order.objects.filter(
        payment_status="Paid"
    ).aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    pending_orders = Order.objects.filter(
        status="Pending"
    ).count()

    delivered_orders = Order.objects.filter(
        status="Delivered"
    ).count()

    cancelled_orders = Order.objects.filter(
        status="Cancelled"
    ).count()

    context = {

        "total_orders": total_orders,

        "total_products": total_products,

        "total_users": total_users,

        "total_reviews": total_reviews,

        "total_revenue": total_revenue,

        "pending_orders": pending_orders,

        "delivered_orders": delivered_orders,

        "cancelled_orders": cancelled_orders,

    }

    return render(
        request,
        "ogs/admin_dashboard.html",
        context
    )

def ocr_scanner(request):

    products = []

    extracted_text = ""

    if request.method == "POST":

        form = OCRUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            image = Image.open(
                request.FILES["image"]
            )

            extracted_text = pytesseract.image_to_string(image)

            words = extracted_text.split()

            for word in words:

                result = Product.objects.filter(
                    name__icontains=word
                )

                products.extend(result)

    else:

        form = OCRUploadForm()

    return render(
        request,
        "ogs/ocr_scanner.html",
        {
            "form": form,
            "products": products,
            "text": extracted_text
        }
    )


def ai_chat(request):

    if request.method == "POST":

        message = request.POST.get("message")

        print("=" * 60)
        print("USER :", message)

        reply = ask_ai(message, request.user)

        print("AI REPLY :", reply)
        print("=" * 60)

        return JsonResponse({
            "reply": reply
        })

    return render(request, "ogs/ai_chat.html")


def search_products(request):
    query = request.GET.get("q", "").strip()
    products = []

    if query:
        q_lower = query.lower()
        results = Product.objects.filter(
            Q(name__icontains=q_lower) |
            Q(category__name__icontains=q_lower) |
            Q(brand__icontains=q_lower) |
            Q(flavour__icontains=q_lower),
            available=True
        ).distinct()[:6]

        for product in results:
            products.append({
                "id": product.id,
                "slug": product.slug or str(product.id),
                "name": product.name,
                "price": str(product.price),
                "category": product.category.name if product.category else "",
                "image_url": product.image_url,
            })

    return JsonResponse({"products": products}, safe=False)


# ===========================
# Recipe Hub & 1-Click Recipe to Cart
# ===========================

RECIPE_INGREDIENT_DATABASE = {
    # 1. Hyderabadi Veg Dum Biryani
    'biryani': [
        {'name': 'Basmati Rice', 'keywords': ['basmati', 'rice']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato', 'tomatoes']},
        {'name': 'Fresh Onions', 'keywords': ['onion', 'onions']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter', 'ghee']},
        {'name': 'Fresh Paneer', 'keywords': ['paneer']},
        {'name': 'Biryani & Masala Spices', 'keywords': ['spice']},
        {'name': 'Fresh Whole Milk / Curd', 'keywords': ['milk', 'curd']},
        {'name': 'Saffron / Food Color', 'keywords': ['saffron']}
    ],
    # 2. Telangana Bagara Rice
    'bagara': [
        {'name': 'Basmati Rice', 'keywords': ['basmati', 'rice']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic & Ginger', 'keywords': ['garlic']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter']},
        {'name': 'Biryani Spices', 'keywords': ['spice']}
    ],
    # 3. Telangana Tomato Kura / Curry
    'tomato kura': [
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Premium Basmati Rice', 'keywords': ['rice', 'basmati']}
    ],
    # 4. Telangana Sakinalu
    'sakinalu': [
        {'name': 'Rice Flour', 'keywords': ['rice', 'flour']},
        {'name': 'Sesame Seeds / Til', 'keywords': ['sesame', 'seed']},
        {'name': 'Cooking Oil / Ghee', 'keywords': ['butter', 'oil']},
        {'name': 'Salt & Carom Seeds', 'keywords': ['salt']}
    ],
    # 5. Sarva Pindi / Tapala Chettu
    'sarva pindi': [
        {'name': 'Rice Flour', 'keywords': ['rice', 'flour']},
        {'name': 'Chana Dal / Lentils', 'keywords': ['dal', 'chana']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Cooking Oil', 'keywords': ['butter']}
    ],
    # 6. Telangana Bendakaya Fry / Okra
    'bendakaya': [
        {'name': 'Okra / Bhindi', 'keywords': ['okra', 'bhindi', 'spinach']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Cooking Oil', 'keywords': ['butter']}
    ],
    # 7. Gutti Vankaya Kura / Stuffed Brinjal
    'vankaya': [
        {'name': 'Brinjal / Eggplant', 'keywords': ['brinjal', 'eggplant', 'tomato']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']}
    ],
    # 8. Pachi Pulusu / Raw Tamarind Stew
    'pachi pulusu': [
        {'name': 'Tamarind / Fresh Lemon', 'keywords': ['lemon', 'tamarind']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Green Chilies & Herbs', 'keywords': ['spinach']}
    ],
    # 9. Mirchi Ka Salan
    'mirchi ka salan': [
        {'name': 'Green Chilies', 'keywords': ['spinach']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Garlic & Spices', 'keywords': ['garlic', 'spice']},
        {'name': 'Peanut / Sesame Paste', 'keywords': ['butter']}
    ],
    # 10. Hyderabadi Khatti Dal
    'khatti dal': [
        {'name': 'Yellow Lentils / Dal', 'keywords': ['dal', 'oats']},
        {'name': 'Tamarind / Fresh Lemon', 'keywords': ['lemon']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Ghee / Butter', 'keywords': ['butter']}
    ],
    # 11. Hyderabadi Irani Chai
    'chai': [
        {'name': 'Hyderabadi Irani Tea Powder', 'keywords': ['tea']},
        {'name': 'Fresh Whole Milk', 'keywords': ['milk']},
        {'name': 'Fresh Garlic & Ginger', 'keywords': ['garlic']},
        {'name': 'Cardamom & Sugar', 'keywords': ['cardamom']}
    ],
    # 12. Tea
    'tea': [
        {'name': 'Hyderabadi Irani Tea Powder', 'keywords': ['tea']},
        {'name': 'Fresh Whole Milk', 'keywords': ['milk']}
    ],
    # 13. Telangana Atukula Upma / Poha
    'poha': [
        {'name': 'Flattened Rice / Atukulu', 'keywords': ['rice', 'atukulu']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Lemon', 'keywords': ['lemon']},
        {'name': 'Table Butter / Oil', 'keywords': ['butter']}
    ],
    # 14. South Indian Masala Dosa
    'dosa': [
        {'name': 'Rice & Dal Dosa Batter', 'keywords': ['rice', 'basmati']},
        {'name': 'Fresh Onions & Potatoes', 'keywords': ['onion']},
        {'name': 'Fresh Tomatoes / Chutney', 'keywords': ['tomato']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter']}
    ],
    # 15. Steamed Soft Idli
    'idli': [
        {'name': 'Rice Idli Batter', 'keywords': ['rice', 'basmati']},
        {'name': 'Fresh Tomatoes for Chutney', 'keywords': ['tomato']},
        {'name': 'Ghee / Butter', 'keywords': ['butter']}
    ],
    # 16. Medu Vada
    'vada': [
        {'name': 'Urad Dal Batter', 'keywords': ['dal', 'rice']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Cooking Oil', 'keywords': ['butter']}
    ],
    # 17. South Indian Sambar
    'sambar': [
        {'name': 'Yellow Lentils / Dal', 'keywords': ['dal']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Tamarind / Lemon', 'keywords': ['lemon']},
        {'name': 'Sambar Spice Powder', 'keywords': ['spice']}
    ],
    # 18. South Indian Pepper Rasam
    'rasam': [
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Tamarind / Fresh Lemon', 'keywords': ['lemon']},
        {'name': 'Pepper Spices & Ghee', 'keywords': ['butter', 'spice']}
    ],
    # 19. Curd Rice / Daddojanam
    'curd rice': [
        {'name': 'Premium Basmati Rice', 'keywords': ['rice', 'basmati']},
        {'name': 'Fresh Whole Milk / Curd', 'keywords': ['milk', 'curd']},
        {'name': 'Fresh Garlic & Ginger', 'keywords': ['garlic']},
        {'name': 'Mustard & Butter', 'keywords': ['butter']}
    ],
    # 20. Upma / Rava Upma
    'upma': [
        {'name': 'Semolina / Rava', 'keywords': ['rice', 'oats']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter']}
    ],
    # 21. Uttapam
    'uttapam': [
        {'name': 'Dosa Batter', 'keywords': ['rice', 'basmati']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']}
    ],
    # 22. Lemon Rice / Chitrannam
    'lemon rice': [
        {'name': 'Premium Basmati Rice', 'keywords': ['rice', 'basmati']},
        {'name': 'Fresh Lemon', 'keywords': ['lemon']},
        {'name': 'Mustard & Peanuts', 'keywords': ['butter']},
        {'name': 'Fresh Garlic', 'keywords': ['garlic']}
    ],
    # 23. Tamarind Rice / Pulihora
    'pulihora': [
        {'name': 'Premium Basmati Rice', 'keywords': ['rice', 'basmati']},
        {'name': 'Tamarind / Fresh Lemon', 'keywords': ['lemon']},
        {'name': 'Peanuts & Spices', 'keywords': ['spice']},
        {'name': 'Ghee / Butter', 'keywords': ['butter']}
    ],
    # 24. Bisi Bele Bath
    'bisi bele bath': [
        {'name': 'Basmati Rice', 'keywords': ['rice', 'basmati']},
        {'name': 'Yellow Lentils / Dal', 'keywords': ['dal']},
        {'name': 'Fresh Tomatoes', 'keywords': ['tomato']},
        {'name': 'Fresh Onions', 'keywords': ['onion']},
        {'name': 'Ghee & Spices', 'keywords': ['butter', 'spice']}
    ],
    # 25. Double Ka Meetha / Dessert
    'meetha': [
        {'name': 'Bread Slices', 'keywords': ['bread', 'oats']},
        {'name': 'Fresh Whole Milk', 'keywords': ['milk']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter']},
        {'name': 'Sugar & Cardamom', 'keywords': ['sugar']}
    ],
    # 26. Semiya Payasam / Kheer
    'payasam': [
        {'name': 'Vermicelli / Semiya', 'keywords': ['oats', 'pasta']},
        {'name': 'Fresh Whole Milk', 'keywords': ['milk']},
        {'name': 'Table Butter / Ghee', 'keywords': ['butter']}
    ]
}

def get_recipe_ingredients_breakdown(recipe_name):
    name_lower = recipe_name.lower()
    items_to_check = None
    for key, items in RECIPE_INGREDIENT_DATABASE.items():
        if key in name_lower:
            items_to_check = items
            break

    if not items_to_check:
        words = [w for w in name_lower.split() if len(w) > 2]
        items_to_check = [
            {'name': f'Main Ingredient for {recipe_name.title()}', 'keywords': words if words else [name_lower]},
            {'name': 'Fresh Tomatoes / Base', 'keywords': ['tomato']},
            {'name': 'Fresh Onions & Garlic', 'keywords': ['garlic']},
            {'name': 'Butter / Ghee / Oil', 'keywords': ['butter']},
            {'name': 'Fresh Lemon / Herbs', 'keywords': ['lemon', 'spinach']}
        ]

    matched_results = []
    for item in items_to_check:
        found_product = None
        for kw in item['keywords']:
            p = Product.objects.filter(name__icontains=kw, available=True).first()
            if p:
                found_product = p
                break

        if found_product and found_product.stock > 0:
            matched_results.append({
                'name': item['name'],
                'product': found_product,
                'status': 'available',
                'price': found_product.price,
                'stock': found_product.stock
            })
        else:
            matched_results.append({
                'name': item['name'],
                'product': None,
                'status': 'not_available',
                'price': None,
                'stock': 0
            })

    return matched_results


def recipe_list(request):
    query = request.GET.get('q', '').strip()
    recipes_qs = Recipe.objects.all().order_by('-created_at')
    searched_recipe_breakdown = None

    if query:
        q_lower = query.lower()
        recipes_qs = Recipe.objects.filter(
            Q(name__icontains=q_lower) |
            Q(description__icontains=q_lower) |
            Q(health_tag__icontains=q_lower)
        ).distinct()

        # Get full ingredient breakdown for searched recipe (e.g. Biryani)
        raw_breakdown = get_recipe_ingredients_breakdown(query)
        available_items = [item for item in raw_breakdown if item['status'] == 'available']
        unavailable_items = [item for item in raw_breakdown if item['status'] != 'available']

        searched_recipe_breakdown = {
            'recipe_name': query.title(),
            'all_items': raw_breakdown,
            'available_items': available_items,
            'unavailable_items': unavailable_items,
            'total_count': len(raw_breakdown),
            'available_count': len(available_items),
            'unavailable_count': len(unavailable_items),
        }

    # Process ingredient availability for pre-defined recipes
    processed_recipes = []
    for r in recipes_qs:
        ing_list = r.ingredients.all()
        in_stock_count = sum(1 for ing in ing_list if ing.product.available and ing.product.stock > 0)
        out_of_stock_count = sum(1 for ing in ing_list if not (ing.product.available and ing.product.stock > 0))
        total_ing = ing_list.count()

        processed_recipes.append({
            'recipe': r,
            'ingredients': ing_list,
            'in_stock_count': in_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'total_ing': total_ing,
            'is_fully_available': (out_of_stock_count == 0 and total_ing > 0),
        })

    # If NO search query is typed, limit default display to ONLY 3 recommended recipes!
    if not query:
        processed_recipes = processed_recipes[:3]

    return render(request, 'ogs/recipes.html', {
        'recipes': processed_recipes,
        'query': query,
        'breakdown': searched_recipe_breakdown,
    })

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    ingredients = recipe.ingredients.all()
    return render(request, 'ogs/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients
    })

@login_required
def add_recipe_to_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    added_count = 0
    for ing in recipe.ingredients.all():
        if ing.product.available and ing.product.stock > 0:
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=ing.product
            )
            if not item_created:
                cart_item.quantity += ing.quantity
            else:
                cart_item.quantity = ing.quantity
            cart_item.save()
            added_count += 1

    if added_count > 0:
        messages.success(request, f"🎉 All ingredients for '{recipe.name}' added to your cart!")
    else:
        messages.warning(request, "Some ingredients for this recipe are currently out of stock.")

    return redirect('cart')