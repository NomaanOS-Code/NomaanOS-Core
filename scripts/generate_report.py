import json, datetime, os
from fpdf import FPDF

class NomaanOS_Report(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'NOMAANOS CORE // SOVEREIGN SCHOLAR REPORT', 0, 1, 'L')
        self.line(10, 20, 200, 20)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()} | Confidential - Nomaan Khan (IHFC IIT Delhi)', 0, 0, 'C')

def build_pdf():
    pdf = NomaanOS_Report()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Section
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 12, "Executive Work Log & System Audit", 0, 1, "L")
    
    # Metadata
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    pdf.cell(0, 6, f"Generated On: {now}", 0, 1, "L")
    pdf.cell(0, 6, "Author: Nomaan Khan (Scholar @ IHFC - IIT Delhi)", 0, 1, "L")
    pdf.ln(8)
    
    # Tasks Section
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 8, "Active Tasks & Logged Items", 0, 1, "L")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    
    # Read Tasks from JSON
    if os.path.exists("work_hours.json"):
        with open("work_hours.json", "r") as f:
            data = json.load(f)
            for date, details in list(data.items())[-5:]: # Last 5 records
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, f"Date: {date} | Status: {details.get('status', 'N/A')}", 0, 1, "L")
                pdf.set_font("Helvetica", "", 10)
                for task in details.get("tasks", []):
                    pdf.cell(10)
                    pdf.cell(0, 6, f"- {task}", 0, 1, "L")
                pdf.ln(3)
    else:
        pdf.cell(0, 6, "No work log found. Run 'python3 auto_tasks.py' first.", 0, 1, "L")
        
    # Output to Vault
    vault_dir = os.path.expanduser("~/workspace/NomaanOS-Core_recovery_final")
    out_file = os.path.join(vault_dir, "NomaanOS_Scholar_Report.pdf")
    pdf.output(out_file)
    print(f"✅ PDF Generated Successfully: {out_file}")

if __name__ == "__main__":
    build_pdf()
