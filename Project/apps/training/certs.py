import os
from datetime import datetime
from io import BytesIO
from django.conf import settings

from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, BalancedColumns

from apps.core.project_requirements.certs_mixin import styles


def itc_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        for i in qs.trainees.all():
            _extracted_from_itc_cert_19(flowables, i, qs)
    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    message_bit = f"1 {model_name} was" if rows == 1 else f"{rows} {model_name}s were"

    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


# TODO Rename this here and in `itc_cert`
def _extracted_from_itc_cert_19(flowables, i, qs):
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"KSA/qs/{i.unique_code}/{qs.pk}", styles['right']))
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"{i.name.upper()}", styles['name']))
    flowables.append(Spacer(0 * inch, 1 * inch))
    flowables.append(Paragraph(f"{qs.venue_name.upper()}", styles['centered']))
    flowables.append(Spacer(0 * inch, 0.3 * inch))
    flowables.append(Paragraph(f"{qs.start_date} {qs.end_date}", styles['centered']))

    flowables.append(PageBreak())


def ptc_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        for i in qs.trainees.all():
            _extracted_from_ptc_cert_19(flowables, i, qs)
    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    message_bit = f"1 {model_name} was" if rows == 1 else f"{rows} {model_name}s were"

    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


# TODO Rename this here and in `ptc_cert`
def _extracted_from_ptc_cert_19(flowables, i, qs):
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"KSA/qs/{i.unique_code}/{qs.pk}", styles['right']))
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"{i.name.upper()}", styles['name']))
    flowables.append(Spacer(0 * inch, 1 * inch))
    flowables.append(Paragraph(f"{qs.venue_name.upper()}", styles['centered']))
    flowables.append(Spacer(0 * inch, 0.3 * inch))
    flowables.append(Paragraph(f"{qs.start_date} {qs.end_date}", styles['centered']))

    flowables.append(PageBreak())


def wbii_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        for i in qs.trainees.all():
            _extracted_from_wbii_cert_19(flowables, i, qs)
    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    message_bit = f"1 {model_name} was" if rows == 1 else f"{rows} {model_name}s were"

    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


# TODO Rename this here and in `wbii_cert`
def _extracted_from_wbii_cert_19(flowables, i, qs):
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"KSA/WBII/{i.unique_code}/{qs.number}", styles['right']))

    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"{i.name.upper()}", styles['name']))
    flowables.append(Spacer(0 * inch, 1 * inch))
    flowables.append(Paragraph(f"{qs.venue_name.upper()}", styles['centered']))
    flowables.append(Spacer(0 * inch, 0.3 * inch))
    flowables.append(Paragraph(f"{qs.start_date} {qs.end_date}", styles['centered']))

    flowables.append(PageBreak())


def alt_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        for i in qs.trainees.all():
            _extracted_from_alt_cert_19(flowables, i, qs)
    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    message_bit = f"1 {model_name} was" if rows == 1 else f"{rows} {model_name}s were"

    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


# TODO Rename this here and in `alt_cert`
def _extracted_from_alt_cert_19(flowables, i, qs):
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"KSA/qs/{i.unique_code}/{qs.number}", styles['right']))
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"{i.name.upper()}", styles['name']))
    flowables.append(Spacer(0 * inch, 1 * inch))
    flowables.append(Paragraph(f"{qs.venue_name.upper()}", styles['centered']))
    flowables.append(Spacer(0 * inch, 0.3 * inch))
    flowables.append(Paragraph(f"{qs.start_date} {qs.end_date}", styles['centered']))
    flowables.append(PageBreak())


def lt_cert(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=1 * inch, leftMargin=1 * inch,
                               rightMargin=1 * inch, bottomMargin=1 * inch,
                               title=f"{model_name}s Certificates {date_str}.pdf")

    flowables = []
    for qs in queryset:
        for i in qs.trainees.all():
            _extracted_from_lt_cert_19(flowables, i, qs)
    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type=f"{model_name}s-{date_str}.pdf")
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    message_bit = f"1 {model_name} was" if rows == 1 else f"{rows} {model_name}s were"

    modeladmin.message_user(request, f"Certificates for {message_bit} successfully printed.")

    return response


