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


