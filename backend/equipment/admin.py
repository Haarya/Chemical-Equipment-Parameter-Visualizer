from django.contrib import admin
from .models import Dataset, Equipment


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """
    Admin interface for Dataset model.
    Displays key information and provides filtering/search capabilities.
    """
    list_display = ('name', 'uploaded_at', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature')
    list_filter = ('uploaded_at',)
    search_fields = ('name',)
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'uploaded_at', 'total_records')
        }),
        ('Statistics', {
            'fields': ('avg_flowrate', 'avg_pressure', 'avg_temperature', 'type_distribution')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual creation - datasets should be created via API"""
        return False


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Equipment model.
    Displays equipment details with filtering by dataset and type.
    """
    list_display = ('equipment_name', 'equipment_type', 'dataset', 'flowrate', 'pressure', 'temperature')
    list_filter = ('equipment_type', 'dataset')
    search_fields = ('equipment_name', 'equipment_type')
    ordering = ('equipment_name',)
    
    fieldsets = (
        ('Equipment Information', {
            'fields': ('dataset', 'equipment_name', 'equipment_type')
        }),
        ('Parameters', {
            'fields': ('flowrate', 'pressure', 'temperature')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual creation - equipment should be created via API"""
        return False
