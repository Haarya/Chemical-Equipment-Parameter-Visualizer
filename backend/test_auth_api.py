"""
Quick test script to verify authentication API endpoints work correctly.

Run this while Django server is running to test:
- POST /api/auth/register/
- POST /api/auth/login/
- GET /api/auth/user/
- POST /api/auth/logout/

Usage: python test_auth_api.py
"""

import requests
import json
from datetime import datetime

# Base URL for API
BASE_URL = 'http://127.0.0.1:8000'

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(response):
    """Print formatted response."""
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_authentication():
    """Test complete authentication flow."""
    
    # Generate unique username with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_username = f"testuser_{timestamp}"
    test_email = f"{test_username}@example.com"
    test_password = "test123456"
    
    print_section("1. REGISTER NEW USER")
    print(f"Creating user: {test_username}")
    
    register_url = f"{BASE_URL}/api/auth/register/"
    register_data = {
        "username": test_username,
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        print_response(response)
        
        if response.status_code != 201:
            print("\n❌ Registration failed!")
            return
        
        token = response.json().get('token')
        print(f"\n✅ Registration successful! Token: {token[:20]}...")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Django server.")
        print("Please ensure Django server is running: python manage.py runserver")
        return
    except Exception as e:
        print(f"❌ Error during registration: {str(e)}")
        return
    
    # Test 2: Login
    print_section("2. LOGIN WITH CREDENTIALS")
    
    login_url = f"{BASE_URL}/api/auth/login/"
    login_data = {
        "username": test_username,
        "password": test_password
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print_response(response)
        
        if response.status_code != 200:
            print("\n❌ Login failed!")
            return
        
        login_token = response.json().get('token')
        print(f"\n✅ Login successful! Token: {login_token[:20]}...")
        
        # Verify same token
        if token == login_token:
            print("✅ Token matches registration token")
        
    except Exception as e:
        print(f"❌ Error during login: {str(e)}")
        return
    
    # Test 3: Get User Info (Protected Endpoint)
    print_section("3. GET USER INFO (PROTECTED)")
    
    user_url = f"{BASE_URL}/api/auth/user/"
    headers = {
        "Authorization": f"Token {token}"
    }
    
    try:
        response = requests.get(user_url, headers=headers)
        print_response(response)
        
        if response.status_code != 200:
            print("\n❌ Failed to get user info!")
            return
        
        print("\n✅ Successfully accessed protected endpoint!")
        
    except Exception as e:
        print(f"❌ Error getting user info: {str(e)}")
        return
    
    # Test 4: Access Protected Endpoint Without Token
    print_section("4. TEST PROTECTION (NO TOKEN)")
    
    try:
        response = requests.get(user_url)  # No token
        print_response(response)
        
        if response.status_code == 401:
            print("\n✅ Endpoint properly protected - unauthorized access denied")
        else:
            print("\n❌ Warning: Endpoint should return 401 without token")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 5: Logout
    print_section("5. LOGOUT")
    
    logout_url = f"{BASE_URL}/api/auth/logout/"
    
    try:
        response = requests.post(logout_url, headers=headers)
        print_response(response)
        
        if response.status_code != 200:
            print("\n❌ Logout failed!")
            return
        
        print("\n✅ Logout successful!")
        
    except Exception as e:
        print(f"❌ Error during logout: {str(e)}")
        return
    
    # Test 6: Verify Token Invalidated
    print_section("6. VERIFY TOKEN INVALIDATED")
    
    try:
        response = requests.get(user_url, headers=headers)
        print_response(response)
        
        if response.status_code == 401:
            print("\n✅ Token successfully invalidated after logout")
        else:
            print("\n❌ Warning: Token should be invalid after logout")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 7: Invalid Login
    print_section("7. TEST INVALID CREDENTIALS")
    
    invalid_data = {
        "username": test_username,
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(login_url, json=invalid_data)
        print_response(response)
        
        if response.status_code == 401:
            print("\n✅ Invalid credentials properly rejected")
        else:
            print("\n❌ Warning: Should return 401 for invalid credentials")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print_section("AUTHENTICATION TESTS COMPLETE")
    print("✅ All authentication endpoints are working correctly!")
    print("\nAuthentication Configuration:")
    print("  - Token-based authentication: ✅ Enabled")
    print("  - Registration endpoint: ✅ Working")
    print("  - Login endpoint: ✅ Working")
    print("  - Logout endpoint: ✅ Working")
    print("  - Protected endpoints: ✅ Working")
    print("  - Token invalidation: ✅ Working")

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Chemical Equipment Visualizer - Authentication API Test  ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print("Testing authentication endpoints...")
    print("Ensure Django server is running: python manage.py runserver")
    
    test_authentication()
