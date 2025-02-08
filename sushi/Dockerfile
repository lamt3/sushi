# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED True

# Set the working directory
WORKDIR /tuna

# Install Poetry
RUN pip install poetry

# Copy the project files
COPY . .

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose port for the app
EXPOSE 8080

# Run the FastAPI application
CMD ["uvicorn", "tuna.app:app", "--host", "0.0.0.0", "--port", "8080"]