# Django Payments & Orders Management (Chapter 9 - Django By Example)

## Overview
This repository implements payment processing and order management features in a Django project, based on **Chapter 9 of Django By Example**. It demonstrates how to integrate **Stripe** for credit card payments, manage order statuses, export order data in CSV format, and generate PDF invoices dynamically.

## Features
- **Stripe Payment Gateway Integration**: Secure credit card payments.
- **Order Management**: Track and mark orders as paid.
- **Payment Notifications**: Handle Stripe webhooks.
- **Admin Enhancements**:
  - Export orders to **CSV**.
  - Custom admin order detail view.
  - Generate **PDF invoices** dynamically.
- **Celery & RabbitMQ**: Handle asynchronous tasks such as sending invoices.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file and configure the following variables:
```sh
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
```

### 5. Apply Migrations
```sh
python manage.py migrate
```

### 6. Create a Superuser
```sh
python manage.py createsuperuser
```

### 7. Run the Server
```sh
python manage.py runserver
```

## Usage
- Visit `http://127.0.0.1:8000/` to browse the shop.
- Add products to the cart and proceed to checkout.
- Use Stripe's test card `4242 4242 4242 4242` (expiry: any future date, CVV: any 3 digits) to simulate payments.
- Access the admin panel at `http://127.0.0.1:8000/admin/` to manage orders.

## Technologies Used
- **Django 5**
- **Stripe API**
- **Celery & RabbitMQ**
- **Django Admin Customization**
- **CSV & PDF Generation**

## License
This project is based on the implementation from **Django By Example** and follows its licensing terms.

---
Feel free to contribute or modify as needed!