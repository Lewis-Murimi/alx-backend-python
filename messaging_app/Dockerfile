# Use base Python image
FROM python:3.10

# Set environment variables to prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into container
COPY . /app/

# Expose port for Django
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver","-p", "0.0.0.0:8000"]
