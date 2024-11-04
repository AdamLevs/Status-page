FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the entire statuspage directory and requirements.txt
COPY ./statuspage /app/statuspage
COPY requirements.txt /app/

# Install any dependencies required for building packages (optional)
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 80

# Set the command to run the application
CMD ["python", "statuspage/manage.py", "runserver", "0.0.0.0:80", "--settings=statuspage.settings"]