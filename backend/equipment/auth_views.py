"""
Authentication API Views for Chemical Equipment Parameter Visualizer.

Provides endpoints for user registration, login, and logout.
Uses Django REST Framework Token Authentication.

SECURITY:
- Password hashing via Django's default PBKDF2 algorithm
- Token-based authentication for API access
- Input validation on registration
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError


class RegisterView(APIView):
    """
    User Registration Endpoint.
    
    POST /api/auth/register/
    
    Request Body:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    
    Returns:
    {
        "token": "string",
        "user": {
            "id": int,
            "username": "string",
            "email": "string"
        }
    }
    
    SECURITY:
    - Username uniqueness enforced by database
    - Password is hashed before storage
    - Input validation for required fields
    - Email validation
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Create a new user account and return authentication token.
        """
        # Extract data from request
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        
        # SECURITY: Validate required fields
        if not username:
            return Response(
                {'error': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not password:
            return Response(
                {'error': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # SECURITY: Validate username length and format
        if len(username) < 3:
            return Response(
                {'error': 'Username must be at least 3 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(username) > 150:
            return Response(
                {'error': 'Username must be less than 150 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # SECURITY: Validate password strength
        if len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # SECURITY: Basic email format validation
        if '@' not in email or '.' not in email:
            return Response(
                {'error': 'Invalid email format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create user (password will be hashed automatically)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Generate authentication token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response(
                {
                    'message': 'User registered successfully',
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                },
                status=status.HTTP_201_CREATED
            )
        
        except IntegrityError:
            # Username already exists
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {'error': 'Registration failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    """
    User Login Endpoint.
    
    POST /api/auth/login/
    
    Request Body:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
    {
        "token": "string",
        "user": {
            "id": int,
            "username": "string",
            "email": "string"
        }
    }
    
    SECURITY:
    - Authentication via Django's authenticate() function
    - Password verification against hashed database value
    - Token returned for subsequent API requests
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Authenticate user and return token.
        """
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        
        # SECURITY: Validate required fields
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # SECURITY: Authenticate user (checks hashed password)
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user account is active
        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response(
            {
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    User Logout Endpoint.
    
    POST /api/auth/logout/
    
    Headers:
    Authorization: Token <token>
    
    Returns:
    {
        "message": "Logged out successfully"
    }
    
    SECURITY:
    - Requires valid authentication token
    - Deletes token on logout (invalidates future requests)
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Delete user's authentication token.
        """
        try:
            # Delete the user's token
            request.user.auth_token.delete()
            
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': 'Logout failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserInfoView(APIView):
    """
    Get Current User Information.
    
    GET /api/auth/user/
    
    Headers:
    Authorization: Token <token>
    
    Returns:
    {
        "id": int,
        "username": "string",
        "email": "string"
    }
    
    SECURITY:
    - Requires valid authentication token
    - Returns only authenticated user's information
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Return current authenticated user's information.
        """
        user = request.user
        
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_200_OK
        )