# TODO Rename this here and in `lt_cert`
def _extracted_from_lt_cert_19(flowables, i, qs):
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"KSA/qs/{i.unique_code}/{qs.number}", styles['right']))
    flowables.append(Spacer(0 * inch, 1.5 * inch))
    flowables.append(Paragraph(f"{i.name.upper()}", styles['name']))
    flowables.append(Spacer(0 * inch, 1 * inch))
    flowables.append(Paragraph(f"{qs.venue_name.upper()}", styles['centered']))
    flowables.append(Spacer(0 * inch, 0.3 * inch))
    flowables.append(Paragraph(f"{qs.start_date} {qs.end_date}", styles['centered']))
    flowables.append(PageBreak())


def itc_report(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        title="%ss Report %s.pdf" % (model_name, date_str)
    )

    flowables = []
    logo = os.path.join(settings.BASE_DIR, 'static/img/favicon.png')
    image = Image('%s' % logo, width=50, height=50)
    image.hAlign = 'CENTER'

    for qs in queryset:
        flowables.append(image)
        flowables.append(Paragraph("<strong>The Kenya Scouts Association</strong>", styles['title1']))
        flowables.append(Paragraph("<u><i><b>%s</b></i></u> ITC Report" % qs.venue_name, styles['title2']))
        flowables.append(Paragraph("Held on: <b>%s</b> To <b>%s</b>" % (qs.start_date, qs.end_date), styles['title3']))
        flowables.append(Paragraph("Held in: <b>%s</b> County, <b>%s</b> SubCounty" %
                                   (qs.sub_county.county.name, qs.sub_county.name), styles['title3']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Course Director:</u>', styles['title3']))
        flowables.append(Paragraph("Name: <b>%s</b>" % qs.director.name, styles['myNormal']))
        flowables.append(Paragraph("Email: <b>%s</b>" % qs.director.email, styles['myNormal']))
        flowables.append(Paragraph("Phone Number:  <b>%s</b>" % qs.director.phone_number, styles['myNormal']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Support Staff:</u>', styles['title3']))
        for i, staff in enumerate(qs.staff.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), staff.name), styles['myNormal']),
                     Paragraph("%s" % staff.phone_number, styles['myNormal'])],
                    nCols=2))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Participants:</u>', styles['title3']))
        for i, participant in enumerate(qs.trainees.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), participant.name), styles['myNormal']),
                     Paragraph("%s" % participant.unique_code, styles['myNormal']),
                     Paragraph("%s" % participant.sub_county.name, styles['myNormal'])],
                    nCols=3, innerPadding=0.1, endSlack=0.1))
        flowables.append(PageBreak())

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type="%ss-%s.pdf" % (model_name, date_str))
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = "1 %s was" % model_name
    else:
        message_bit = "%s %ss were" % (rows, model_name)
    modeladmin.message_user(request, "Certificates for %s successfully printed." % message_bit)
    return response


def ptc_report(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        title="%ss Report %s.pdf" % (model_name, date_str)
    )

    flowables = []
    logo = os.path.join(settings.BASE_DIR, 'static/img/favicon.png')
    image = Image('%s' % logo, width=50, height=50)
    image.hAlign = 'CENTER'

    for qs in queryset:
        flowables.append(image)
        flowables.append(Paragraph("<strong>The Kenya Scouts Association</strong>", styles['title1']))
        flowables.append(Paragraph("<u><i><b>%s</b></i></u> PTC Report" % qs.venue_name, styles['title2']))
        flowables.append(Paragraph("Held on: <b>%s</b> To <b>%s</b>" % (qs.start_date, qs.end_date), styles['title3']))
        flowables.append(Paragraph("Held in: <b>%s</b> County, <b>%s</b> SubCounty" %
                                   (qs.sub_county.county.name, qs.sub_county.name), styles['title3']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Course Director:</u>', styles['title3']))
        flowables.append(Paragraph("Name: <b>%s</b>" % qs.director.name, styles['myNormal']))
        flowables.append(Paragraph("Email: <b>%s</b>" % qs.director.email, styles['myNormal']))
        flowables.append(Paragraph("Phone Number:  <b>%s</b>" % qs.director.phone_number, styles['myNormal']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Support Staff:</u>', styles['title3']))
        for i, staff in enumerate(qs.staff.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), staff.name), styles['myNormal']),
                     Paragraph("%s" % staff.phone_number, styles['myNormal'])],
                    nCols=2))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Participants:</u>', styles['title3']))
        for i, participant in enumerate(qs.trainees.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), participant.name), styles['myNormal']),
                     Paragraph("%s" % participant.unique_code, styles['myNormal']),
                     Paragraph("%s" % participant.sub_county.name, styles['myNormal'])],
                    nCols=3, innerPadding=0.1, endSlack=0.1))
        flowables.append(PageBreak())

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type="%ss-%s.pdf" % (model_name, date_str))
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = "1 %s was" % model_name
    else:
        message_bit = "%s %ss were" % (rows, model_name)
    modeladmin.message_user(request, "Certificates for %s successfully printed." % message_bit)
    return response


