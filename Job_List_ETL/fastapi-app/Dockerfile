# Use Python 3.9 Alpine as the base image
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /code

# Copy requirements.txt into the container
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the FastAPI app into the container
COPY . /code/

# Expose the FastAPI app port (default is 81 as per your command)
EXPOSE 81

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81"]
