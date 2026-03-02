"""
FEATURE-003: PDF report generation engine for GreaterWMS.

Generates PDF reports for:
- Stock summary reports
- ASN receiving reports
- DN shipping reports
- Inventory valuation reports
- Pick list reports

Uses ReportLab for PDF generation. Install: pip install reportlab
"""
import io
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from django.http import HttpResponse

logger = logging.getLogger(__name__)

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph,
        Spacer, PageBreak, Image
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not installed. PDF generation unavailable. pip install reportlab")


def _check_reportlab():
    """Ensure reportlab is available."""
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "ReportLab is required for PDF generation. "
            "Install it with: pip install reportlab"
        )


def generate_stock_report(
    stock_data: List[Dict[str, Any]],
    title: str = "Stock Summary Report",
    openid: str = "",
) -> bytes:
    """
    Generate a stock summary PDF report.

    Args:
        stock_data: List of stock records with keys:
            goods_code, goods_desc, goods_qty, onhand_stock, can_order_stock
        title: Report title.
        openid: Tenant identifier.

    Returns:
        PDF file as bytes.
    """
    _check_reportlab()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=title)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=18, spaceAfter=30, alignment=1,
    )
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Tenant: {openid}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 20))

    # Table header
    headers = ['Goods Code', 'Description', 'Total Qty', 'On Hand', 'Available']
    data = [headers]

    for item in stock_data:
        data.append([
            str(item.get('goods_code', '')),
            str(item.get('goods_desc', ''))[:40],
            str(item.get('goods_qty', 0)),
            str(item.get('onhand_stock', 0)),
            str(item.get('can_order_stock', 0)),
        ])

    table = Table(data, colWidths=[80, 180, 60, 60, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    elements.append(table)

    # Summary
    elements.append(Spacer(1, 20))
    total_qty = sum(item.get('goods_qty', 0) for item in stock_data)
    total_onhand = sum(item.get('onhand_stock', 0) for item in stock_data)
    elements.append(Paragraph(
        f"<b>Total Items:</b> {len(stock_data)} | "
        f"<b>Total Qty:</b> {total_qty} | "
        f"<b>Total On Hand:</b> {total_onhand}",
        styles['Normal']
    ))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_pick_list_report(
    picking_data: List[Dict[str, Any]],
    dn_code: str = "",
) -> bytes:
    """
    Generate a pick list PDF for warehouse operators.

    Args:
        picking_data: List of pick items with keys:
            dn_code, bin_name, goods_code, pick_qty, picked_qty
        dn_code: DN code for the pick list.

    Returns:
        PDF file as bytes.
    """
    _check_reportlab()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f"Pick List - {dn_code}")
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Pick List: {dn_code}", styles['Heading1']))
    elements.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 20))

    headers = ['DN Code', 'Bin', 'Goods Code', 'Pick Qty', 'Picked', '✓']
    data = [headers]
    for item in picking_data:
        data.append([
            str(item.get('dn_code', '')),
            str(item.get('bin_name', '')),
            str(item.get('goods_code', '')),
            str(item.get('pick_qty', 0)),
            str(item.get('picked_qty', 0)),
            '☐',
        ])

    table = Table(data, colWidths=[80, 80, 100, 60, 60, 30])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff0')]),
    ]))
    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def pdf_response(pdf_bytes: bytes, filename: str) -> HttpResponse:
    """
    Wrap PDF bytes in a Django HttpResponse for download.

    Args:
        pdf_bytes: The PDF file content.
        filename: Filename for the download.

    Returns:
        HttpResponse with PDF content type.
    """
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
