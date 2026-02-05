from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """
    Model to store dataset metadata and summary statistics.
    Automatically enforces keeping only the last 5 uploaded datasets per user.
    
    SECURITY: Input validation on all fields with appropriate constraints.
    """
    # User who uploaded this dataset
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='datasets',
        help_text="User who uploaded this dataset"
    )
    
    # SECURITY: Filename validation - max length 255 chars
    name = models.CharField(
        max_length=255,
        help_text="Original CSV filename"
    )
    
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when dataset was uploaded"
    )
    
    # SECURITY: Validate record count is positive and reasonable
    total_records = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Dataset must have at least 1 record"),
            MaxValueValidator(10000, message="Dataset exceeds maximum allowed rows")
        ],
        help_text="Total number of equipment records in this dataset"
    )
    
    # SECURITY: Validate numeric fields are non-negative and within reasonable ranges
    avg_flowrate = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Flowrate cannot be negative"),
            MaxValueValidator(10000.0, message="Flowrate value is unrealistic")
        ],
        help_text="Average flowrate (m³/h)"
    )
    
    avg_pressure = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Pressure cannot be negative"),
            MaxValueValidator(1000.0, message="Pressure value is unrealistic")
        ],
        help_text="Average pressure (bar)"
    )
    
    avg_temperature = models.FloatField(
        validators=[
            MinValueValidator(-273.15, message="Temperature below absolute zero"),
            MaxValueValidator(5000.0, message="Temperature value is unrealistic")
        ],
        help_text="Average temperature (°C)"
    )
    
    # SECURITY: JSONField for type distribution - will validate JSON structure in save()
    type_distribution = models.JSONField(
        default=dict,
        help_text="Dictionary storing count of each equipment type"
    )
    
    class Meta:
        ordering = ['-uploaded_at']  # Most recent first
        verbose_name = "Dataset"
        verbose_name_plural = "Datasets"
    
    def __str__(self):
        return f"{self.name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    def clean(self):
        """
        SECURITY: Custom validation for model fields.
        Validates type_distribution JSON structure.
        """
        super().clean()
        
        # Validate type_distribution is a dict with non-negative integers
        if not isinstance(self.type_distribution, dict):
            raise ValidationError({
                'type_distribution': 'Must be a dictionary'
            })
        
        for equipment_type, count in self.type_distribution.items():
            # SECURITY: Validate equipment type name
            if not isinstance(equipment_type, str) or len(equipment_type) > 100:
                raise ValidationError({
                    'type_distribution': f'Invalid equipment type: {equipment_type}'
                })
            
            # SECURITY: Validate count is non-negative integer
            if not isinstance(count, int) or count < 0:
                raise ValidationError({
                    'type_distribution': f'Invalid count for {equipment_type}: must be non-negative integer'
                })
    
    def save(self, *args, **kwargs):
        """
        Override save to enforce keeping only last 5 datasets per user.
        Automatically deletes oldest datasets when limit is exceeded.
        """
        # Run validation
        self.full_clean()
        
        # Save the current dataset
        super().save(*args, **kwargs)
        
        # Enforce maximum 5 datasets rule per user
        self.enforce_dataset_limit(user=self.user)
    
    @classmethod
    def enforce_dataset_limit(cls, user, max_datasets=5):
        """
        BUSINESS LOGIC: Keep only the last 5 uploaded datasets per user.
        Deletes oldest datasets when limit is exceeded.
        
        Args:
            user: The user whose datasets to check
            max_datasets (int): Maximum number of datasets to keep (default: 5)
        """
        total_count = cls.objects.filter(user=user).count()
        
        if total_count > max_datasets:
            # Get datasets to delete (oldest ones for this user)
            excess_count = total_count - max_datasets
            datasets_to_delete = cls.objects.filter(user=user).order_by('uploaded_at')[:excess_count]
            
            # Delete excess datasets (cascade will delete related Equipment records)
            for dataset in datasets_to_delete:
                dataset.delete()


class Equipment(models.Model):
    """
    Model to store individual equipment data from CSV files.
    Each equipment record belongs to a Dataset.
    
    SECURITY: Input validation on all fields with appropriate constraints.
    """
    # ForeignKey with CASCADE delete - when Dataset is deleted, all Equipment records are deleted
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='equipment_records',
        help_text="Parent dataset this equipment belongs to"
    )
    
    # SECURITY: Equipment name validation - max length and no special characters
    equipment_name = models.CharField(
        max_length=100,
        help_text="Equipment identifier (e.g., P-101, R-201)"
    )
    
    # SECURITY: Equipment type validation - max length
    equipment_type = models.CharField(
        max_length=50,
        help_text="Type of equipment (e.g., Pump, Reactor, Heat Exchanger)"
    )
    
    # SECURITY: Validate numeric fields are non-negative and within reasonable ranges
    flowrate = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Flowrate cannot be negative"),
            MaxValueValidator(10000.0, message="Flowrate value is unrealistic")
        ],
        help_text="Flowrate in m³/h"
    )
    
    pressure = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Pressure cannot be negative"),
            MaxValueValidator(1000.0, message="Pressure value is unrealistic")
        ],
        help_text="Pressure in bar"
    )
    
    temperature = models.FloatField(
        validators=[
            MinValueValidator(-273.15, message="Temperature below absolute zero"),
            MaxValueValidator(5000.0, message="Temperature value is unrealistic")
        ],
        help_text="Temperature in °C"
    )
    
    class Meta:
        ordering = ['equipment_name']
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        # Add index for faster queries
        indexes = [
            models.Index(fields=['dataset', 'equipment_type']),
            models.Index(fields=['equipment_name']),
        ]
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
    
    def clean(self):
        """
        SECURITY: Custom validation for equipment fields.
        """
        super().clean()
        
        # Validate equipment_name contains only allowed characters
        import re
        if not re.match(r'^[A-Za-z0-9\-_]+$', self.equipment_name):
            raise ValidationError({
                'equipment_name': 'Equipment name can only contain letters, numbers, hyphens, and underscores'
            })
        
        # Validate equipment_type contains only letters, spaces, and hyphens
        if not re.match(r'^[A-Za-z\s\-]+$', self.equipment_type):
            raise ValidationError({
                'equipment_type': 'Equipment type can only contain letters, spaces, and hyphens'
            })
    
    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)
