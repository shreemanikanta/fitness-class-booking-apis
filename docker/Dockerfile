# Use an official Python runtime as a parent image
FROM python:3.9.5
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY fitness_booking/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev python3-dev && apt-get install -y build-essential

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project code
COPY . .

# Expose port 8000 to the host
EXPOSE 8010

# For development: run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]