def wbii_report(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        title="%ss Report %s.pdf" % (model_name, date_str)
    )

    flowables = []
    logo = os.path.join(settings.BASE_DIR, 'static/img/favicon.png')
    image = Image('%s' % logo, width=50, height=50)
    image.hAlign = 'CENTER'

    for qs in queryset:
        flowables.append(image)
        flowables.append(Paragraph("<strong>The Kenya Scouts Association</strong>", styles['title1']))
        flowables.append(Paragraph("<u><i><b>%s</b></i></u> WoodBadge Report" % qs.venue_name, styles['title2']))
        flowables.append(Paragraph("Held on: <b>%s</b> To <b>%s</b>" % (qs.start_date, qs.end_date), styles['title3']))
        flowables.append(Paragraph("Held in: <b>%s</b> County" % qs.county.name, styles['title3']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Course Director:</u>', styles['title3']))
        flowables.append(Paragraph("Name: <b>%s</b>" % qs.director.name, styles['myNormal']))
        flowables.append(Paragraph("Email: <b>%s</b>" % qs.director.email, styles['myNormal']))
        flowables.append(Paragraph("Phone Number:  <b>%s</b>" % qs.director.phone_number, styles['myNormal']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Support Staff:</u>', styles['title3']))
        for i, staff in enumerate(qs.staff.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), staff.name), styles['myNormal']),
                     Paragraph("%s" % staff.phone_number, styles['myNormal'])],
                    nCols=2))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Participants:</u>', styles['title3']))
        for i, participant in enumerate(qs.trainees.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), participant.name), styles['myNormal']),
                     Paragraph("%s" % participant.unique_code, styles['myNormal']),
                     Paragraph("%s" % participant.sub_county.name, styles['myNormal'])],
                    nCols=3, innerPadding=0.1, endSlack=0.1))
        flowables.append(PageBreak())

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type="%ss-%s.pdf" % (model_name, date_str))
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = "1 %s was" % model_name
    else:
        message_bit = "%s %ss were" % (rows, model_name)
    modeladmin.message_user(request, "Certificates for %s successfully printed." % message_bit)
    return response


def alt_report(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        title="%ss Report %s.pdf" % (model_name, date_str)
    )

    flowables = []
    logo = os.path.join(settings.BASE_DIR, 'static/img/favicon.png')
    image = Image('%s' % logo, width=50, height=50)
    image.hAlign = 'CENTER'

    for qs in queryset:
        flowables.append(image)
        flowables.append(Paragraph("<strong>The Kenya Scouts Association</strong>", styles['title1']))
        flowables.append(Paragraph("<u><i><b>%s</b></i></u> ALT Report" % qs.venue_name, styles['title2']))
        flowables.append(Paragraph("Held on: <b>%s</b> To <b>%s</b>" % (qs.start_date, qs.end_date), styles['title3']))
        flowables.append(Paragraph("Held in: <b>%s</b> County" % qs.county.name, styles['title3']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Course Director:</u>', styles['title3']))
        flowables.append(Paragraph("Name: <b>%s</b>" % qs.director.name, styles['myNormal']))
        flowables.append(Paragraph("Email: <b>%s</b>" % qs.director.email, styles['myNormal']))
        flowables.append(Paragraph("Phone Number:  <b>%s</b>" % qs.director.phone_number, styles['myNormal']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Support Staff:</u>', styles['title3']))
        for i, staff in enumerate(qs.staff.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), staff.name), styles['myNormal']),
                     Paragraph("%s" % staff.phone_number, styles['myNormal'])],
                    nCols=2))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Participants:</u>', styles['title3']))
        for i, participant in enumerate(qs.trainees.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), participant.name), styles['myNormal']),
                     Paragraph("%s" % participant.unique_code, styles['myNormal']),
                     Paragraph("%s" % participant.sub_county.name, styles['myNormal'])],
                    nCols=3, innerPadding=0.1, endSlack=0.1))
        flowables.append(PageBreak())

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type="%ss-%s.pdf" % (model_name, date_str))
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = "1 %s was" % model_name
    else:
        message_bit = "%s %ss were" % (rows, model_name)
    modeladmin.message_user(request, "Certificates for %s successfully printed." % message_bit)
    return response


