import requests
import json

# Testing User Service endpoints
def test_user_registration():
    url = "http://localhost:5000/users/register"
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password"
    }
    response = requests.post(url, json=payload)
    print("User Registration Response:", response.status_code, response.json())
    assert response.status_code == 201, "User registration failed"
    return response.json()  # Expecting {"message": "User registered successfully", "user": { ... }}

def test_user_login():
    url = "http://localhost:5000/users/login"
    payload = {
        "username": "testuser",
        "password": "password"
    }
    response = requests.post(url, json=payload)
    print("User Login Response:", response.status_code, response.json())
    assert response.status_code == 200, "User login failed"

# Testing Product Service endpoints
def test_product_creation():
    url = "http://localhost:5001/products/"
    payload = {
        "name": "Test Product",
        "description": "A test product",
        "price": 19.99
    }
    response = requests.post(url, json=payload)
    print("Product Creation Response:", response.status_code, response.json())
    assert response.status_code == 201, "Product creation failed"
    return response.json()  # Expecting {"message": "Product added successfully", "product": { ... }}

def test_product_list():
    url = "http://localhost:5001/products/"
    response = requests.get(url)
    print("Product List Response:", response.status_code, response.json())
    assert response.status_code == 200, "Fetching product list failed"

# Testing Notification Service endpoints
def test_notification():
    url = "http://localhost:5003/notifications/send"
    payload = {
        "type": "email",
        "recipient": "user@example.com",
        "message": "Your order has been processed!"
    }
    response = requests.post(url, json=payload)
    print("Notification Response:", response.status_code, response.json())
    assert response.status_code == 201, "Notification sending failed"
    return response.json()

def main():
    print("=== Testing User Service ===")
    test_user_registration()
    test_user_login()

    print("\n=== Testing Product Service ===")
    test_product_creation()
    test_product_list()

    print("\n=== Testing Notification Service ===")
    test_notification()

    print("\nAll tests passed successfully!")

if __name__ == '__main__':
    main()
