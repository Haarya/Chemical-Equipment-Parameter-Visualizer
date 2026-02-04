"""
API Root View - Shows available endpoints when accessing root URL.
"""

from django.http import JsonResponse
from django.views import View


class APIRootView(View):
    """
    API Root endpoint that lists all available endpoints.
    
    GET / or GET /api/
    """
    
    def get(self, request):
        """Return list of available API endpoints."""
        
        base_url = request.build_absolute_uri('/').rstrip('/')
        
        endpoints = {
            "message": "Welcome to Chemical Equipment Parameter Visualizer API",
            "version": "1.0.0",
            "status": "operational",
            "endpoints": {
                "Authentication": {
                    "register": f"{base_url}/api/auth/register/",
                    "login": f"{base_url}/api/auth/login/",
                    "logout": f"{base_url}/api/auth/logout/",
                    "user_info": f"{base_url}/api/auth/user/"
                },
                "Equipment Data": {
                    "upload_csv": f"{base_url}/api/upload/",
                    "list_datasets": f"{base_url}/api/datasets/",
                    "dataset_detail": f"{base_url}/api/datasets/<id>/",
                    "dataset_summary": f"{base_url}/api/datasets/<id>/summary/",
                    "download_pdf": f"{base_url}/api/datasets/<id>/report/pdf/"
                },
                "Admin": {
                    "admin_panel": f"{base_url}/admin/"
                }
            },
            "documentation": {
                "Authentication": {
                    "register": {
                        "method": "POST",
                        "url": "/api/auth/register/",
                        "body": {
                            "username": "string",
                            "email": "string",
                            "password": "string"
                        },
                        "response": {
                            "token": "string",
                            "user": {"id": "int", "username": "string", "email": "string"}
                        }
                    },
                    "login": {
                        "method": "POST",
                        "url": "/api/auth/login/",
                        "body": {
                            "username": "string",
                            "password": "string"
                        },
                        "response": {
                            "token": "string",
                            "user": {"id": "int", "username": "string", "email": "string"}
                        }
                    },
                    "logout": {
                        "method": "POST",
                        "url": "/api/auth/logout/",
                        "headers": {
                            "Authorization": "Token <your_token>"
                        }
                    }
                },
                "CSV Upload": {
                    "method": "POST",
                    "url": "/api/upload/",
                    "body": "multipart/form-data with 'file' field containing CSV",
                    "csv_columns": [
                        "Equipment Name",
                        "Type",
                        "Flowrate",
                        "Pressure",
                        "Temperature"
                    ]
                }
            },
            "postman_collection": f"{base_url}/api/postman-collection/",
            "sample_data": "sample_data/sample_equipment_data.csv"
        }
        
        return JsonResponse(endpoints, json_dumps_params={'indent': 2})
