FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2023-10-30

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
