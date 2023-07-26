# Use the official Python image as the base image
FROM python:3.11

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Add any system dependencies your Django project may require here (e.g., PostgreSQL client)

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy the entire Django project source code to the container
COPY . .

# Expose the Django development server port (adjust this if needed)
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]