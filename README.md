## Final Project Part 1

### Part 1: Microservices Design and Dockerization

This project demonstrates a microservices architecture built using Python and Flask.
The project comprises three independent services. They communicate using RESTful APIs and are designed to be modular,
each with its own dedicated database using the Polyglot approach!.

## Table of Contents

- [Overview](#overview)
- [Architecture & Design](#architecture--design)
  - [Microservices Design](#microservices-design)
  - [Database Design](#database-design)
  - [Service Discovery](#service-discovery)
- [Project Structure](#project-structure)
- [Service Details](#service-details)
  - [User Service](#user-service)
  - [Product Service](#product-service)
  - [Notification Service](#notification-service)
- [Environment Setup(Installation) & Deployment](#environment-setup--deployment)
  - [Testing](#testing)
- [Architecture Diagrams](#architecture-diagrams)
  - [High-Level Architecture Diagram](#high-level-architecture-diagram)
  - [User Registration Sequence Diagram](#user-registration-sequence-diagram)

---

## Overview

This project consists of four microservices:

1. **User Service:** Handles user registration, authentication, and profile management.
2. **Product Service:** Manages product catalogs.
3. **Notification Service:** Sends email or SMS notifications.

---

## Architecture & Design

### Microservices Design

- **Modular Structure:** Each service is encapsulated as an independent Flask application with its own routes, business logic, and models.
- **RESTful Communication:** APIs follow RESTful conventions allowing healthy, standardized interactions between services.
- **Inter-service Communication:** Services interact via HTTP.

### Database Design

- **Polyglot Persistence:** Each microservice maintains its own database, ensuring isolation. For instance:
  - User Service uses one database.
  - Product Service uses a second, dedicated database.
- During development, SQLite was used.

### Service Discovery

- **Consul Integration:**  
  Each service includes a stub for registering with a Consul agent, which manages service discovery. Although we’ll revisit the detailed Consul integration later, the current setup lays the groundwork by including registration code in each service’s `app.py`.

---

## Project Structure

```bash
env
microservices_project/
├── user_service/
|   ├── app.py
|   ├── models.py
|   ├── routes.py
|   └── requirements.txt
├── product_service/
|   ├── app.py
|   ├── models.py
|   ├── routes.py
|   └── requirements.txt
├── notification_service/
|   ├── app.py
|   ├── routes.py
|   └── requirements.txt
└── docker-compose.yml
```

---

## Service Details

### User Service

**Responsibilities:**

- Handles user registration and authentication.
- Manages user profiles.

**Endpoints:**

- **POST `/users/register`**  
  Registers a new user.  
  **Request Body:**
  ```json
  {
    "username": "exampleUser",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

**Response:**
Returns a success message and the created user details.

- **POST `/users/login`**
  Authenticates an existing user.
  **Request Body Example:**

```json
{
  "username": "exampleUser",
  "password": "securepassword"
}
```

**Response:** On success, returns a confirmation along with user details; otherwise, an error message.

**Database Schema:**

**User Table:** Contains fields for id, username, email, and password

**Consul Registration:** The service includes a function in app.py to register with Consul for service discovery.

### Product Service

**Responsibilities:**
Manages the product catalog.

Endpoints:

- **GET `/products/`**
  Retrieves a list of all products.

- **POST `/products/`**
  Adds a new product to the catalog.
  **Request Body Example:**

```json
{
  "name": "Product Name",
  "description": "A brief description of the product",
  "price": 19.99
}
```

**Response:**
Returns a success message along with the product details.

**Database Schema:**

**Product Table:** Contains fields for id, name, description, and price.

**Consul Registration:** Similar to the User Service, it includes registration code to auto-register with Consul.

### Notification Service

**Responsibilities:**

Sends notifications via email or SMS (simulated in this setup).

**Endpoints:**

- **POST `/notifications/send`**
  Sends a notification.
  **Request Body Example:**

```json
{
  "type": "email",
  "recipient": "user@example.com",
  "message": "Your order has been processed!"
}
```

**Response:** Returns a success message indicating the type of notification sent and its recipient.

## Environment Setup & Deployment

**Prerequisites**

- Python 3.10 or above
- Docker & Docker Compose (for containerized deployment)
- Sqlite (my preferred database system)

**Local Development**
Setup Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

**Install Dependencies for Each Service:**

For example, for the User Service:

```bash
cd user_service
pip install -r requirements.txt
cd ..
# Repeat for each service folder.
```

Run Each Service Individually:

```
bash
python services/user_service/app.py
python services/product_service/app.py
python services/notification_service/app.py
```

**Deployment with Docker Compose**
A pre-configured docker-compose.yml is provided to start all services concurrently. To deploy, run:

```bash
docker-compose up --build
```

This file defines containers for each microservice, separate PostgreSQL databases for each service, and a Consul container for service discovery.

### Testing

To run a general test on all the endpoints to ensure they are working, you will need to start the server of all three services(You will open three terminal windows and run each service separately)
and then simply run in the terminal

```bash
python test_services.py
```

And this should be the expected output

```cmd
psh ⚡  python .\test_services.py
=== Testing User Service ===
User Registration Response: 201 {'message': 'User registered successfully', 'user': {'email': 'testuser@example.com', 'id': 1, 'username': 'testuser'}}
User Login Response: 200 {'message': 'Login successful', 'user': {'email': 'testuser@example.com', 'id': 1, 'username': 'testuser'}}

=== Testing Product Service ===
Product Creation Response: 201 {'message': 'Product added successfully', 'product': {'description': 'A test product', 'id': 1, 'name': 'Test Product', 'price': 19.99}}
Product List Response: 200 [{'description': 'A test product', 'id': 1, 'name': 'Test Product', 'price': 19.99}]

=== Testing Notification Service ===
Notification Response: 201 {'message': 'Email notification sent to user@example.com'}

All tests passed successfully!
```

## Architecture Diagrams

**High-Level Architecture Diagram**

```bash
                           +------------------+
                           |   API Gateway    |
                           +--------+---------+
                                    |
          +-------------------------+
          |                         |
+---------v--------+       +--------v--------+
|  User Service    |       |  Product Service|
|   (5000 port)    |       |   (5001 port)   |
+------------------+       +-----------------+
            \                          |
             \                         |
              \                +-------v-----------------+
               ---------------+ Notification Service    |
                                |      (5003 port)        |
                                +-------------------------+

                   Service Discovery via Consul (port 8500)
```

**User Registration Sequence Diagram**

```bash
User (Client)         User Service                User DB
   |                       |                         |
   | POST /users/register  |                         |
   |---------------------->|                         |
   |                       | Insert new user record  |
   |                       |------------------------>|
   |                       |                         |
   |                       | <----- Confirmation ----|
   | <--- 201 Created -----|                         |
```
