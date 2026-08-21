from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail_slug'),

    path('categories/', views.categories, name='categories'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('category/<slug:slug>/', views.category_products, name='category_products_slug'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication & User Profile
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),

    # OTP
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp_user'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp_user'),

    # Forgot Password
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/<int:user_id>/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),

    # Cart
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),

    # Search
    path('search-products/', views.search_products, name='search_products'),

    # Checkout & Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),

    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/', views.my_orders, name='orders'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('orders/<int:id>/', views.order_detail, name='order_detail_alt'),
    path('cancel-order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:id>/', views.invoice_pdf, name='invoice_pdf'),

    # Reviews
    path('add-review/<int:id>/', views.add_review, name='add_review'),
    path('delete-review/<int:id>/', views.delete_review, name='delete_review'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),
    path('wishlist-cart/<int:id>/', views.wishlist_to_cart, name='wishlist_to_cart'),

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("ocr-scanner/",views.ocr_scanner,name="ocr_scanner"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("ai-chat/",views.ai_chat,name="ai_chat"),

    # Recipe Hub
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('add-recipe-to-cart/<int:id>/', views.add_recipe_to_cart, name='add_recipe_to_cart'),
]