# Product Aggregator Microservice

This repository contains a REST API JSON Python microservice designed to allow users to browse a product catalog and automatically update prices and number of items in stock from the provided offer service.

## Features

- CRUD operations for products.
- Automatically register products with the external offer service.
- Periodically query the external microservice for product offers.
- Read-only API to get product offers.
- User authentication and token-based access control.
- Uses an PostgreSQL database as the internal data store.
- Integrates with the offers microservice using JWT authentication.

## Requirements

- Docker
- Python 3.x

## Getting Started

### Installation using Docker

1. Clone the repository:

   ```bash
    git clone https://github.com/ozerodar/product-aggregator.git && cd product-aggregator

2. Build a docker image
    ```bash
    docker-compose build

3. Run a Docker container
    ```bash
    docker-compose up

The Swagger will be available at [127.0.0.1:8000](http://127.0.0.1:8000/api/docs/#/).

### User Authentication

1. Create a user via request ``POST /api/user/create``. Provide email and password in the request body (you can use simple email and password, we won't judge).

2. Generate a token using your email and password via request ``POST /api/user/token``

3. Use the token in the Authorization header for other endpoints:
    Authorization: ``Token {your_token}``

## Usage

- Users can create products that are registered on an external server.
- Users can access offers that are periodically updated.
- Token authentication ensures that different users can access their own products.

## Running test

- Tests are written using Django. Run them with:

    ```bash
    docker-compose run --rm app sh -c "python manage.py test"

### Notes

Note that offers for products get updated every 2 minutes so when you create a new product they might not come right away (wait a minute or so).
