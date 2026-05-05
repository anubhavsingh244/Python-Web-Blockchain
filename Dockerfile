# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Create a non-root user
RUN useradd -m appuser

# Set the working directory inside the container
WORKDIR /app
RUN chown appuser:appuser /app

# Copy only the requirements file first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
# This includes app.py, static/, and templates/
COPY --chown=appuser:appuser . .

# Expose the port Flask listens on
EXPOSE 5000

# Switch to the non-root user
USER appuser

# Command to run the application using Gunicorn (recommended for production)
# Assuming your Flask app instance is named 'app' in 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# If you were debugging and wanted to use Flask's dev server (NOT for production):
# CMD ["python", "app.py"]
