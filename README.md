# 🛒 Online Grocery Store System (OGS)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

The **Online Grocery Store System (OGS)** is a full-stack, feature-rich web application built with **Django**, **HTML5/CSS3/JavaScript**, **Razorpay Payment Gateway**, **Groq AI (Llama 3)**, and **Tesseract OCR**. It offers an end-to-end shopping experience complete with AI grocery recommendations, intelligent list scanning, automated PDF invoice generation, and an administrative dashboard.

---

## 📌 Table of Contents
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
  - [Prerequisites](#1-prerequisites)
  - [Installation & Virtual Environment](#2-installation--virtual-environment)
  - [Environment Configuration](#3-environment-configuration)
  - [Database Setup & Seeding](#4-database-setup--seeding)
  - [Running the Application](#5-running-the-application)
- [Environment Variables](#-environment-variables)
- [Evaluation Access Credentials](#-evaluation-access-credentials)
- [License](#-license)

---

## 🚀 Key Features

### 🛒 1. Customer Shopping Experience
- **Catalog & Search:** Category filtering, live search by product name/tags, dynamic sorting by price, rating, or popularity.
- **Cart & Wishlist:** Real-time quantity updates, coupon discount calculation, and persistent user shopping cart.
- **Checkout & Tracking:** Multi-step address selection, order confirmation, and real-time status updates (Pending, Processing, Out for Delivery, Delivered).

### 💳 2. Payment Gateway & Invoicing
- **Razorpay Integration:** Complete sandbox payment flow supporting UPI, Cards, NetBanking, and Cash on Delivery (COD).
- **Automated PDF Invoices:** Instant downloadable PDF receipts generated programmatically via `ReportLab`.

### 🤖 3. AI Grocery Assistant & OCR Scanner
- **AI Grocery Chatbot (Groq / Llama 3):** Product recommendations, recipe advice, and conversational cart insertion.
- **OCR Grocery List Scanner:** Image upload for hand-written lists or receipts using OpenCV and Tesseract OCR to automatically match and add products to cart.

### 🍲 4. Recipe & Meal Kit Builder
- Regional and continental recipe directory with exact ingredient breakdowns.
- One-click **"Buy All Ingredients"** to seamlessly add all recipe items directly to cart.

### 📊 5. Security & Store Administration
- **Email OTP Authentication:** User registration and password resets backed by Gmail SMTP and 6-digit OTP verification.
- **Admin Management Portal:** Dedicated dashboard for inventory management, stock levels, orders, coupons, and user inquiries.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10+ / Django 5.0+ |
| **Frontend UI** | HTML5, CSS3, JavaScript (Vanilla) |
| **Database** | SQLite3 (Default relational database) |
| **Payment Gateway** | Razorpay Python SDK |
| **Artificial Intelligence** | Groq API (Llama 3 70B / 8B) |
| **Computer Vision / OCR** | Tesseract OCR & OpenCV (`cv2`) |
| **PDF Generation** | ReportLab |
| **Authentication** | Django Auth + Email OTP Verification |

---

## 📂 Project Architecture

```text
Online_Grocery_Store/
├── manage.py                   # Django primary CLI entrypoint
├── seed_database.py            # Database auto-seeding script (categories, products, recipes)
├── build_submission_zip.py     # Academic submission packager
├── requirements.txt            # Python dependencies manifest
├── .env.example                # Template for environment configuration
├── .gitignore                  # Git exclusion rules
├── LICENSE                     # MIT Open Source License
├── README.md                   # Project documentation
│
├── online_grocery/             # Django Core Configuration Package
│   ├── __init__.py
│   ├── settings.py             # Global Django configuration & environment loader
│   ├── urls.py                 # Core routing table
│   ├── wsgi.py                 # WSGI web server deployment interface
│   └── asgi.py                 # ASGI asynchronous web server interface
│
├── ogs/                        # Main Application Module
│   ├── admin.py                # Admin portal registration & configuration
│   ├── ai_assistant.py         # Groq AI chatbot logic & prompt engineering
│   ├── apps.py                 # App configuration
│   ├── context_processors.py   # Global dynamic context (cart badge counter)
│   ├── forms.py                # Form definitions (OCR image upload form)
│   ├── models.py               # Database ORM models (Product, Category, Order, Cart, etc.)
│   ├── tests.py                # Unit test suite
│   ├── urls.py                 # App routing table
│   ├── utils.py                # General utility functions
│   ├── views.py                # Controller handlers & view logic
│   ├── migrations/             # Database migration history
│   ├── static/                 # Static Assets (CSS, JS, Icons)
│   └── templates/              # Jinja2 / Django HTML templates
│
└── media/                      # Product & Category Seed Images
    ├── categories/             # Category thumbnails
    └── products/               # Product imagery
```

---

## 💻 Getting Started

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- **Tesseract-OCR** (Optional, required for hand-written OCR scanner feature):
  - **Windows:** Download installer from [UB-Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki).
  - **macOS:** `brew install tesseract`
  - **Linux:** `sudo apt-get install tesseract-ocr`

### 2. Installation & Virtual Environment
Clone the repository and set up a virtual environment:

```bash
# Clone the repository
git clone https://github.com/nallapremteja04/Online_Grocery_Store.git
cd Online_Grocery_Store

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Configure your credentials inside `.env`:
```ini
SECRET_KEY=your_django_secret_key
GROQ_API_KEY=your_groq_api_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

### 4. Database Setup & Seeding
Run Django database migrations and seed sample data:

```bash
# Apply database migrations
python manage.py migrate

# Seed sample categories, products, and recipes
python seed_database.py
```

### 5. Running the Application
Launch the Django development server:

```bash
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## 🔑 Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | No | Django secret key (defaults to a dev key if unspecified) |
| `DEBUG` | No | Debug mode flag (`True` / `False`, defaults to `True`) |
| `GROQ_API_KEY` | Optional | Groq Cloud API key for AI Assistant |
| `RAZORPAY_KEY_ID` | Optional | Razorpay Key ID for payment sandbox |
| `RAZORPAY_KEY_SECRET` | Optional | Razorpay Key Secret for payment signature validation |
| `EMAIL_HOST_USER` | Optional | Gmail address for sending OTP emails |
| `EMAIL_HOST_PASSWORD` | Optional | Gmail App Password for SMTP authentication |
| `TESSERACT_CMD` | Optional | Custom absolute path to `tesseract` binary |

---

## 🔑 Evaluation Access Credentials

For quick evaluation and testing:

| Role | Username / Email | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | `http://127.0.0.1:8000/admin/` |
| **Store Manager** | `manager` | `admin123` | `http://127.0.0.1:8000/admin-dashboard/` |
| **Test Customer** | `customer1` | `password123` | `http://127.0.0.1:8000/login/` |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
