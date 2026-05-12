import traceback
from fpdf import FPDF
try:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(35, 10, 'CA', border=1, fill=False, align='C')
    pdf.ln(15)
    print('X:', pdf.get_x())
    pdf.multi_cell(0, 8, 'Abilita')
    print('OK')
except Exception as e:
    traceback.print_exc()
