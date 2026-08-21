from groq import Groq
from django.conf import settings
from .models import Product, Cart, CartItem
import re

def get_groq_client():
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception:
        return None

def ask_ai(question, user=None):
    q = question.lower().strip()
    products = Product.objects.filter(available=True)

    # ======================================================
    # ADD PRODUCT TO CART
    # ======================================================
    if user and user.is_authenticated:
        if "add" in q and "cart" in q:
            for product in products:
                if product.name.lower() in q:
                    cart, _ = Cart.objects.get_or_create(user=user)
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        product=product
                    )
                    if not created:
                        cart_item.quantity += 1
                        cart_item.save()

                    return f"✅ {product.name} has been added to your cart."

            return "❌ Product not found."

    # ======================================================
    # CATEGORY SEARCH
    # ======================================================
    categories = [
        "fruit",
        "vegetable",
        "dairy",
        "snacks",
        "beverages",
        "staples"
    ]

    for category in categories:
        if category in q:
            data = products.filter(category__name__icontains=category)
            if data.exists():
                answer = f"🛒 {category.title()} Products\n\n"
                for p in data:
                    answer += f"✅ {p.name}\n💰 ₹{p.price}\n📦 Stock : {p.stock}\n\n"
                return answer
            return f"No {category} products available."

    # ======================================================
    # PRODUCTS UNDER PRICE
    # ======================================================
    price = re.findall(r"\d+", q)
    if "under" in q and price:
        amount = int(price[0])
        data = products.filter(price__lte=amount)
        if data.exists():
            answer = f"🛍 Products Under ₹{amount}\n\n"
            for p in data:
                answer += f"✅ {p.name} - ₹{p.price}\n"
            return answer
        return "No products found."

    # ======================================================
    # PRODUCT SEARCH
    # ======================================================
    for product in products:
        if product.name.lower() in q:
            return f"""
📦 {product.name}

💰 Price : ₹{product.price}

📂 Category : {product.category.name}

🏷 Brand : {product.brand if product.brand else "N/A"}

⚖ Weight : {product.weight if product.weight else "N/A"}

📦 Stock : {product.stock}

📝 Description :

{product.description}
"""

    # ======================================================
    # GROQ AI
    # ======================================================
    client = get_groq_client()
    if not client:
        return "🤖 AI Assistant is currently offline. Please configure a valid GROQ_API_KEY in your .env file to enable live AI responses."

    product_data = ""
    for p in products:
        product_data += f"{p.name} | {p.category.name} | ₹{p.price} | {p.stock} in stock\n"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are an AI Shopping Assistant for an Online Grocery Store.

Available Products:

{product_data}

Rules:
1. Recommend only available products.
2. Mention prices.
3. Suggest recipes.
4. Suggest healthy foods.
5. Never invent products.
6. Keep answers short.
7. Be friendly.
"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🤖 AI Assistant encounters an issue: {str(e)}"