def lt_report(modeladmin, request, queryset):
    rows = len(queryset)
    model_name = modeladmin.model._meta.model_name.capitalize()
    date_str = datetime.now().strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    my_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        title="%ss Report %s.pdf" % (model_name, date_str)
    )

    flowables = []
    logo = os.path.join(settings.BASE_DIR, 'static/img/favicon.png')
    image = Image('%s' % logo, width=50, height=50)
    image.hAlign = 'CENTER'

    for qs in queryset:
        flowables.append(image)
        flowables.append(Paragraph("<strong>The Kenya Scouts Association</strong>", styles['title1']))
        flowables.append(Paragraph("<u><i><b>%s</b></i></u> LT Report" % qs.venue_name, styles['title2']))
        flowables.append(Paragraph("Held on: <b>%s</b> To <b>%s</b>" % (qs.start_date, qs.end_date), styles['title3']))
        flowables.append(Paragraph("Held in: <b>%s</b> County" % qs.county.name, styles['title3']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Course Director:</u>', styles['title3']))
        flowables.append(Paragraph("Name: <b>%s</b>" % qs.director.name, styles['myNormal']))
        flowables.append(Paragraph("Email: <b>%s</b>" % qs.director.email, styles['myNormal']))
        flowables.append(Paragraph("Phone Number:  <b>%s</b>" % qs.director.phone_number, styles['myNormal']))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Support Staff:</u>', styles['title3']))
        for i, staff in enumerate(qs.staff.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), staff.name), styles['myNormal']),
                     Paragraph("%s" % staff.phone_number, styles['myNormal'])],
                    nCols=2))
        flowables.append(Spacer(0 * inch, 0.3 * inch))
        flowables.append(Paragraph('<u>Participants:</u>', styles['title3']))
        for i, participant in enumerate(qs.trainees.all()):
            flowables.append(
                BalancedColumns(
                    [Paragraph("<b>%d.</b> %s" % ((i + 1), participant.name), styles['myNormal']),
                     Paragraph("%s" % participant.unique_code, styles['myNormal']),
                     Paragraph("%s" % participant.sub_county.name, styles['myNormal'])],
                    nCols=3, innerPadding=0.1, endSlack=0.1))
        flowables.append(PageBreak())

    my_doc.build(flowables)

    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type="%ss-%s.pdf" % (model_name, date_str))
    response['Content-Disposition'] = 'attachment; filename="%ss Certificates %s.pdf"' % (model_name, date_str)

    response.write(pdf_value)
    if rows == 1:
        message_bit = "1 %s was" % model_name
    else:
        message_bit = "%s %ss were" % (rows, model_name)
    modeladmin.message_user(request, "Certificates for %s successfully printed." % message_bit)
    return response


itc_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
ptc_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
wbii_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
alt_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
lt_cert.short_description = "Print Certificates for selected %(verbose_name_plural)s"
itc_report.short_description = "Print Reports for selected %(verbose_name_plural)s"
ptc_report.short_description = "Print Reports for selected %(verbose_name_plural)s"
wbii_report.short_description = "Print Reports for selected %(verbose_name_plural)s"
alt_report.short_description = "Print Reports for selected %(verbose_name_plural)s"
lt_report.short_description = "Print Reports for selected %(verbose_name_plural)s"
