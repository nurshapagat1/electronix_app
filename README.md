# Electronix Shop

An e-commerce web application built with Django.

---

## About

Electronix Shop is an online store for electronics. Users can browse products, add items to their cart, leave reviews, and track their orders. The site also includes an admin panel for managing products, orders, and users.

---

## Features

- User registration and login
- Product catalog with categories
- Add products to cart
- Write and view product reviews
- Order tracking with status updates
- Admin panel for full site management
- Responsive design (mobile-friendly)

---

## Tech Stack

- Backend: Django (Python)
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript
- Deployment: [platform, if deployed]
- Version Control: Git / GitHub

------
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nurshapagat1/electronix_app.git
   cd electronix_app
```
2. Create a virtual environment:
  to create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a .env file in the root directory with:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the server:
   ```bash
   python manage.py runserver
   ```
8. Open http://127.0.0.1:8000 in your browser.

---



Future Improvements

· Integrate payment system (Stripe / Kaspi Pay)
· Add product search and filters
· Email notifications for orders
· User order history

---

Author

Nurshapagat
GitHub: nurshapagat1

---
