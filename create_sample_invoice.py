# create_sample_invoice.py
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def create_sample_invoice():
    """Generate a realistic sample invoice PDF"""
    
    # Create PDF
    doc = SimpleDocTemplate("sample_invoice.pdf", pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30
    )
    
    # Company header
    elements.append(Paragraph("TECH SOLUTIONS INC.", title_style))
    elements.append(Paragraph("123 Business Street, Tech City, TC 12345", styles['Normal']))
    elements.append(Paragraph("Phone: (555) 123-4567 | Email: billing@techsolutions.com", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice details
    elements.append(Paragraph("<b>INVOICE</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice info table
    invoice_info = [
        ['Invoice #:', 'INV-2025-001234'],
        ['Date:', '03/02/2025'],
        ['Due Date:', '04/01/2025'],
        ['Customer:', 'Sameer Ahmed'],
    ]
    
    info_table = Table(invoice_info, colWidths=[1.5*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Bill to section
    elements.append(Paragraph("<b>Bill To:</b>", styles['Heading3']))
    elements.append(Paragraph("Sameer Ahmed", styles['Normal']))
    elements.append(Paragraph("456 Customer Lane", styles['Normal']))
    elements.append(Paragraph("London, UK", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Line items table
    elements.append(Paragraph("<b>Items:</b>", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    
    items_data = [
        ['Item', 'Description', 'Qty', 'Unit Price', 'Amount'],
        ['Web Development', 'Custom website design and development', '1', '$2,500.00', '$2,500.00'],
        ['API Integration', 'Third-party API setup and testing', '3', '$450.00', '$1,350.00'],
        ['Database Setup', 'PostgreSQL database configuration', '1', '$800.00', '$800.00'],
        ['Hosting (1 year)', 'Cloud hosting and maintenance', '12', '$50.00', '$600.00'],
        ['SSL Certificate', 'Premium SSL certificate', '1', '$150.00', '$150.00'],
    ]
    
    items_table = Table(items_data, colWidths=[1.5*inch, 2.5*inch, 0.5*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        
        # Data rows styling
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#ECF0F1')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totals section
    totals_data = [
        ['', '', '', 'Subtotal:', '$5,400.00'],
        ['', '', '', 'Tax (10%):', '$540.00'],
        ['', '', '', 'Discount:', '-$100.00'],
        ['', '', '', 'Total:', '$5,840.00'],
    ]
    
    totals_table = Table(totals_data, colWidths=[1.5*inch, 2.5*inch, 0.5*inch, 1*inch, 1*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (3,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (3,0), (-1,-1), 10),
        ('LINEABOVE', (3,0), (-1,0), 0.5, colors.grey),
        ('LINEABOVE', (3,-1), (-1,-1), 1.5, colors.black),
        ('TOPPADDING', (3,0), (-1,-1), 6),
        ('BOTTOMPADDING', (3,0), (-1,-1), 6),
        # Make final total larger
        ('FONTSIZE', (3,-1), (-1,-1), 12),
        ('TEXTCOLOR', (3,-1), (-1,-1), colors.HexColor('#27AE60')),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Payment info
    elements.append(Paragraph("<b>Payment Information:</b>", styles['Heading3']))
    elements.append(Paragraph("Bank: Tech Bank International", styles['Normal']))
    elements.append(Paragraph("Account: 1234-5678-9012", styles['Normal']))
    elements.append(Paragraph("Routing: 987654321", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(Paragraph("<i>Thank you for your business!</i>", styles['Normal']))
    elements.append(Paragraph("<i>Payment due within 30 days. Late payments subject to 1.5% monthly fee.</i>", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print("✅ Created sample_invoice.pdf")

if __name__ == "__main__":
    create_sample_invoice()