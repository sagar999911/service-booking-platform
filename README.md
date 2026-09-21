# 🛠️ Service Booking Platform

A full-stack service booking platform built with **Python and Django**, inspired by platforms like Urban Company.

The platform allows customers to discover services, add services to a cart, manage their profile and addresses, complete checkout, and manage their bookings.

> 🚧 This project is actively under development. New features and improvements are being added continuously.

---

## AWS Deployment Architecture

The application is deployed on AWS using:

- Amazon EC2 - Django application server
- Nginx - Reverse proxy
- Gunicorn - WSGI application server
- Amazon RDS PostgreSQL - Production database
- AWS Systems Manager - Remote EC2 management and deployment
- IAM - Access control
- GitHub Actions - CI/CD
- GitHub OIDC - Secure GitHub-to-AWS authentication

### CI/CD Flow

Local development
→ GitHub
→ GitHub Actions
→ GitHub OIDC
→ AWS IAM
→ AWS Systems Manager
→ EC2
→ deploy.sh
→ Gunicorn
→ Nginx

---

## 📸 Project Preview

Screenshots and a live demo will be added after deployment.

---

## ✨ Current Features

### 👤 Customer Management

- Customer registration
- Customer login/logout
- Customer profile management
- Update customer information
- Multiple address management
- Add, edit and manage customer addresses

### 🛠️ Service Management

- Service categories
- Sub-categories
- Main services
- Service administration
- Browse services by category and sub-category

### 🛒 Cart

- Add services to cart
- View cart
- Manage cart items
- Checkout process

### 📅 Booking

- Create booking from checkout
- Customer booking history
- View customer bookings
- Booking structure for future provider workflow

---

## 🔄 Current Customer Flow

```text
Customer
   │
   ▼
Signup / Login
   │
   ▼
Browse Categories
   │
   ▼
Select Sub-category
   │
   ▼
Browse Services
   │
   ▼
Add Service to Cart
   │
   ▼
Cart
   │
   ▼
Checkout
   │
   ▼
Select Address
   │
   ▼
Confirm Booking
   │
   ▼
My Bookings