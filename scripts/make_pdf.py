from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import datetime, hashlib

# Calculate Hash of current state
with open('make_pdf.py', 'rb') as f: hash_val = hashlib.sha256(f.read()).hexdigest()[:16]
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

doc = SimpleDocTemplate("NomaanOS_Project_Explanation.pdf", pagesize=A4)
style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10)
content = [Paragraph(f"<b>DOCUMENT INTEGRITY PROOF</b><br/>Timestamp: {timestamp}<br/>Digital Hash: {hash_val}", style)]

doc.build(content)
print(f"✅ PDF Generated with Watermark: {hash_val}")
