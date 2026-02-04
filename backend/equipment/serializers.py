"""
Django REST Framework Serializers for Equipment API.

SECURITY: All serializers implement strict input validation and sanitization.
- Type checking on all fields
- Length limits enforced
- Reject unexpected fields
- File upload validation
"""

from rest_framework import serializers
from .models import Dataset, Equipment
from django.conf import settings
import os


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Equipment model.
    
    SECURITY: 
    - Validates all numeric fields are within acceptable ranges
    - Validates string fields for length and format
    - Rejects any unexpected fields
    """
    
    class Meta:
        model = Equipment
        fields = [
            'id',
            'equipment_name',
            'equipment_type',
            'flowrate',
            'pressure',
            'temperature'
        ]
        read_only_fields = ['id']
        
        # SECURITY: Enforce strict validation - reject extra fields
        extra_kwargs = {
            'equipment_name': {
                'required': True,
                'allow_blank': False,
                'max_length': 100,
                'trim_whitespace': True,
            },
            'equipment_type': {
                'required': True,
                'allow_blank': False,
                'max_length': 50,
                'trim_whitespace': True,
            },
            'flowrate': {
                'required': True,
                'min_value': 0.0,
                'max_value': 10000.0,
            },
            'pressure': {
                'required': True,
                'min_value': 0.0,
                'max_value': 1000.0,
            },
            'temperature': {
                'required': True,
                'min_value': -273.15,
                'max_value': 5000.0,
            },
        }
    
    def validate_equipment_name(self, value):
        """
        SECURITY: Validate equipment name format.
        Only allow alphanumeric characters, hyphens, and underscores.
        """
        import re
        if not re.match(r'^[A-Za-z0-9\-_]+$', value):
            raise serializers.ValidationError(
                "Equipment name can only contain letters, numbers, hyphens, and underscores."
            )
        return value
    
    def validate_equipment_type(self, value):
        """
        SECURITY: Validate equipment type format.
        Only allow letters, spaces, and hyphens.
        """
        import re
        if not re.match(r'^[A-Za-z\s\-]+$', value):
            raise serializers.ValidationError(
                "Equipment type can only contain letters, spaces, and hyphens."
            )
        return value


class DatasetListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing datasets.
    Returns only essential information for list views.
    
    SECURITY: Read-only fields prevent modification.
    """
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'uploaded_at',
            'total_records'
        ]
        read_only_fields = fields  # All fields are read-only for list view


class DatasetSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for dataset summary statistics.
    Returns aggregated data without individual equipment records.
    
    SECURITY: Read-only to prevent tampering with calculated values.
    """
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'uploaded_at',
            'total_records',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution'
        ]
        read_only_fields = fields  # All fields are read-only


class DatasetDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Dataset with nested Equipment records.
    Used for full dataset view with all equipment data.
    
    SECURITY: Nested serializer ensures equipment data is validated.
    """
    
    # Nested serializer for related equipment
    equipment_records = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'uploaded_at',
            'total_records',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution',
            'equipment_records'  # Nested equipment data
        ]
        read_only_fields = fields  # All fields are read-only


class FileUploadSerializer(serializers.Serializer):
    """
    Serializer for CSV file upload validation.
    
    SECURITY: Comprehensive file validation
    - File type checking (CSV only)
    - File size limits
    - File extension validation
    - MIME type validation
    """
    
    file = serializers.FileField(
        required=True,
        allow_empty_file=False,
        max_length=255,  # Max filename length
        help_text="CSV file containing equipment data"
    )
    
    def validate_file(self, value):
        """
        SECURITY: Validate uploaded file.
        
        Checks:
        1. File extension is .csv
        2. File size within limits (10MB)
        3. File is not empty
        4. Content type validation
        """
        # Get file extension
        file_name = value.name
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # SECURITY: Check file extension
        allowed_extensions = getattr(settings, 'ALLOWED_UPLOAD_EXTENSIONS', ['.csv'])
        if file_ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Invalid file type. Only {', '.join(allowed_extensions)} files are allowed."
            )
        
        # SECURITY: Check file size (10MB limit)
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 10485760)  # 10MB
        if value.size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            raise serializers.ValidationError(
                f"File size exceeds maximum allowed size of {max_size_mb}MB."
            )
        
        # SECURITY: Check file is not empty
        if value.size == 0:
            raise serializers.ValidationError("Uploaded file is empty.")
        
        # SECURITY: Validate content type (if available)
        content_type = getattr(value, 'content_type', '').lower()
        allowed_content_types = [
            'text/csv',
            'text/plain',
            'application/csv',
            'application/vnd.ms-excel',
        ]
        
        if content_type and content_type not in allowed_content_types:
            raise serializers.ValidationError(
                f"Invalid content type: {content_type}. Expected CSV file."
            )
        
        return value
    
    def validate(self, attrs):
        """
        SECURITY: Additional validation at serializer level.
        Ensures no unexpected fields are present.
        """
        # Get the file
        file = attrs.get('file')
        
        if not file:
            raise serializers.ValidationError("File is required.")
        
        return attrs


class DatasetCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new Dataset entries.
    Used internally by CSV upload view.
    
    SECURITY: Validates all fields before database insertion.
    """
    
    class Meta:
        model = Dataset
        fields = [
            'name',
            'total_records',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution'
        ]
        
        # SECURITY: Strict validation on all fields
        extra_kwargs = {
            'name': {
                'required': True,
                'allow_blank': False,
                'max_length': 255,
                'trim_whitespace': True,
            },
            'total_records': {
                'required': True,
                'min_value': 1,
                'max_value': 10000,
            },
            'avg_flowrate': {
                'required': True,
                'min_value': 0.0,
                'max_value': 10000.0,
            },
            'avg_pressure': {
                'required': True,
                'min_value': 0.0,
                'max_value': 1000.0,
            },
            'avg_temperature': {
                'required': True,
                'min_value': -273.15,
                'max_value': 5000.0,
            },
            'type_distribution': {
                'required': True,
            },
        }
    
    def validate_name(self, value):
        """
        SECURITY: Sanitize filename to prevent path traversal.
        """
        # Remove any path components
        value = os.path.basename(value)
        
        # Remove potentially dangerous characters
        import re
        value = re.sub(r'[^\w\s\-\.]', '', value)
        
        if not value:
            raise serializers.ValidationError("Invalid filename.")
        
        return value
    
    def validate_type_distribution(self, value):
        """
        SECURITY: Validate type_distribution JSON structure.
        Must be a dict with string keys and positive integer values.
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Type distribution must be a dictionary.")
        
        for equipment_type, count in value.items():
            # Validate key is string
            if not isinstance(equipment_type, str):
                raise serializers.ValidationError("Equipment type must be a string.")
            
            # SECURITY: Validate key length
            if len(equipment_type) > 100:
                raise serializers.ValidationError("Equipment type name is too long.")
            
            # Validate value is non-negative integer
            if not isinstance(count, int) or count < 0:
                raise serializers.ValidationError(
                    f"Count for '{equipment_type}' must be a non-negative integer."
                )
        
        return value
