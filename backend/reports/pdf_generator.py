"""
PDF Report Generator for Chemical Equipment Data.

Uses ReportLab to generate professional PDF reports with:
- Header with title and date
- Summary statistics section
- Equipment type distribution table
- Complete data table with all equipment
- Optional chart embedding
"""

import io
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class PDFReportGenerator:
    """
    Generate PDF reports for chemical equipment datasets.
    """
    
    def __init__(self, pagesize=letter):
        """
        Initialize PDF generator.
        
        Args:
            pagesize: Page size (letter or A4)
        """
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles for the report."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4a90e2'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20
        )
    
    def _create_header(self, dataset_info: Dict[str, Any]) -> List:
        """
        Create report header with title and dataset information.
        
        Args:
            dataset_info: Dictionary with dataset details
            
        Returns:
            List of reportlab elements
        """
        elements = []
        
        # Title
        title = Paragraph("Chemical Equipment Parameter Report", self.title_style)
        elements.append(title)
        
        # Report generation date
        date_text = f"<i>Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</i>"
        date_para = Paragraph(date_text, ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        elements.append(date_para)
        
        # Horizontal line
        elements.append(Spacer(1, 0.1*inch))
        
        # Dataset information
        info_text = f"<b>Dataset Name:</b> {dataset_info.get('name', 'N/A')}<br/>"
        info_text += f"<b>Upload Date:</b> {dataset_info.get('upload_date', 'N/A')}<br/>"
        info_text += f"<b>Total Records:</b> {dataset_info.get('total_records', 0)}<br/>"
        info_text += f"<b>Dataset ID:</b> {dataset_info.get('id', 'N/A')}"
        
        info_para = Paragraph(info_text, self.info_style)
        elements.append(info_para)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_summary_section(self, summary_stats: Dict[str, float]) -> List:
        """
        Create summary statistics section.
        
        Args:
            summary_stats: Dictionary with avg_flowrate, avg_pressure, avg_temperature
            
        Returns:
            List of reportlab elements
        """
        elements = []
        
        # Section heading
        heading = Paragraph("Summary Statistics", self.heading_style)
        elements.append(heading)
        
        # Summary data table
        summary_data = [
            ['Metric', 'Value', 'Unit'],
            ['Average Flowrate', f"{summary_stats.get('avg_flowrate', 0):.2f}", 'm³/h'],
            ['Average Pressure', f"{summary_stats.get('avg_pressure', 0):.2f}", 'bar'],
            ['Average Temperature', f"{summary_stats.get('avg_temperature', 0):.2f}", '°C'],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.2*inch])
        summary_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.beige])
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_type_distribution_section(
        self, 
        type_distribution: Dict[str, int],
        total_records: int
    ) -> List:
        """
        Create equipment type distribution section.
        
        Args:
            type_distribution: Dictionary mapping equipment type to count
            total_records: Total number of equipment records
            
        Returns:
            List of reportlab elements
        """
        elements = []
        
        # Section heading
        heading = Paragraph("Equipment Type Distribution", self.heading_style)
        elements.append(heading)
        
        # Type distribution table
        type_data = [['Equipment Type', 'Count', 'Percentage']]
        
        # Sort by count descending
        sorted_types = sorted(
            type_distribution.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for equip_type, count in sorted_types:
            percentage = (count / total_records * 100) if total_records > 0 else 0
            type_data.append([
                equip_type,
                str(count),
                f"{percentage:.1f}%"
            ])
        
        type_table = Table(type_data, colWidths=[2.8*inch, 1.2*inch, 1.2*inch])
        type_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(type_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_data_table_section(
        self, 
        equipment_data: List[Dict[str, Any]],
        max_rows: int = 50
    ) -> List:
        """
        Create equipment data table section.
        
        Args:
            equipment_data: List of equipment dictionaries
            max_rows: Maximum number of rows to include
            
        Returns:
            List of reportlab elements
        """
        elements = []
        
        # Section heading
        heading = Paragraph("Equipment Data", self.heading_style)
        elements.append(heading)
        
        if not equipment_data:
            no_data_para = Paragraph(
                "<i>No equipment data available</i>",
                self.styles['Normal']
            )
            elements.append(no_data_para)
            return elements
        
        # Prepare equipment data for table
        table_data = [['Equipment Name', 'Type', 'Flowrate\n(m³/h)', 'Pressure\n(bar)', 'Temp\n(°C)']]
        
        # Limit rows for PDF size
        limited_data = equipment_data[:max_rows]
        
        for equipment in limited_data:
            table_data.append([
                equipment.get('equipment_name', 'N/A')[:20],  # Truncate long names
                equipment.get('equipment_type', 'N/A')[:15],
                f"{equipment.get('flowrate', 0):.1f}",
                f"{equipment.get('pressure', 0):.1f}",
                f"{equipment.get('temperature', 0):.1f}"
            ])
        
        # Add note if data was truncated
        if len(equipment_data) > max_rows:
            truncated_count = len(equipment_data) - max_rows
            table_data.append([
                f"... {truncated_count} more records omitted",
                '', '', '', ''
            ])
        
        equipment_table = Table(
            table_data,
            colWidths=[1.5*inch, 1.3*inch, 1*inch, 1*inch, 0.8*inch]
        )
        equipment_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            # Data rows styling
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(equipment_table)
        
        return elements
    
    def _add_chart_image(
        self,
        elements: List,
        chart_path: Optional[str] = None,
        chart_buffer: Optional[io.BytesIO] = None,
        width: float = 5*inch,
        height: float = 3*inch
    ):
        """
        Add chart image to PDF (optional).
        
        Args:
            elements: List of reportlab elements to append to
            chart_path: Path to chart image file
            chart_buffer: BytesIO buffer containing chart image
            width: Image width
            height: Image height
        """
        if chart_path or chart_buffer:
            heading = Paragraph("Equipment Parameter Chart", self.heading_style)
            elements.append(heading)
            
            try:
                if chart_buffer:
                    # Create image from buffer
                    img = Image(chart_buffer, width=width, height=height)
                elif chart_path:
                    # Create image from file path
                    img = Image(chart_path, width=width, height=height)
                else:
                    return
                
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                # If image loading fails, add error note
                error_para = Paragraph(
                    f"<i>Chart could not be loaded: {str(e)}</i>",
                    self.styles['Normal']
                )
                elements.append(error_para)
    
    def generate_report(
        self,
        dataset_info: Dict[str, Any],
        summary_stats: Dict[str, float],
        type_distribution: Dict[str, int],
        equipment_data: List[Dict[str, Any]],
        chart_path: Optional[str] = None,
        chart_buffer: Optional[io.BytesIO] = None,
        include_chart: bool = False
    ) -> io.BytesIO:
        """
        Generate complete PDF report.
        
        Args:
            dataset_info: Dataset metadata (name, id, upload_date, total_records)
            summary_stats: Summary statistics (avg_flowrate, avg_pressure, avg_temperature)
            type_distribution: Equipment type distribution dict
            equipment_data: List of equipment dictionaries
            chart_path: Optional path to chart image file
            chart_buffer: Optional BytesIO buffer with chart image
            include_chart: Whether to include chart in report
            
        Returns:
            BytesIO buffer containing PDF content
        """
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.pagesize,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        # Build report elements
        elements = []
        
        # 1. Header with title and dataset info
        elements.extend(self._create_header(dataset_info))
        
        # 2. Summary statistics section
        elements.extend(self._create_summary_section(summary_stats))
        
        # 3. Equipment type distribution section
        elements.extend(self._create_type_distribution_section(
            type_distribution,
            dataset_info.get('total_records', 0)
        ))
        
        # 4. Optional chart
        if include_chart:
            self._add_chart_image(elements, chart_path, chart_buffer)
        
        # 5. Equipment data table
        elements.extend(self._create_data_table_section(equipment_data))
        
        # Footer text
        elements.append(Spacer(1, 0.3*inch))
        footer_text = "<i>End of Report</i>"
        footer_para = Paragraph(
            footer_text,
            ParagraphStyle(
                'FooterStyle',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        )
        elements.append(footer_para)
        
        # Build PDF
        doc.build(elements)
        
        # Reset buffer position
        buffer.seek(0)
        
        return buffer
