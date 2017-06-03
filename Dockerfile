FROM python:3
RUN mkdir -p /app
WORKDIR /app
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt