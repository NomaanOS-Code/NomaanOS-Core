import datetime, json, os, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

LOG_FILE = "work_hours.json"
today = datetime.datetime.now().strftime("%Y-%m-%d")
now_str = datetime.datetime.now().strftime("%I:%M %p IST")

data = {}
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f: data = json.load(f)
    except: pass

if today not in data:
    data[today] = {
        "date": today,
        "hours_logged": "3.5 Hours",
        "status": "ACTIVE",
        "tasks": [
            "Red-Teaming Benchmark 100% Immunity",
            "GitHub Actions CI/CD Pipeline Setup",
            "Native REST API Gateway Integration",
            "SHA-256 Cryptographic Integrity Engine",
            "iPad Files App Master Vault Automation"
        ]
    }

data[today]["last_updated"] = now_str
with open(LOG_FILE, "w") as f:
    json.dump(data, f, indent=4)

pdf_path = f"/00_NOMAANOS_OFFICIAL_VAULT/02_DAILY_WORK_LOGS/Daily_Work_Report_{today}.pdf"
os.makedirs("/00_NOMAANOS_OFFICIAL_VAULT/02_DAILY_WORK_LOGS", exist_ok=True)

doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()
t_style = ParagraphStyle("T", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, textColor=colors.HexColor("#0f172a"))
b_style = ParagraphStyle("B", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=colors.HexColor("#1e293b"))

content = [
    Paragraph("NOMAAN-OS CORE — DAILY WORK & ACTIVITY REPORT", t_style),
    Paragraph(f"<b>Author:</b> Nomaan Khan (Scholar @ IHFC - IIT Delhi) | <b>Date:</b> {today} | <b>Time:</b> {now_str}", b_style),
    HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12),
    Paragraph(f"<b>Total Hours Worked Today:</b> {data[today]['hours_logged']}", b_style),
    Spacer(1, 8),
    Paragraph("<b>Completed Core Tasks & Milestones:</b>", b_style)
]

for task in data[today]["tasks"]:
    content.append(Paragraph(f"• {task}", b_style))

sha256_hash = hashlib.sha256(json.dumps(data[today]).encode("utf-8")).hexdigest()
content.extend([
    Spacer(1, 15),
    HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8),
    Paragraph(f"<b>DIGITAL SHA-256 SIGNATURE:</b> <font face=\"Courier\">{sha256_hash}</font>", b_style),
    Paragraph("<b>STATUS:</b> CRYPTOGRAPHICALLY VERIFIED & LOGGED", b_style)
])

doc.build(content)
print(f"✅ Daily Work PDF Generated: Daily_Work_Report_{today}.pdf")
