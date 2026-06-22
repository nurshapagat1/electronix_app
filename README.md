Electronix Shop

An e-commerce web application built with Django.

---

Screenshots

(Add screenshots of your project here)

---

About

Electronix Shop is a full-featured online store for electronics built with Django.
Users can browse products, filter by categories, add items to their shopping cart, leave reviews, and track their orders.

The project includes an admin dashboard for managing products, categories, orders, and users.

This application was created as a hands-on project to improve full-stack web development skills using Django.

---

Features

- User Authentication
  
  - Registration
  - Login / Logout
  - Profile management

- Product Catalog
  
  - Browse electronics products
  - Product categories
  - Product details

- Shopping Cart
  
  - Add products to cart
  - Update quantity
  - Remove items

- Reviews System
  
  - Users can leave product reviews
  - View customer feedback

- Order Management
  
  - Create orders
  - Track order status:
    - Processing
    - Shipped
    - Delivered

- Admin Panel
  
  - Manage products
  - Manage categories
  - Manage orders
  - Manage users

- Responsive Design
  
  - Works on desktop and mobile devices

---

Tech Stack

Backend

- Python
- Django

Database

- PostgreSQL

Frontend

- HTML5
- CSS3
- JavaScript

Tools

- Git
- GitHub

Deployment

- Coming soon

---

Installation

Follow these steps to run the project locally.

1. Clone the repository

git clone https://github.com/nurshapagat1/electronix_app.git

Go to the project folder:

cd electronix_app

---

2. Create a virtual environment

Create a virtual environment:

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

---

3. Install dependencies

Install all required packages:

pip install -r requirements.txt

---

4. Configure environment variables

Create a ".env" file in the project root:

SECRET_KEY=your_secret_key
DEBUG=True

DATABASE_NAME=electronix_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

Update the values according to your local setup.

---

5. Setup PostgreSQL Database

Create a PostgreSQL database:

CREATE DATABASE electronix_db;

Make sure PostgreSQL is running and your credentials match the ".env" file.

---

6. Apply migrations

Run Django migrations:

python manage.py makemigrations

python manage.py migrate

---

7. Create an admin user

Create a superuser:

python manage.py createsuperuser

Enter:

- Username
- Email
- Password

---

8. Run the development server

Start the Django server:

python manage.py runserver

Open your browser:

http://127.0.0.1:8000/

---

Admin Panel

To access the admin dashboard:

http://127.0.0.1:8000/admin/

Login using the superuser account created earlier.

---

Project Structure

electronix_app/
│
├── apps/
│   ├── products/
│   ├── orders/
│   ├── accounts/
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
├── .env
└── README.md

---

Future Improvements

- Online payment integration
- Product search and filtering
- Wishlist functionality
- Email notifications
- Deployment with Docker
- Cloud hosting setup
---

Author:
Nurshapagat

GitHub: 
nurshapagat1

---

License

This project is for educational purposes.
