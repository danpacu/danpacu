import os
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def export_calendar(calendar_data, file_format, period='day', date=None):
    """
    Exporta la vista de los eventos del calendario a un archivo PDF o ODT.

    :param calendar_data: Diccionario con los eventos del calendario
    :type calendar_data: dict
    :param file_format: Formato de archivo a exportar (PDF o ODT)
    :type file_format: str
    :param period: Periodo de tiempo de los eventos a exportar (day, week o month), por defecto day
    :type period: str
    :param date: Fecha de inicio del periodo a exportar, por defecto None (hoy)
    :type date: str
    :return: Nombre del archivo exportado
    :rtype: str
    """

    # Selecciona los eventos a exportar según el periodo especificado
    if period == 'day':
        if not date:
            date = datetime.now().date()
        events = [calendar_data[date]]
    elif period == 'week':
        if not date:
            date = datetime.now().date()
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
        events = [calendar_data[d] for d in calendar_data if start_date <= d <= end_date]
    elif period == 'month':
        if not date:
            date = datetime.now().date()
        month = date.month
        year = date.year
        _, num_days = calendar.monthrange(year, month)
        start_date = date.replace(day=1)
        end_date = date.replace(day=num_days)
        events = [calendar_data[d] for d in calendar_data if start_date <= d <= end_date]
    else:
        raise ValueError('Periodo de tiempo no válido.')

    # Prepara la tabla con los eventos a exportar
    data = []
    for event in events:
        row = [event['date'], event['time'], event['name'], event['location']]
        if 'link' in event:
            row.append(event['link'])
        data.append(row)

    # Crea el archivo PDF o ODT
    if file_format == 'pdf':
        filename = f"calendar_{period}_{date.strftime('%Y-%m-%d')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('ALIGN', (0,1), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('BOTTOMPADDING', (0,1), (-1,-1), 10),
            ('BACKGROUND', (0,-1), (-1,-1), colors.grey),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.whitesmoke),
            ('ALIGN', (0,-1), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,-1), (-1,-1), 14),('TOPPADDING', (0,-1), (-1,-1), 12),
            ])


    # Add title
    elements.append(Paragraph(f'<strong>{title}</strong>', styles['Heading1']))
    elements.append(Spacer(1, 20))

    # Add table
    data = [[Paragraph("<strong>Date</strong>", styles['Normal']),
            Paragraph("<strong>Event</strong>", styles['Normal']),
            Paragraph("<strong>Time</strong>", styles['Normal']),
            Paragraph("<strong>Location</strong>", styles['Normal']),
            Paragraph("<strong>Link</strong>", styles['Normal'])]]
    
    for event in events:
        date = event['date'].strftime('%d-%m-%Y')
        event_name = event['name']
        time = event['time']
        location = event['location']
        link = event['link']
        if link:
            link = f'<a href="{link}">{link}</a>'
        data.append([Paragraph(date, styles['Normal']),
                    Paragraph(event_name, styles['Normal']),
                    Paragraph(time, styles['Normal']),
                    Paragraph(location, styles['Normal']),
                    Paragraph(link, styles['Normal'])])
    
    table = Table(data, colWidths=[doc.width/5]*5)
    table.setStyle(style)
    elements.append(table)

elif file_format == 'odt':
    filename = f"calendar_{period}_{date.strftime('%Y-%m-%d')}.odt"
    doc = OpenDocumentText()
    table = doc.add_table(len(events)+1, 5)
    for i in range(5):
        cell = table.cell(0, i)
        if i == 0:
            cell.text = "Date"
        elif i == 1:
            cell.text = "Event"
        elif i == 2:
            cell.text = "Time"
        elif i == 3:
            cell.text = "Location"
        elif i == 4:
            cell.text = "Link"
    
    for i, event in enumerate(events):
        date = event['date'].strftime('%d-%m-%Y')
        event_name = event['name']
        time = event['time']
        location = event['location']
        link = event['link']
        if link:
            link = f'<a href="{link}">{link}</a>'
        row = table.row(i+1)
        row.cells[0].text = date
        row.cells[1].text = event_name
        row.cells[2].text = time
        row.cells[3].text = location
        row.cells[4].text = link

    doc.save(filename)

return filename
