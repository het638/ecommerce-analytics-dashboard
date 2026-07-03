from fpdf import FPDF, XPos, YPos
import os

BASE = os.path.dirname(__file__)
TXT  = os.path.join(BASE, "PROJECT_EXPLANATION.txt")
OUT  = os.path.join(BASE, "Project_Explanation_Het_Savani.pdf")

def clean(text):
    for k, v in {"—":"-","–":"-","'":"'","'":"'",""":'"',""":'"',"•":"*",
                 "│":"|","├":"+","└":"+","─":"-","├":"+",
                 "┐":"+","┘":"+","┬":"+","┴":"+","┼":"+"}.items():
        text = text.replace(k, v)
    # Remove any remaining non-latin-1 characters
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_margins(15, 15, 15)

# Title page header
pdf.set_fill_color(30, 33, 48)
pdf.rect(0, 0, 210, 40, "F")
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(15, 12)
pdf.cell(180, 10, "E-Commerce Sales & Customer Analytics", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "", 10)
pdf.set_x(15)
pdf.cell(180, 8, "Project Explanation Report  |  Het Savani", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(0, 0, 0)
pdf.ln(20)

with open(TXT, "r", encoding="utf-8") as f:
    lines = [clean(l.rstrip()) for l in f.readlines()]

for line in lines:
    # Reset x position before each line
    pdf.set_x(15)

    if line.startswith("===") or line.startswith("---"):
        pdf.set_draw_color(100, 100, 200)
        pdf.set_line_width(0.3)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(2)

    elif (line.strip() and line.strip() == line.strip().upper()
          and len(line.strip()) > 3
          and not line.strip().startswith("-")
          and not line.strip().startswith("*")
          and line.strip()[0].isdigit()):
        pdf.ln(3)
        pdf.set_fill_color(79, 142, 247)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_x(15)
        pdf.cell(180, 7, "  " + line.strip(), fill=True,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(1)

    elif (line.strip() and line.strip() == line.strip().upper()
          and 3 < len(line.strip()) < 50
          and not line.strip().startswith("-")
          and not line.strip()[0].isdigit()):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(50, 80, 180)
        pdf.set_x(15)
        pdf.cell(180, 6, line.strip(),
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

    elif line.strip().startswith(("-", "*")):
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        content = "   *  " + line.strip().lstrip("-* ").strip()
        pdf.set_x(15)
        pdf.multi_cell(180, 5, content)

    elif not line.strip():
        pdf.ln(2)

    else:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        pdf.set_x(15)
        pdf.multi_cell(180, 5, line.strip())

# Footer on last page
pdf.set_y(-15)
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(150, 150, 150)
pdf.cell(0, 8, "Het Savani  |  hetsavani2002@gmail.com", align="C")

pdf.output(OUT)
print(f"PDF saved: {OUT}")
