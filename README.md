# 🧘 Fitness Class Booking API

A simple Django REST API that allows users to view available fitness classes and book a slot.

---

## 🚀 Features

- List upcoming fitness classes
- Book a fitness class (with email-based uniqueness)
- View bookings by client email
- Timezone-aware class schedule
- Prevent overbooking

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- virtualenv (optional but recommended)
- PostgreSQL or SQLite

### 1. Clone the Repository

```bash
git clone https://github.com/shreemanikanta/fitness-class-booking-apis.git
cd fitness-booking-api
```

### 2. Create Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. (Optional) Create a Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

## 🔌 API Endpoints

### 1. List Upcoming Fitness Classes

- **Endpoint:** `GET /api/classes/`
- **Optional Timezone Parameter:**
  - Pass `?timezone=Asia/Kolkata` or any valid [pytz timezone]

#### 📦 Example (cURL)
```bash
curl -X GET "http://127.0.0.1:8000/api/classes/?timezone=Asia/Kolkata"
```

## 📌 2. Book a Class

**Endpoint:** `POST /api/book/`

**Request Body:**

```json
{
  "fitness_class": "uuid-of-class",
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```

**Example (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/book/ \
-H "Content-Type: application/json" \
-d '{
  "fitness_class": "your-class-uuid-here",
  "client_name": "John Doe",
  "client_email": "john@example.com"
}'
```

## 3. 📋 View Bookings by Email

**Endpoint:** `GET /api/bookings/?email=john@example.com`

**Example (cURL):**
```bash
curl "http://127.0.0.1:8000/api/bookings/?email=john@example.com"
```

### 🧪 Run Tests
```bash
python manage.py test
```

