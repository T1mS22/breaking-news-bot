# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the working directory
COPY requirements.txt requirements.txt

# Install the dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . .

# Run the bot.py script when the container starts
CMD ["python3", "bot.py"]
