import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_grocery.settings')
django.setup()

from ogs.models import Category, Product, Recipe, RecipeIngredient

MAIN_10_CATEGORIES = {
    'Fruits': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=600&auto=format&fit=crop&q=80',
    'Vegetables': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=600&auto=format&fit=crop&q=80',
    'Dairy & Eggs': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=600&auto=format&fit=crop&q=80',
    'Staples & Grains': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80',
    'Spices & Masalas': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600&auto=format&fit=crop&q=80',
    'Oils & Ghee': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&auto=format&fit=crop&q=80',
    'Snacks & Munchies': 'https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=600&auto=format&fit=crop&q=80',
    'Beverages & Tea': 'https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=600&auto=format&fit=crop&q=80',
    'Bakery & Sweets': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&auto=format&fit=crop&q=80',
    'Personal & Household': 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=600&auto=format&fit=crop&q=80',
}

PRODUCTS_CATALOG = {
    'Fruits': [
        {"name": "Fresh Red Apple", "price": 120.00, "weight": "1 kg", "cal": 52, "prot": 0.3, "carbs": 14.0, "fat": 0.2, "health": 95, "img": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=500&auto=format&fit=crop&q=80"},
        {"name": "Robusta Banana", "price": 60.00, "weight": "1 Dozen", "cal": 89, "prot": 1.1, "carbs": 23.0, "fat": 0.3, "health": 90, "img": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&auto=format&fit=crop&q=80"},
        {"name": "Nagpur Orange", "price": 110.00, "weight": "1 kg", "cal": 47, "prot": 0.9, "carbs": 12.0, "fat": 0.1, "health": 92, "img": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=500&auto=format&fit=crop&q=80"},
        {"name": "Alphonso Mango", "price": 299.00, "weight": "1 kg", "cal": 60, "prot": 0.8, "carbs": 15.0, "fat": 0.4, "health": 88, "img": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&auto=format&fit=crop&q=80"},
        {"name": "Green Seedless Grapes", "price": 90.00, "weight": "500g", "cal": 69, "prot": 0.7, "carbs": 18.0, "fat": 0.2, "health": 85, "img": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=500&auto=format&fit=crop&q=80"},
        {"name": "Pomegranate (Anar)", "price": 190.00, "weight": "1 kg", "cal": 83, "prot": 1.7, "carbs": 19.0, "fat": 1.2, "health": 96, "img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Sweet Watermelon", "price": 99.00, "weight": "1 Pc (~3kg)", "cal": 30, "prot": 0.6, "carbs": 8.0, "fat": 0.2, "health": 91, "img": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&auto=format&fit=crop&q=80"},
        {"name": "Sweet Honey Papaya", "price": 70.00, "weight": "1 Pc", "cal": 43, "prot": 0.5, "carbs": 11.0, "fat": 0.3, "health": 93, "img": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=500&auto=format&fit=crop&q=80"},
        {"name": "Pink Guava", "price": 85.00, "weight": "1 kg", "cal": 68, "prot": 2.6, "carbs": 14.0, "fat": 1.0, "health": 94, "img": "https://images.unsplash.com/photo-1536511135885-37ff4d4efdd2?w=500&auto=format&fit=crop&q=80"},
        {"name": "Imported Kiwi Fruit", "price": 120.00, "weight": "3 Pcs", "cal": 61, "prot": 1.1, "carbs": 15.0, "fat": 0.5, "health": 92, "img": "https://images.unsplash.com/photo-1585059819970-31398d689617?w=500&auto=format&fit=crop&q=80"},
    ],
    'Vegetables': [
        {"name": "Fresh Tomatoes", "price": 35.00, "weight": "1 kg", "cal": 18, "prot": 0.9, "carbs": 3.9, "fat": 0.2, "health": 95, "img": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Potatoes", "price": 30.00, "weight": "1 kg", "cal": 77, "prot": 2.0, "carbs": 17.0, "fat": 0.1, "health": 82, "img": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Onions", "price": 40.00, "weight": "1 kg", "cal": 40, "prot": 1.1, "carbs": 9.3, "fat": 0.1, "health": 85, "img": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Garlic", "price": 40.00, "weight": "250g", "cal": 149, "prot": 6.4, "carbs": 33.0, "fat": 0.5, "health": 98, "img": "https://images.unsplash.com/photo-1608797178974-15b35a6405ba?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Spinach (Palak)", "price": 30.00, "weight": "250g", "cal": 23, "prot": 2.9, "carbs": 3.6, "fat": 0.4, "health": 99, "img": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=500&auto=format&fit=crop&q=80"},
        {"name": "Crisp Cucumber", "price": 25.00, "weight": "500g", "cal": 15, "prot": 0.7, "carbs": 3.6, "fat": 0.1, "health": 94, "img": "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=500&auto=format&fit=crop&q=80"},
        {"name": "Green Chili", "price": 25.00, "weight": "200g", "cal": 40, "prot": 2.0, "carbs": 9.0, "fat": 0.2, "health": 89, "img": "https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Ginger (Adrak)", "price": 35.00, "weight": "250g", "cal": 80, "prot": 1.8, "carbs": 18.0, "fat": 0.8, "health": 97, "img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Lady Finger (Bhindi)", "price": 40.00, "weight": "500g", "cal": 33, "prot": 1.9, "carbs": 7.0, "fat": 0.2, "health": 90, "img": "https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?w=500&auto=format&fit=crop&q=80"},
        {"name": "Cauliflower (Gobi)", "price": 40.00, "weight": "1 Pc", "cal": 25, "prot": 1.9, "carbs": 5.0, "fat": 0.3, "health": 91, "img": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=500&auto=format&fit=crop&q=80"},
    ],
    'Dairy & Eggs': [
        {"name": "Fresh Whole Milk", "price": 65.00, "weight": "1 Ltr", "cal": 62, "prot": 3.2, "carbs": 4.8, "fat": 3.3, "health": 88, "img": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&auto=format&fit=crop&q=80"},
        {"name": "Farm Fresh Eggs", "price": 90.00, "weight": "Pack of 12", "cal": 155, "prot": 13.0, "carbs": 1.1, "fat": 11.0, "health": 92, "img": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=500&auto=format&fit=crop&q=80"},
        {"name": "Premium Fresh Paneer", "price": 95.00, "weight": "200g", "cal": 265, "prot": 18.0, "carbs": 3.0, "fat": 20.0, "health": 87, "img": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500&auto=format&fit=crop&q=80"},
        {"name": "Amul Table Butter", "price": 58.00, "weight": "100g", "cal": 717, "prot": 0.8, "carbs": 0.1, "fat": 81.0, "health": 70, "img": "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=500&auto=format&fit=crop&q=80"},
        {"name": "Processed Cheese Slices", "price": 145.00, "weight": "200g", "cal": 300, "prot": 18.0, "carbs": 2.0, "fat": 24.0, "health": 75, "img": "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Curd (Dahi)", "price": 35.00, "weight": "400g", "cal": 60, "prot": 3.5, "carbs": 4.7, "fat": 3.0, "health": 94, "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&auto=format&fit=crop&q=80"},
        {"name": "Fresh Cooking Cream", "price": 65.00, "weight": "200ml", "cal": 195, "prot": 2.0, "carbs": 3.5, "fat": 20.0, "health": 78, "img": "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=500&auto=format&fit=crop&q=80"},
        {"name": "Condensed Milk (Milkmaid)", "price": 145.00, "weight": "400g", "cal": 321, "prot": 7.9, "carbs": 54.0, "fat": 8.7, "health": 65, "img": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&auto=format&fit=crop&q=80"},
        {"name": "Spiced Buttermilk (Chaas)", "price": 15.00, "weight": "200ml", "cal": 40, "prot": 2.0, "carbs": 4.0, "fat": 1.5, "health": 93, "img": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Greek Yogurt", "price": 50.00, "weight": "100g", "cal": 97, "prot": 9.0, "carbs": 3.9, "fat": 5.0, "health": 96, "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&auto=format&fit=crop&q=80"},
    ],
    'Staples & Grains': [
        {"name": "Premium Basmati Rice", "price": 160.00, "weight": "1 kg", "cal": 130, "prot": 2.7, "carbs": 28.0, "fat": 0.3, "health": 88, "img": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=80"},
        {"name": "Sona Masoori Rice", "price": 320.00, "weight": "5 kg", "cal": 130, "prot": 2.5, "carbs": 28.0, "fat": 0.4, "health": 86, "img": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=500&auto=format&fit=crop&q=80"},
        {"name": "Whole Wheat Atta", "price": 245.00, "weight": "5 kg", "cal": 340, "prot": 13.0, "carbs": 71.0, "fat": 2.5, "health": 92, "img": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=500&auto=format&fit=crop&q=80"},
        {"name": "Toor Dal (Arhar)", "price": 160.00, "weight": "1 kg", "cal": 343, "prot": 22.0, "carbs": 63.0, "fat": 1.5, "health": 95, "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=80"},
        {"name": "Chana Dal", "price": 95.00, "weight": "1 kg", "cal": 360, "prot": 20.0, "carbs": 60.0, "fat": 5.0, "health": 94, "img": "https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=500&auto=format&fit=crop&q=80"},
        {"name": "Moong Dal", "price": 140.00, "weight": "1 kg", "cal": 347, "prot": 24.0, "carbs": 63.0, "fat": 1.2, "health": 96, "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&auto=format&fit=crop&q=80"},
        {"name": "Rajma (Kidney Beans)", "price": 165.00, "weight": "1 kg", "cal": 333, "prot": 24.0, "carbs": 60.0, "fat": 0.8, "health": 93, "img": "https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=500&auto=format&fit=crop&q=80"},
        {"name": "Kabuli Chana (Chickpeas)", "price": 145.00, "weight": "1 kg", "cal": 364, "prot": 19.0, "carbs": 61.0, "fat": 6.0, "health": 94, "img": "https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?w=500&auto=format&fit=crop&q=80"},
        {"name": "Instant Rolled Oats", "price": 120.00, "weight": "1 kg", "cal": 389, "prot": 16.9, "carbs": 66.0, "fat": 6.9, "health": 97, "img": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=500&auto=format&fit=crop&q=80"},
        {"name": "Premium Maida Flour", "price": 48.00, "weight": "1 kg", "cal": 364, "prot": 10.0, "carbs": 76.0, "fat": 1.0, "health": 75, "img": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=500&auto=format&fit=crop&q=80"},
    ],
    'Spices & Masalas': [
        {"name": "Biryani & Masala Spices", "price": 85.00, "weight": "1 Pack", "cal": 250, "prot": 8.0, "carbs": 40.0, "fat": 10.0, "health": 88, "img": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=500&auto=format&fit=crop&q=80"},
        {"name": "Tata Iodized Salt", "price": 24.00, "weight": "1 kg", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 80, "img": "https://images.unsplash.com/photo-1518110168401-f2877ee2c88c?w=500&auto=format&fit=crop&q=80"},
        {"name": "Garam Masala Powder", "price": 88.00, "weight": "100g", "cal": 300, "prot": 10.0, "carbs": 50.0, "fat": 12.0, "health": 89, "img": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=500&auto=format&fit=crop&q=80"},
        {"name": "Red Chili Powder", "price": 80.00, "weight": "200g", "cal": 280, "prot": 12.0, "carbs": 56.0, "fat": 14.0, "health": 87, "img": "https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=500&auto=format&fit=crop&q=80"},
        {"name": "Turmeric Powder (Haldi)", "price": 62.00, "weight": "200g", "cal": 354, "prot": 8.0, "carbs": 65.0, "fat": 10.0, "health": 98, "img": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Cumin Seeds (Jeera)", "price": 85.00, "weight": "200g", "cal": 375, "prot": 18.0, "carbs": 44.0, "fat": 22.0, "health": 92, "img": "https://images.unsplash.com/photo-1514733670139-4d87a1941d55?w=500&auto=format&fit=crop&q=80"},
        {"name": "Mustard Seeds (Rai)", "price": 35.00, "weight": "200g", "cal": 508, "prot": 26.0, "carbs": 28.0, "fat": 36.0, "health": 90, "img": "https://images.unsplash.com/photo-1532336414038-cf19250c5757?w=500&auto=format&fit=crop&q=80"},
        {"name": "Green Cardamom (Elaichi)", "price": 160.00, "weight": "50g", "cal": 300, "prot": 11.0, "carbs": 68.0, "fat": 6.7, "health": 94, "img": "https://images.unsplash.com/photo-1509358271058-acd02cc93898?w=500&auto=format&fit=crop&q=80"},
        {"name": "Asafoetida (Hing)", "price": 65.00, "weight": "50g", "cal": 297, "prot": 4.0, "carbs": 67.0, "fat": 1.0, "health": 91, "img": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=500&auto=format&fit=crop&q=80"},
        {"name": "Black Pepper Powder", "price": 85.00, "weight": "100g", "cal": 255, "prot": 10.0, "carbs": 64.0, "fat": 3.3, "health": 93, "img": "https://images.unsplash.com/photo-1588252303782-7ccb8d6f92fb?w=500&auto=format&fit=crop&q=80"},
    ],
    'Oils & Ghee': [
        {"name": "Pure Cow Ghee", "price": 349.00, "weight": "500ml", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 99.5, "health": 85, "img": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=500&auto=format&fit=crop&q=80"},
        {"name": "Pure Buffalo Ghee", "price": 320.00, "weight": "500ml", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 99.5, "health": 84, "img": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=500&auto=format&fit=crop&q=80"},
        {"name": "Sunflower Cooking Oil", "price": 135.00, "weight": "1 Ltr", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 80, "img": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Mustard Cooking Oil", "price": 145.00, "weight": "1 Ltr", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 82, "img": "https://images.unsplash.com/photo-1620706857370-e1b9770e8bb1?w=500&auto=format&fit=crop&q=80"},
        {"name": "Saffola Gold Oil", "price": 155.00, "weight": "1 Ltr", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 85, "img": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=80"},
        {"name": "Pure Coconut Oil", "price": 225.00, "weight": "500ml", "cal": 862, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 86, "img": "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=500&auto=format&fit=crop&q=80"},
        {"name": "Filtered Groundnut Oil", "price": 175.00, "weight": "1 Ltr", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 83, "img": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Extra Virgin Olive Oil", "price": 599.00, "weight": "500ml", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 95, "img": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Cold Pressed Sesame Oil", "price": 180.00, "weight": "500ml", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 88, "img": "https://images.unsplash.com/photo-1620706857370-e1b9770e8bb1?w=500&auto=format&fit=crop&q=80"},
        {"name": "Rice Bran Oil", "price": 140.00, "weight": "1 Ltr", "cal": 884, "prot": 0.0, "carbs": 0.0, "fat": 100.0, "health": 84, "img": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=80"},
    ],
    'Snacks & Munchies': [
        {"name": "Classic Potato Chips", "price": 20.00, "weight": "50g", "cal": 536, "prot": 7.0, "carbs": 53.0, "fat": 34.0, "health": 65, "img": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&auto=format&fit=crop&q=80"},
        {"name": "Good Day Cookies", "price": 45.00, "weight": "150g", "cal": 490, "prot": 6.0, "carbs": 68.0, "fat": 22.0, "health": 70, "img": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500&auto=format&fit=crop&q=80"},
        {"name": "Parle-G Biscuits", "price": 30.00, "weight": "250g", "cal": 450, "prot": 6.5, "carbs": 77.0, "fat": 13.0, "health": 72, "img": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=500&auto=format&fit=crop&q=80"},
        {"name": "Haldiram Bhujia Sev", "price": 110.00, "weight": "400g", "cal": 580, "prot": 12.0, "carbs": 42.0, "fat": 40.0, "health": 68, "img": "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=500&auto=format&fit=crop&q=80"},
        {"name": "Kurkure Masala Munch", "price": 20.00, "weight": "90g", "cal": 550, "prot": 6.0, "carbs": 56.0, "fat": 34.0, "health": 62, "img": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&auto=format&fit=crop&q=80"},
        {"name": "Roasted Cashews", "price": 210.00, "weight": "200g", "cal": 553, "prot": 18.0, "carbs": 30.0, "fat": 44.0, "health": 88, "img": "https://images.unsplash.com/photo-1536591375315-1989938b7074?w=500&auto=format&fit=crop&q=80"},
        {"name": "Roasted Almonds", "price": 195.00, "weight": "200g", "cal": 579, "prot": 21.0, "carbs": 22.0, "fat": 50.0, "health": 93, "img": "https://images.unsplash.com/photo-1508061252966-f727f6265050?w=500&auto=format&fit=crop&q=80"},
        {"name": "Salted Pistachios", "price": 240.00, "weight": "200g", "cal": 562, "prot": 20.0, "carbs": 28.0, "fat": 45.0, "health": 91, "img": "https://images.unsplash.com/photo-1536591375315-1989938b7074?w=500&auto=format&fit=crop&q=80"},
        {"name": "Cheese Nacho Chips", "price": 50.00, "weight": "150g", "cal": 500, "prot": 7.0, "carbs": 62.0, "fat": 26.0, "health": 66, "img": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=500&auto=format&fit=crop&q=80"},
        {"name": "Dark Chocolate Bar 70%", "price": 99.00, "weight": "100g", "cal": 540, "prot": 8.0, "carbs": 46.0, "fat": 32.0, "health": 85, "img": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=500&auto=format&fit=crop&q=80"},
    ],
    'Beverages & Tea': [
        {"name": "Hyderabadi Irani Tea Powder", "price": 165.00, "weight": "250g", "cal": 100, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 85, "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&auto=format&fit=crop&q=80"},
        {"name": "Red Label Tea", "price": 260.00, "weight": "500g", "cal": 100, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 86, "img": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=500&auto=format&fit=crop&q=80"},
        {"name": "Tata Tea Gold", "price": 280.00, "weight": "500g", "cal": 100, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 88, "img": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=500&auto=format&fit=crop&q=80"},
        {"name": "Nescafe Instant Coffee", "price": 335.00, "weight": "200g", "cal": 2, "prot": 0.1, "carbs": 0.3, "fat": 0.0, "health": 84, "img": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500&auto=format&fit=crop&q=80"},
        {"name": "Bru Coffee", "price": 195.00, "weight": "200g", "cal": 2, "prot": 0.1, "carbs": 0.3, "fat": 0.0, "health": 82, "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500&auto=format&fit=crop&q=80"},
        {"name": "Mango Fruit Juice", "price": 110.00, "weight": "1 Ltr", "cal": 60, "prot": 0.2, "carbs": 15.0, "fat": 0.1, "health": 78, "img": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=500&auto=format&fit=crop&q=80"},
        {"name": "Orange Juice", "price": 135.00, "weight": "1 Ltr", "cal": 45, "prot": 0.7, "carbs": 10.0, "fat": 0.2, "health": 85, "img": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500&auto=format&fit=crop&q=80"},
        {"name": "Coca Cola Classic", "price": 40.00, "weight": "750ml", "cal": 42, "prot": 0.0, "carbs": 10.6, "fat": 0.0, "health": 60, "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=80"},
        {"name": "Sprite Lime Soda", "price": 40.00, "weight": "750ml", "cal": 39, "prot": 0.0, "carbs": 10.0, "fat": 0.0, "health": 60, "img": "https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=500&auto=format&fit=crop&q=80"},
        {"name": "Tender Coconut Water", "price": 50.00, "weight": "200ml", "cal": 19, "prot": 0.7, "carbs": 3.7, "fat": 0.2, "health": 98, "img": "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=500&auto=format&fit=crop&q=80"},
    ],
    'Bakery & Sweets': [
        {"name": "Whole Wheat Bread", "price": 45.00, "weight": "400g", "cal": 250, "prot": 9.0, "carbs": 43.0, "fat": 3.5, "health": 88, "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=80"},
        {"name": "White Sandwich Bread", "price": 35.00, "weight": "400g", "cal": 265, "prot": 8.0, "carbs": 49.0, "fat": 3.0, "health": 75, "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=80"},
        {"name": "Haldiram Rasgulla", "price": 220.00, "weight": "1 kg", "cal": 186, "prot": 4.0, "carbs": 38.0, "fat": 2.0, "health": 72, "img": "https://images.unsplash.com/photo-1587314168485-3236d6710814?w=500&auto=format&fit=crop&q=80"},
        {"name": "Soan Papdi", "price": 140.00, "weight": "500g", "cal": 500, "prot": 6.0, "carbs": 60.0, "fat": 26.0, "health": 68, "img": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=500&auto=format&fit=crop&q=80"},
        {"name": "Moti Choor Ladoo", "price": 180.00, "weight": "500g", "cal": 420, "prot": 5.0, "carbs": 55.0, "fat": 20.0, "health": 65, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80"},
        {"name": "Gulab Jamun", "price": 210.00, "weight": "1 kg", "cal": 300, "prot": 4.0, "carbs": 50.0, "fat": 10.0, "health": 70, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80"},
        {"name": "Kaju Katli", "price": 350.00, "weight": "250g", "cal": 480, "prot": 10.0, "carbs": 50.0, "fat": 25.0, "health": 76, "img": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=500&auto=format&fit=crop&q=80"},
        {"name": "Chocolate Cake Slice", "price": 85.00, "weight": "150g", "cal": 380, "prot": 5.0, "carbs": 52.0, "fat": 18.0, "health": 62, "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&auto=format&fit=crop&q=80"},
        {"name": "Garlic Butter Naan", "price": 40.00, "weight": "2 Pcs", "cal": 290, "prot": 8.0, "carbs": 48.0, "fat": 8.0, "health": 78, "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=80"},
        {"name": "Butter Croissant", "price": 65.00, "weight": "2 Pcs", "cal": 406, "prot": 8.2, "carbs": 45.0, "fat": 21.0, "health": 70, "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500&auto=format&fit=crop&q=80"},
    ],
    'Personal & Household': [
        {"name": "Dettol Antiseptic Liquid", "price": 210.00, "weight": "550ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 95, "img": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&auto=format&fit=crop&q=80"},
        {"name": "Dove Beauty Soap", "price": 175.00, "weight": "Pack of 3", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 90, "img": "https://images.unsplash.com/photo-1608248597260-6578616b30c2?w=500&auto=format&fit=crop&q=80"},
        {"name": "Colgate Toothpaste", "price": 115.00, "weight": "200g", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 92, "img": "https://images.unsplash.com/photo-1559598467-f8b76c8155d0?w=500&auto=format&fit=crop&q=80"},
        {"name": "Head & Shoulders Shampoo", "price": 275.00, "weight": "340ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 88, "img": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&auto=format&fit=crop&q=80"},
        {"name": "Surf Excel Detergent", "price": 140.00, "weight": "1 kg", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 85, "img": "https://images.unsplash.com/photo-1585421514738-01798e348b17?w=500&auto=format&fit=crop&q=80"},
        {"name": "Vim Dishwash Gel", "price": 120.00, "weight": "500ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 87, "img": "https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=500&auto=format&fit=crop&q=80"},
        {"name": "Harpic Toilet Cleaner", "price": 98.00, "weight": "500ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 86, "img": "https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?w=500&auto=format&fit=crop&q=80"},
        {"name": "Lizol Floor Cleaner", "price": 105.00, "weight": "500ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 89, "img": "https://images.unsplash.com/photo-1584483766114-2cea6facdf57?w=500&auto=format&fit=crop&q=80"},
        {"name": "Instant Hand Sanitizer", "price": 60.00, "weight": "100ml", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 94, "img": "https://images.unsplash.com/photo-1584483766114-2cea6facdf57?w=500&auto=format&fit=crop&q=80"},
        {"name": "Soft Facial Tissues", "price": 85.00, "weight": "Pack of 100", "cal": 0, "prot": 0.0, "carbs": 0.0, "fat": 0.0, "health": 90, "img": "https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=500&auto=format&fit=crop&q=80"},
    ],
}

def seed_categories():
    print("Seeding store categories...")
    cat_map = {}
    for cname, cimg in MAIN_10_CATEGORIES.items():
        cat, _ = Category.objects.get_or_create(name=cname)
        cat.image = cimg
        cat.save()
        cat_map[cname] = cat
    print(f"Successfully seeded {len(cat_map)} categories.")
    return cat_map

def seed_products(cat_map):
    print("Cleaning up old products and seeding EXACTLY 10 products per category...")
    Product.objects.all().delete()
    
    total_created = 0
    for cname, items in PRODUCTS_CATALOG.items():
        category = cat_map.get(cname)
        if not category:
            continue
        for pdata in items:
            Product.objects.create(
                name=pdata["name"],
                category=category,
                price=pdata["price"],
                stock=50,
                available=True,
                description=f"Fresh, premium quality {pdata['name']} sourced directly for our customers.",
                weight=pdata["weight"],
                calories=pdata["cal"],
                protein_g=pdata["prot"],
                carbs_g=pdata["carbs"],
                fat_g=pdata["fat"],
                health_score=pdata["health"],
                image=pdata["img"]
            )
            total_created += 1
        print(f"  -> Seeded {len(items)} products for category '{cname}'")
    print(f"Successfully seeded total of {total_created} unique products (10 per category).")

def seed_recipes():
    print("Seeding authentic recipes...")
    Recipe.objects.all().delete()

    cat_fruits = Category.objects.get(name="Fruits")
    cat_vegetables = Category.objects.get(name="Vegetables")
    cat_dairy = Category.objects.get(name="Dairy & Eggs")
    cat_beverages = Category.objects.get(name="Beverages & Tea")
    cat_staples = Category.objects.get(name="Staples & Grains")
    cat_spices = Category.objects.get(name="Spices & Masalas")

    p_rice = Product.objects.get(name="Premium Basmati Rice", category=cat_staples)
    p_paneer = Product.objects.get(name="Premium Fresh Paneer", category=cat_dairy)
    p_tomato = Product.objects.get(name="Fresh Tomatoes", category=cat_vegetables)
    p_onion = Product.objects.get(name="Fresh Onions", category=cat_vegetables)
    p_garlic = Product.objects.get(name="Fresh Garlic", category=cat_vegetables)
    p_butter = Product.objects.get(name="Amul Table Butter", category=cat_dairy)
    p_spices = Product.objects.get(name="Biryani & Masala Spices", category=cat_spices)
    p_milk = Product.objects.get(name="Fresh Whole Milk", category=cat_dairy)
    p_tea = Product.objects.get(name="Hyderabadi Irani Tea Powder", category=cat_beverages)

    recipe_data = [
        {
            "name": "Hyderabadi Veg Dum Biryani",
            "description": "Authentic Telangana style dum biryani made with fragrant Basmati rice, paneer, tomatoes, onions, and rich spices.",
            "prep_time": "35 Mins",
            "servings": 4,
            "calories_per_serving": 450,
            "health_tag": "Telangana Special 🌶️",
            "ingredients": [(p_rice, "1 kg"), (p_paneer, "250g"), (p_tomato, "500g"), (p_onion, "500g"), (p_garlic, "50g"), (p_butter, "100g"), (p_spices, "1 Pack")]
        },
        {
            "name": "Telangana Bagara Rice & Khatti Dal",
            "description": "Famous Telangana Bagara Annam served with tangy Hyderabadi tamarind tomato khatti dal.",
            "prep_time": "25 Mins",
            "servings": 3,
            "calories_per_serving": 380,
            "health_tag": "Traditional Flavor 🍲",
            "ingredients": [(p_rice, "1 kg"), (p_tomato, "500g"), (p_onion, "250g"), (p_garlic, "50g"), (p_butter, "50g")]
        },
        {
            "name": "Telangana Tomato Kura & Rice",
            "description": "Spicy home-style Telangana tomato curry cooked with fresh garlic, onions, and served with rice.",
            "prep_time": "15 Mins",
            "servings": 2,
            "calories_per_serving": 280,
            "health_tag": "Homestyle Spicy 🌶️",
            "ingredients": [(p_tomato, "500g"), (p_onion, "250g"), (p_garlic, "50g"), (p_rice, "500g")]
        },
        {
            "name": "Hyderabadi Irani Chai Bundle",
            "description": "Rich, creamy Hyderabadi Irani tea slow-brewed with fresh milk, cardamom, and ginger.",
            "prep_time": "10 Mins",
            "servings": 4,
            "calories_per_serving": 130,
            "health_tag": "Hyderabadi Special ☕",
            "ingredients": [(p_tea, "250g"), (p_milk, "1 Ltr")]
        },
    ]

    for data in recipe_data:
        recipe = Recipe.objects.create(
            name=data["name"],
            description=data["description"],
            prep_time=data["prep_time"],
            servings=data["servings"],
            calories_per_serving=data["calories_per_serving"],
            health_tag=data["health_tag"]
        )
        for prod, unit in data["ingredients"]:
            RecipeIngredient.objects.create(
                recipe=recipe,
                product=prod,
                unit_note=unit
            )

    print("Seeded recipe items successfully.")

def seed_all():
    cat_map = seed_categories()
    seed_products(cat_map)
    seed_recipes()
    print("Database seeding completed cleanly!")

if __name__ == '__main__':
    seed_all()
