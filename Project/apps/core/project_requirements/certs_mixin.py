from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='right', alignment=TA_RIGHT, textColor=colors.green))
styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER, textColor=colors.green, fontSize=14))
styles.add(ParagraphStyle(name='name', alignment=TA_CENTER, textColor=colors.green, fontSize=20))
styles.add(ParagraphStyle(name='title1', alignment=TA_CENTER, textColor=colors.green, fontSize=18, spaceAfter=30))
styles.add(ParagraphStyle(name='title2', alignment=TA_LEFT, fontSize=16, spaceAfter=24))
styles.add(ParagraphStyle(name='title3', alignment=TA_LEFT, fontSize=16, spaceAfter=15))
styles.add(ParagraphStyle(name='myNormal', alignment=TA_LEFT, fontSize=10, spaceAfter=5))
