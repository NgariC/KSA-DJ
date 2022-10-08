from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.rl_settings import defaultPageSize

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='first_centered', alignment=TA_CENTER, textColor=colors.green, fontSize=18))
styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, textColor=colors.green))
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


def print_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        unit_name = Paragraph(f"{qs.name}", styles['first_centered'])
        unit_warrant_date = Paragraph(f"{qs.date_warranted}", styles['centered'])
        unit_code = Paragraph(f"{qs.code}", styles['centered'])

        flowables.extend((Spacer(4 * inch, 4 * inch), unit_name, Spacer(0, 0),
                          Paragraph("<br></br><br></br>", styles['Normal']),
                          unit_warrant_date, Paragraph("<br></br><br></br>", styles['Normal']),
                          unit_code, PageBreak()))

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = f"1 {model_name} was"
    else:
        message_bit = f"{rows} {model_name}s were"
    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


def print_warrant(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    pdf_buffer = BytesIO()
    date_str = datetime.now().strftime('%Y-%m-%d')
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Warrants {date_str}.pdf")

    flowables = []

    for qs in queryset:
        unit_name = Paragraph(f"{qs.name}", styles['first_centered'])
        unit_warrant_date = Paragraph(f"{qs.date_warranted}", styles['centered'])
        unit_code = Paragraph(f"{qs.code}", styles['centered'])

        flowables.extend((Spacer(4 * inch, 4 * inch), unit_name, Spacer(0, 0),
                          Paragraph("<br></br><br></br>", styles['Normal']), unit_warrant_date,
                          Paragraph("<br></br><br></br>", styles['Normal']), unit_code))

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Warrants %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = f"1 {model_name} was"
    else:
        message_bit = f"{rows} {model_name}s were"
    modeladmin.message_user(request, f"Warrants for {message_bit} successfully printed.")

    return response


print_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
print_warrant.short_description = "Print Warrants for selected %(verbose_name_plural)s"
