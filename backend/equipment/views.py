"""
API Views for Chemical Equipment Parameter Visualizer.

SECURITY: All views implement OWASP best practices:
- Input validation and sanitization
- Rate limiting (via DRF throttling)
- Authentication required where appropriate
- Error handling without exposing sensitive information
"""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

import pandas as pd
import io
from datetime import datetime
from collections import Counter

from .models import Dataset, Equipment
from .serializers import (
    DatasetListSerializer,
    DatasetDetailSerializer,
    DatasetSummarySerializer,
    EquipmentSerializer,
    FileUploadSerializer,
    DatasetCreateSerializer
)

# For PDF generation
from reports.pdf_generator import PDFReportGenerator


class CSVUploadView(APIView):
    """
    API View for uploading CSV files containing equipment data.
    
    POST /api/upload/
    
    SECURITY:
    - File validation (type, size, content)
    - CSV column validation
    - Data sanitization
    - Row limit enforcement (prevent DoS)
    - Automatic cleanup (keep last 5 datasets)
    
    Authentication: Required
    """
    
    permission_classes = [IsAuthenticated]
    # Rate limiting: Applied via DRF throttling in settings
    
    def post(self, request):
        """
        Handle CSV file upload.
        
        Expected CSV columns:
        - Equipment Name
        - Type
        - Flowrate
        - Pressure
        - Temperature
        """
        # SECURITY: Validate file upload using serializer
        file_serializer = FileUploadSerializer(data=request.data)
        
        if not file_serializer.is_valid():
            return Response(
                {'error': 'Invalid file upload', 'details': file_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = file_serializer.validated_data['file']
        
        try:
            # Read CSV file with Pandas
            # SECURITY: Read as text first to prevent binary exploits
            try:
                csv_data = uploaded_file.read().decode('utf-8')
                df = pd.read_csv(io.StringIO(csv_data))
            except UnicodeDecodeError:
                # Try different encodings
                uploaded_file.seek(0)
                csv_data = uploaded_file.read().decode('latin-1')
                df = pd.read_csv(io.StringIO(csv_data))
            
            # SECURITY: Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {
                        'error': 'Invalid CSV format',
                        'details': f"Missing required columns: {', '.join(missing_columns)}",
                        'required_columns': required_columns,
                        'found_columns': list(df.columns)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # SECURITY: Check row count limit (prevent DoS)
            max_rows = getattr(settings, 'MAX_CSV_ROWS', 10000)
            if len(df) > max_rows:
                return Response(
                    {
                        'error': 'File too large',
                        'details': f"CSV contains {len(df)} rows, maximum allowed is {max_rows}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # SECURITY: Check for empty dataset
            if len(df) == 0:
                return Response(
                    {'error': 'Empty dataset', 'details': 'CSV file contains no data rows'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Clean column names (remove extra spaces)
            df.columns = df.columns.str.strip()
            
            # SECURITY: Drop rows with missing values in critical columns
            initial_count = len(df)
            df = df.dropna(subset=required_columns)
            dropped_count = initial_count - len(df)
            
            if len(df) == 0:
                return Response(
                    {'error': 'No valid data', 'details': 'All rows contain missing values'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # SECURITY: Validate data types and ranges
            try:
                # Convert numeric columns
                df['Flowrate'] = pd.to_numeric(df['Flowrate'], errors='coerce')
                df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
                df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
                
                # Drop rows with invalid numeric values
                df = df.dropna(subset=['Flowrate', 'Pressure', 'Temperature'])
                
                if len(df) == 0:
                    return Response(
                        {'error': 'Invalid data', 'details': 'All numeric values are invalid'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # SECURITY: Validate numeric ranges
                validation_errors = []
                
                if (df['Flowrate'] < 0).any() or (df['Flowrate'] > 10000).any():
                    validation_errors.append("Flowrate values must be between 0 and 10,000")
                
                if (df['Pressure'] < 0).any() or (df['Pressure'] > 1000).any():
                    validation_errors.append("Pressure values must be between 0 and 1,000")
                
                if (df['Temperature'] < -273.15).any() or (df['Temperature'] > 5000).any():
                    validation_errors.append("Temperature values must be between -273.15 and 5,000")
                
                if validation_errors:
                    return Response(
                        {'error': 'Invalid data ranges', 'details': validation_errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
            except Exception as e:
                return Response(
                    {'error': 'Data conversion error', 'details': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # SECURITY: Sanitize string fields
            df['Equipment Name'] = df['Equipment Name'].astype(str).str.strip()
            df['Type'] = df['Type'].astype(str).str.strip()
            
            # SECURITY: Validate string field lengths
            if (df['Equipment Name'].str.len() > 100).any():
                return Response(
                    {'error': 'Invalid data', 'details': 'Equipment Name exceeds 100 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if (df['Type'].str.len() > 50).any():
                return Response(
                    {'error': 'Invalid data', 'details': 'Equipment Type exceeds 50 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate summary statistics
            total_records = len(df)
            avg_flowrate = float(df['Flowrate'].mean())
            avg_pressure = float(df['Pressure'].mean())
            avg_temperature = float(df['Temperature'].mean())
            
            # Calculate type distribution
            type_counts = df['Type'].value_counts().to_dict()
            
            # Create Dataset record
            dataset_data = {
                'name': uploaded_file.name,
                'total_records': total_records,
                'avg_flowrate': avg_flowrate,
                'avg_pressure': avg_pressure,
                'avg_temperature': avg_temperature,
                'type_distribution': type_counts
            }
            
            dataset_serializer = DatasetCreateSerializer(data=dataset_data)
            
            if not dataset_serializer.is_valid():
                return Response(
                    {'error': 'Dataset validation failed', 'details': dataset_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save Dataset with the logged-in user
            dataset = dataset_serializer.save(user=request.user)
            
            # Create Equipment records in bulk
            equipment_records = []
            for _, row in df.iterrows():
                equipment_records.append(
                    Equipment(
                        dataset=dataset,
                        equipment_name=row['Equipment Name'],
                        equipment_type=row['Type'],
                        flowrate=row['Flowrate'],
                        pressure=row['Pressure'],
                        temperature=row['Temperature']
                    )
                )
            
            # Bulk create for efficiency
            Equipment.objects.bulk_create(equipment_records)
            
            # Return summary
            summary_serializer = DatasetSummarySerializer(dataset)
            
            response_data = {
                'message': 'CSV file uploaded successfully',
                'dataset': summary_serializer.data,
                'warnings': []
            }
            
            if dropped_count > 0:
                response_data['warnings'].append(
                    f"{dropped_count} rows were dropped due to missing values"
                )
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except pd.errors.EmptyDataError:
            return Response(
                {'error': 'Empty file', 'details': 'The uploaded CSV file is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except pd.errors.ParserError as e:
            return Response(
                {'error': 'CSV parsing error', 'details': f'Unable to parse CSV file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # SECURITY: Don't expose internal error details in production
            if settings.DEBUG:
                error_detail = str(e)
            else:
                error_detail = 'An error occurred while processing the file'
            
            return Response(
                {'error': 'Processing error', 'details': error_detail},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DatasetListView(generics.ListAPIView):
    """
    API View for listing all datasets (last 5).
    
    GET /api/datasets/
    
    Returns: List of datasets with basic information (id, name, uploaded_at, total_records)
    
    SECURITY:
    - Authentication required
    - Read-only access
    - Automatic ordering by most recent first
    """
    
    serializer_class = DatasetListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # No pagination - only 5 results max
    
    def get_queryset(self):
        """
        Return last 5 datasets for the logged-in user, ordered by upload date (most recent first).
        
        SECURITY: Only return datasets owned by the authenticated user.
        """
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]


class DatasetDetailView(generics.RetrieveAPIView):
    """
    API View for retrieving full dataset details with all equipment records.
    
    GET /api/datasets/<id>/
    
    Returns: Complete dataset information including nested equipment records
    
    SECURITY:
    - Authentication required
    - Read-only access
    - Validates dataset ID exists
    """
    
    serializer_class = DatasetDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only return datasets owned by the authenticated user."""
        return Dataset.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Retrieve dataset by ID for the logged-in user.
        
        SECURITY: Returns 404 if not found or not owned by user.
        """
        dataset_id = self.kwargs.get('pk')
        return get_object_or_404(Dataset, pk=dataset_id, user=self.request.user)


class DatasetDeleteView(generics.DestroyAPIView):
    """
    API View for deleting a dataset.
    
    DELETE /api/datasets/<id>/
    
    Deletes: Dataset and all associated equipment records (CASCADE)
    
    SECURITY:
    - Authentication required
    - Returns 204 No Content on success
    - Returns 404 if dataset not found
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only return datasets owned by the authenticated user."""
        return Dataset.objects.filter(user=self.request.user)
    
    def get_object(self):
        """
        Retrieve dataset by ID for deletion.
        
        SECURITY: Returns 404 if not found or not owned by user.
        """
        dataset_id = self.kwargs.get('pk')
        return get_object_or_404(Dataset, pk=dataset_id, user=self.request.user)


class DatasetSummaryView(APIView):
    """
    API View for retrieving dataset summary statistics.
    
    GET /api/datasets/<id>/summary/
    
    Returns: Summary statistics (total_count, averages, type_distribution)
    
    SECURITY:
    - Authentication required
    - Read-only access
    - Validates dataset ID
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """
        Get summary statistics for a specific dataset owned by the user.
        """
        # SECURITY: Validate ID and user ownership, return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        serializer = DatasetSummarySerializer(dataset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GeneratePDFReportView(APIView):
    """
    API View for generating PDF reports.
    
    GET /api/datasets/<id>/report/pdf/
    
    Generates a PDF report containing:
    - Dataset summary statistics
    - Equipment type distribution table
    - Complete equipment data table
    
    SECURITY:
    - Authentication required
    - Read-only access
    - PDF generated on-the-fly (no file storage)
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """
        Generate and return PDF report for a specific dataset owned by the user.
        """
        # SECURITY: Validate ID and user ownership
        try:
            dataset = Dataset.objects.get(pk=pk, user=request.user)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found', 'detail': f'No dataset found with id {pk} for your account'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get equipment records
        equipment_records = Equipment.objects.filter(dataset=dataset).order_by('equipment_name')
        
        try:
            # Prepare dataset information
            dataset_info = {
                'id': dataset.id,
                'name': dataset.name,
                'upload_date': dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                'total_records': dataset.total_records
            }
            
            # Prepare summary statistics
            summary_stats = {
                'avg_flowrate': dataset.avg_flowrate,
                'avg_pressure': dataset.avg_pressure,
                'avg_temperature': dataset.avg_temperature
            }
            
            # Prepare equipment data as list of dicts
            equipment_data = [
                {
                    'equipment_name': eq.equipment_name,
                    'equipment_type': eq.equipment_type,
                    'flowrate': eq.flowrate,
                    'pressure': eq.pressure,
                    'temperature': eq.temperature
                }
                for eq in equipment_records
            ]
            
            # Initialize PDF generator
            pdf_generator = PDFReportGenerator()
            
            # Generate PDF report
            pdf_buffer = pdf_generator.generate_report(
                dataset_info=dataset_info,
                summary_stats=summary_stats,
                type_distribution=dataset.type_distribution,
                equipment_data=equipment_data,
                include_chart=False  # Optional: can add chart later
            )
            
            # Get PDF content
            pdf_content = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            # Create response with proper headers
            response = HttpResponse(pdf_content, content_type='application/pdf')
            
            # SECURITY: Sanitize filename
            safe_filename = dataset.name.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}_{safe_filename}.pdf"'
            response['Content-Length'] = len(pdf_content)
            # Expose headers for CORS
            response['Access-Control-Expose-Headers'] = 'Content-Disposition, Content-Length, Content-Type'
            
            return response
        
        except Exception as e:
            # SECURITY: Don't expose internal errors in production
            import traceback
            if settings.DEBUG:
                error_detail = str(e)
            else:
                error_detail = 'Error generating PDF report'
                # Log the full traceback for debugging
                print(f'PDF generation error for dataset {pk}: {traceback.format_exc()}')
            
            return Response(
                {'error': 'PDF generation failed', 'details': error_detail},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
