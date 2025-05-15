# Step 1: Use an official Python runtime as the base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 4: Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Django project files into the container
COPY . /app/

# Step 6: Set environment variables (for Django settings)
ENV PYTHONUNBUFFERED=1

# Step 7: Expose the port that Django will run on
EXPOSE 8000

# Step 8: Run migrations and start the Django development server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
