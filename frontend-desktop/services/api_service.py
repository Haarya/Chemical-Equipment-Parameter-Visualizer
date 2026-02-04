"""
API Service for communicating with Django backend
"""

import requests
from typing import Optional, Dict, Any, List


class APIService:
    """Handle all API requests to Django backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API service
        
        Args:
            base_url: Base URL of the Django backend
        """
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
        
    def set_token(self, token: str):
        """Set authentication token for requests"""
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
        
    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login user
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Response data with token
        """
        url = f"{self.base_url}/api/auth/login/"
        data = {"username": username, "password": password}
        response = self.session.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'token' in result:
            self.set_token(result['token'])
            
        return result
    
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Register new user
        
        Args:
            username: Desired username
            email: User's email
            password: Desired password
            
        Returns:
            Response data with token
        """
        url = f"{self.base_url}/api/auth/register/"
        data = {"username": username, "email": email, "password": password}
        response = self.session.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'token' in result:
            self.set_token(result['token'])
            
        return result
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout current user
        
        Returns:
            Response data
        """
        url = f"{self.base_url}/api/auth/logout/"
        response = self.session.post(url)
        response.raise_for_status()
        self.clear_token()
        return response.json()
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Response data with dataset info
        """
        url = f"{self.base_url}/api/upload/"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(url, files=files)
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """
        Get list of all datasets
        
        Returns:
            List of datasets
        """
        url = f"{self.base_url}/api/datasets/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset_detail(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get detailed dataset information
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dataset details with equipment records
        """
        url = f"{self.base_url}/api/datasets/{dataset_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset_summary(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get dataset summary statistics
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Summary statistics
        """
        url = f"{self.base_url}/api/datasets/{dataset_id}/summary/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def download_pdf_report(self, dataset_id: int, save_path: str) -> bool:
        """
        Download PDF report for dataset
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path to save the PDF file
            
        Returns:
            True if successful
        """
        url = f"{self.base_url}/api/datasets/{dataset_id}/report/pdf/"
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
        return True
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """
        Delete a dataset
        
        Args:
            dataset_id: ID of the dataset to delete
            
        Returns:
            True if successful
        """
        url = f"{self.base_url}/api/datasets/{dataset_id}/delete/"
        response = self.session.delete(url)
        response.raise_for_status()
        return True
