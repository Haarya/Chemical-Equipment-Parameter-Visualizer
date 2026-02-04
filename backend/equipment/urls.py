"""
URL Configuration for Equipment API endpoints.

All routes prefixed with /api/ (configured in config/urls.py)
"""

from django.urls import path
from .views import (
    CSVUploadView,
    DatasetListView,
    DatasetDetailView,
    DatasetDeleteView,
    DatasetSummaryView,
    GeneratePDFReportView
)

app_name = 'equipment'

urlpatterns = [
    # CSV Upload Endpoint
    # POST /api/upload/
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    
    # Dataset Listing Endpoint
    # GET /api/datasets/
    path('datasets/', DatasetListView.as_view(), name='dataset-list'),
    
    # Dataset Detail Endpoint
    # GET /api/datasets/<id>/
    path('datasets/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    
    # Dataset Delete Endpoint
    # DELETE /api/datasets/<id>/
    path('datasets/<int:pk>/delete/', DatasetDeleteView.as_view(), name='dataset-delete'),
    
    # Dataset Summary Endpoint
    # GET /api/datasets/<id>/summary/
    path('datasets/<int:pk>/summary/', DatasetSummaryView.as_view(), name='dataset-summary'),
    
    # PDF Report Generation Endpoint
    # GET /api/datasets/<id>/report/pdf/
    path('datasets/<int:pk>/report/pdf/', GeneratePDFReportView.as_view(), name='dataset-pdf-report'),
]
