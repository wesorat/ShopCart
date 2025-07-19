# ShopCart (Educational Project)

Django e-commerce platform with Stripe payments, Celery tasks and Redis caching.

## Local Setup (Windows)

### Without Docker:
1. Start services in separate terminals:
   ```bash
   stripe listen --forward-to localhost:8000/payment/stripe-webhook/
   redis-server
   celery -A ShopCart worker --pool=solo --loglevel=info
   celery -A ShopCart flower
2. Run Django server:
   ```bash
   python manage.py runserver

4. First-Time Setup
  Create superuser and generate test products:
   ```bash
   python manage.py createsuperuser
   python manage.py fake_products

## Key Features
Stripe payments

Celery background tasks

Redis caching and task queue  

Django REST API

## Tech Stack
Backend: Django, DRF, Celery 

Frontend: HTML/CSS 

Infra: Docker, PostgreSQL, Redis, Nginx
