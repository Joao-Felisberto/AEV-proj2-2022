FROM python:3.8-alpine

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install Flask pyjwt

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY database database

COPY controllers controllers

COPY JS JS

COPY static static

COPY templates templates

COPY token_factory token_factory

COPY util util

COPY app.py .
# Expose port the server is reachable on
EXPOSE 8080

CMD python -m flask run -h 0.0.0.0 -p 8080
