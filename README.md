# E-Commerce API Documentation

## Overview

This Django REST API project provides:

- User registration with email OTP verification
- Login with JWT tokens
- Profile picture upload
- Product catalog listing
- Admin-only product create, update, delete

Base API prefix:

- `/api/`

Authentication and security:

- OTP verification is used for new user activation
- JWT tokens are issued on successful login
- `access_token` and `refresh_token` cookies are set after login
- `session_token` cookie is used during OTP verification

---

## Authentication Flow

### 1. Register a user

Endpoint: `POST /api/accounts/register/`

- Registers a new user
- Sends OTP to user email
- Returns `session_token` cookie valid for 15 minutes

Payload:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "john_doe",
  "email": "john@example.com",
  "password": "StrongPassword123!",
  "phone_number": "+1234567890",
  "role": "customer"
}
```

Successful response:

```json
{
  "message": "User registered successfully. Please check your email for the OTP to verify your account."
}
```

### 2. Verify OTP

Endpoint: `POST /api/accounts/verify-otp/`

- Verifies the OTP sent to the user email
- Activates the account and marks it as verified
- Requires the `session_token` cookie from registration/login

Payload:

```json
{
  "otp": "123456"
}
```

Successful response:

```json
{
  "message": "OTP verified successfully. Your account is now active."
}
```

### 3. Login

Endpoint: `POST /api/accounts/login/`

- Authenticates a verified user
- If account is not verified, it resends OTP and sets `session_token`
- On success, sets `access_token` and `refresh_token` cookies

Payload:

```json
{
  "email": "john@example.com",
  "password": "StrongPassword123!"
}
```

Successful response:

```json
{
  "message": "Login successful."
}
```

If user is not verified:

```json
{
  "message": "User is not verified. A new OTP has been sent to your email."
}
```

### Token cookies

- `session_token` — used only during OTP verification
- `access_token` — JWT access token, expires in 60 minutes
- `refresh_token` — JWT refresh token, expires in 1 day

> Note: The backend uses `rest_framework_simplejwt` for authentication.

---

## Accounts API

### Register

- URL: `POST /api/accounts/register/`
- Public
- Returns `201 Created`

Fields:

- `first_name` (string, required)
- `last_name` (string, required)
- `username` (string, required)
- `email` (string, required)
- `password` (string, required)
- `phone_number` (string, optional)
- `role` (string, optional, default `customer`)

### Verify OTP

- URL: `POST /api/accounts/verify-otp/`
- Public (requires `session_token` cookie)

Fields:

- `otp` (string or integer, required)

### Login

- URL: `POST /api/accounts/login/`
- Public

Fields:

- `email` (string, required)
- `password` (string, required)

### Profile Picture

- URL: `GET /api/accounts/profile-picture/`
- URL: `POST /api/accounts/profile-picture/`
- Requires authentication
- Uses `permissions.IsAuthenticated`

Upload payload example (multipart form):

- `image`: file

Success response:

```json
{
  "message": "Profile picture uploaded successfully."
}
```

Get profile picture response example:

```json
{
  "id": "<uuid>",
  "user": "<user_uuid>",
  "image": "https://.../profile_pictures/myphoto.jpg",
  "created_at": "2026-05-20T12:34:56Z",
  "updated_at": "2026-05-20T12:34:56Z"
}
```

---

## Products API

### List Products

- URL: `GET /api/products/`
- Public
- Returns active products only

Response example:

```json
[
  {
    "id": 1,
    "category": {
      "id": 10,
      "name": "Electronics"
    },
    "title": "Smart Phone",
    "description": "A nice smartphone.",
    "price": "499.99",
    "stock": 25,
    "image": "https://.../products/phone.jpg",
    "created_at": "2026-05-20T12:00:00Z"
  }
]
```

### Create Product

- URL: `POST /api/products/`
- Admin only
- Requires authentication

Payload:

```json
{
  "category_id": 10,
  "title": "Smart Phone",
  "description": "A nice smartphone.",
  "price": "499.99",
  "stock": 25,
  "image": "https://.../products/phone.jpg"
}
```

### Product Detail

- URL: `GET /api/products/<id>/`
- Public
- Returns a single product record

### Update Product

- URL: `PUT /api/products/<id>/`
- Admin only
- Requires authentication

Payload fields are the same as create. Partial updates may be supported via `PATCH` if the client uses it.

### Delete Product

- URL: `DELETE /api/products/<id>/`
- Admin only
- Requires authentication

---

## Data Models

### User

Fields include:

- `id` (UUID)
- `first_name`
- `last_name`
- `username`
- `email`
- `phone_number`
- `role` (`customer`, `admin`, `VENDOR`)
- `is_active`
- `is_verified`
- `date_joined`
- `last_login`

### ProfilePicture

Fields:

- `id` (UUID)
- `user` (one-to-one)
- `image`
- `created_at`
- `updated_at`

### Product

Fields:

- `id`
- `category`
- `title`
- `description`
- `price`
- `stock`
- `image`
- `is_active`
- `created_at`

### Category

Fields:

- `id`
- `name`

---

## Setup & Environment

### Required environment variables

- `SECRET_KEY`
- `DEBUG`
- `SMTP_SERVER`
- `SMTP_PORT`
- `MAIL_USERNAME`
- `EMAIL_HOST_PASSWORD`
- `FROM_EMAIL`
- `CLOUD_NAME`
- `API_KEY`
- `API_SECRET`

### Local setup commands

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Celery

This project uses Celery with Redis:

- `CELERY_BROKER_URL = redis://redis:6379/0`
- `CELERY_RESULT_BACKEND = redis://redis:6379/0`

Start Celery worker separately if using async email tasks.

---

## Notes and behavior

- OTPs are hashed and stored in the database.
- OTP expiration is 10 minutes.
- If login is attempted on an unverified account, a new OTP is sent.
- `profile-picture/` upload creates or updates the current user profile picture.
- Product creation, update, and deletion are protected for admin users only.

---

## Useful URLs

- Admin panel: `/admin/`
- API root prefix: `/api/`
- Accounts: `/api/accounts/`
- Products: `/api/products/`
