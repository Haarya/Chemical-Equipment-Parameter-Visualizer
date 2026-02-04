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
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    
    Authentication: Optional (set to AllowAny, change to IsAuthenticated if needed)
    """
    
    permission_classes = [AllowAny]  # Change to [IsAuthenticated] to require login
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
            
            # Save Dataset
            dataset = dataset_serializer.save()
            
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
    
    def get_queryset(self):
        """
        Return last 5 datasets ordered by upload date (most recent first).
        
        SECURITY: Only return datasets, no filtering to prevent information disclosure.
        """
        return Dataset.objects.all().order_by('-uploaded_at')[:5]


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
    queryset = Dataset.objects.all()
    
    def get_object(self):
        """
        Retrieve dataset by ID.
        
        SECURITY: Returns 404 if not found (prevents information disclosure).
        """
        dataset_id = self.kwargs.get('pk')
        return get_object_or_404(Dataset, pk=dataset_id)


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
    queryset = Dataset.objects.all()
    
    def get_object(self):
        """
        Retrieve dataset by ID for deletion.
        
        SECURITY: Returns 404 if not found.
        """
        dataset_id = self.kwargs.get('pk')
        return get_object_or_404(Dataset, pk=dataset_id)


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
        Get summary statistics for a specific dataset.
        """
        # SECURITY: Validate ID and return 404 if not found
        dataset = get_object_or_404(Dataset, pk=pk)
        
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
        Generate and return PDF report for a specific dataset.
        """
        # SECURITY: Validate ID
        dataset = get_object_or_404(Dataset, pk=pk)
        
        # Get equipment records
        equipment_records = Equipment.objects.filter(dataset=dataset).order_by('equipment_name')
        
        # Create PDF in memory
        buffer = io.BytesIO()
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            # Container for PDF elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a5490'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c5aa0'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            title = Paragraph("Chemical Equipment Parameter Report", title_style)
            elements.append(title)
            
            # Dataset information
            info_text = f"<b>Dataset:</b> {dataset.name}<br/>"
            info_text += f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            info_text += f"<b>Total Records:</b> {dataset.total_records}"
            
            info_para = Paragraph(info_text, styles['Normal'])
            elements.append(info_para)
            elements.append(Spacer(1, 0.3*inch))
            
            # Summary Statistics Section
            summary_heading = Paragraph("Summary Statistics", heading_style)
            elements.append(summary_heading)
            
            summary_data = [
                ['Metric', 'Value', 'Unit'],
                ['Average Flowrate', f"{dataset.avg_flowrate:.2f}", 'm³/h'],
                ['Average Pressure', f"{dataset.avg_pressure:.2f}", 'bar'],
                ['Average Temperature', f"{dataset.avg_temperature:.2f}", '°C'],
            ]
            
            summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Equipment Type Distribution
            type_heading = Paragraph("Equipment Type Distribution", heading_style)
            elements.append(type_heading)
            
            type_data = [['Equipment Type', 'Count', 'Percentage']]
            for equip_type, count in dataset.type_distribution.items():
                percentage = (count / dataset.total_records) * 100
                type_data.append([equip_type, str(count), f"{percentage:.1f}%"])
            
            type_table = Table(type_data, colWidths=[2.5*inch, 1*inch, 1*inch])
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(type_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Equipment Data Table
            data_heading = Paragraph("Equipment Data", heading_style)
            elements.append(data_heading)
            
            # Prepare equipment data
            equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
            
            for equipment in equipment_records[:50]:  # Limit to first 50 for PDF size
                equipment_data.append([
                    equipment.equipment_name[:15],  # Truncate long names
                    equipment.equipment_type[:12],
                    f"{equipment.flowrate:.1f}",
                    f"{equipment.pressure:.1f}",
                    f"{equipment.temperature:.1f}"
                ])
            
            if equipment_records.count() > 50:
                equipment_data.append(['...', '(additional records omitted)', '', '', ''])
            
            equipment_table = Table(equipment_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 1*inch, 0.8*inch])
            equipment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            elements.append(equipment_table)
            
            # Build PDF
            doc.build(elements)
            
            # Get PDF content
            pdf_content = buffer.getvalue()
            buffer.close()
            
            # Create response
            response = HttpResponse(pdf_content, content_type='application/pdf')
            
            # SECURITY: Sanitize filename
            safe_filename = dataset.name.replace(' ', '_').replace('/', '_')[:50]
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}_{safe_filename}.pdf"'
            
            return response
        
        except Exception as e:
            buffer.close()
            
            # SECURITY: Don't expose internal errors in production
            if settings.DEBUG:
                error_detail = str(e)
            else:
                error_detail = 'Error generating PDF report'
            
            return Response(
                {'error': 'PDF generation failed', 'details': error_detail},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
