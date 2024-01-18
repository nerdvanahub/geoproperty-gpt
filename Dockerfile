FROM python:3.11

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt

# Path: /app
COPY . .

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
CMD ["python", "app.py"]