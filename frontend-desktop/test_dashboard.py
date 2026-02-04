"""
Test Dashboard Tab
Demonstrates all dashboard features with sample data
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.dashboard_tab import DashboardTab
from services.api_service import APIService


class MockAPIService:
    """Mock API service for testing"""
    
    def __init__(self):
        self.token = "test_token"
    
    def set_token(self, token):
        self.token = token
    
    def get_datasets(self):
        """Return sample datasets list"""
        return [
            {
                'id': 1,
                'name': 'sample_equipment_data.csv',
                'total_records': 30,
                'uploaded_at': '2026-02-04T10:30:00'
            },
            {
                'id': 2,
                'name': 'test_parameters.csv',
                'total_records': 15,
                'uploaded_at': '2026-02-03T14:20:00'
            }
        ]
    
    def get_dataset_detail(self, dataset_id):
        """Return sample dataset detail"""
        if dataset_id == 1:
            return {
                'id': 1,
                'name': 'sample_equipment_data.csv',
                'total_records': 30,
                'avg_flowrate': 156.33,
                'avg_pressure': 25.67,
                'avg_temperature': 185.42,
                'uploaded_at': '2026-02-04T10:30:00',
                'type_distribution': {
                    'Pump': 8,
                    'Heat Exchanger': 7,
                    'Reactor': 6,
                    'Compressor': 5,
                    'Valve': 4
                },
                'equipment_records': [
                    {
                        'equipment_name': f'Equipment-{i+1}',
                        'equipment_type': ['Pump', 'Heat Exchanger', 'Reactor', 'Compressor', 'Valve'][i % 5],
                        'flowrate': 100 + i * 10,
                        'pressure': 20 + i * 2,
                        'temperature': 150 + i * 5
                    }
                    for i in range(30)
                ]
            }
        else:
            return {
                'id': 2,
                'name': 'test_parameters.csv',
                'total_records': 15,
                'avg_flowrate': 142.50,
                'avg_pressure': 22.30,
                'avg_temperature': 175.80,
                'uploaded_at': '2026-02-03T14:20:00',
                'type_distribution': {
                    'Pump': 5,
                    'Heat Exchanger': 4,
                    'Reactor': 3,
                    'Valve': 3
                },
                'equipment_records': [
                    {
                        'equipment_name': f'Test-Equipment-{i+1}',
                        'equipment_type': ['Pump', 'Heat Exchanger', 'Reactor', 'Valve'][i % 4],
                        'flowrate': 120 + i * 5,
                        'pressure': 18 + i * 1.5,
                        'temperature': 160 + i * 4
                    }
                    for i in range(15)
                ]
            }
    
    def download_pdf_report(self, dataset_id, file_path):
        """Mock PDF download"""
        # Create a dummy PDF file
        with open(file_path, 'w') as f:
            f.write(f"Mock PDF Report for Dataset {dataset_id}\n")
        return True


def main():
    app = QApplication(sys.argv)
    
    # Create mock API service
    api_service = MockAPIService()
    
    # Create dashboard
    dashboard = DashboardTab(api_service)
    dashboard.setWindowTitle("Dashboard Tab Test - Chemical Equipment Visualizer")
    dashboard.resize(1400, 900)
    
    # Load datasets list
    dashboard.load_datasets_list()
    
    # Show window
    dashboard.show()
    
    print("\n===== Dashboard Tab Test =====")
    print("\nInstructions:")
    print("1. Select a dataset from the dropdown at the top")
    print("2. View summary cards with key metrics")
    print("3. Explore the three charts:")
    print("   - Pie chart: Equipment type distribution")
    print("   - Bar chart: Average parameter comparison")
    print("   - Line chart: Parameter trends (change parameter and type)")
    print("4. Browse equipment data in the table at the bottom")
    print("5. Use the search box to filter table data")
    print("6. Click 'Refresh' to reload current dataset")
    print("7. Click 'Download PDF' to save a report (mock)")
    print("\nThe dashboard demonstrates all visualization components working together!")
    print("===============================\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
