# Step 1: Use an official Python image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy your project files into the container
COPY . /app

# Step 4: Install the libraries needed for your app
RUN pip install flask flask-sqlalchemy

# Step 5: Tell Docker which port the app runs on
EXPOSE 5000

# Step 6: The command to run your app
CMD ["python", "app.py"]