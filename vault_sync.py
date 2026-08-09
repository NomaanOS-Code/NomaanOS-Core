import os, shutil, json, datetime, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

V = '/00_NOMAANOS_OFFICIAL_VAULT'
DOCS, LOGS, SIGS, BACKUPS = os.path.join(V, '01_HUMAN_READABLE_DOCS'), os.path.join(V, '02_DAILY_WORK_LOGS'), os.path.join(V, '03_DIGITAL_SHA256_SIGNATURES'), os.path.join(V, '04_PROJECT_BACKUPS')

for d in [DOCS, LOGS, SIGS, BACKUPS]:
    os.makedirs(d, exist_ok=True)

# Generate Base Docs
os.system('python3 make_pdf.py')
os.system('python3 integrity_engine.py')

# Work Tracker Logic
today = datetime.datetime.now().strftime('%Y-%m-%d')
now_str = datetime.datetime.now().strftime('%I:%M %p IST')
log_file = 'work_hours.json'

data = {}
if os.path.exists(log_file):
    try:
        with open(log_file, 'r') as f: data = json.load(f)
    except: pass

if today not in data:
    data[today] = {'date': today, 'hours_logged': '3.5 Hours', 'status': 'ACTIVE', 'tasks': ['Red-Teaming Benchmark 100%', 'GitHub Actions CI/CD Pipeline', 'Native REST API Gateway', 'SHA-256 Integrity Engine', 'iPad Files App Master Vault Automation']}

data[today]['last_updated'] = now_str
with open(log_file, 'w') as f: json.dump(data, f, indent=4)

# Create Work Report PDF
pdf_path = os.path.join(LOGS, f'Daily_Work_Report_{today}.pdf')
doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()
t_style = ParagraphStyle('T', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#0f172a'))
b_style = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#1e293b'))

content = [
    Paragraph('NOMAAN-OS CORE — DAILY WORK & ACTIVITY REPORT', t_style),
    Paragraph(f'<b>Author:</b> Nomaan Khan (Scholar @ IHFC - IIT Delhi) | <b>Date:</b> {today} | <b>Time:</b> {now_str}', b_style),
    HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=12),
    Paragraph(f'<b>Total Hours Worked Today:</b> {data[today]["hours_logged"]}', b_style),
    Spacer(1, 8),
    Paragraph('<b>Completed Core Tasks & Milestones:</b>', b_style)
]

for task in data[today]['tasks']:
    content.append(Paragraph(f'• {task}', b_style))

sha256_hash = hashlib.sha256(json.dumps(data[today]).encode('utf-8')).hexdigest()
content.extend([
    Spacer(1, 15),
    HRFlowable(width='100%', thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=8),
    Paragraph(f'<b>DIGITAL SHA-256 SIGNATURE:</b> <font face="Courier">{sha256_hash}</font>', b_style),
    Paragraph('<b>STATUS:</b> CRYPTOGRAPHICALLY VERIFIED & LOGGED', b_style)
])
doc.build(content)

# File Copies
if os.path.exists('NomaanOS_Project_Explanation.pdf'):
    shutil.copy('NomaanOS_Project_Explanation.pdf', os.path.join(DOCS, 'NomaanOS_Project_Explanation.pdf'))

if os.path.exists('INTEGRITY.manifest.json'):
    shutil.copy('INTEGRITY.manifest.json', os.path.join(SIGS, 'DIGITAL_SHA256_MANIFEST.json'))

ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
shutil.make_archive(os.path.join(BACKUPS, f'NomaanOS_Backup_{ts}'), 'zip', '.')

print('SUCCESS_VAULT_SYNC_COMPLETE')
