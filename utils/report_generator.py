from fpdf import FPDF

def generate_pdf_report(errors, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Validation Report for {filename}", ln=True, align='C')
    
    if errors:
        pdf.set_font("Arial", size=10)
        for error in errors:
            pdf.multi_cell(0, 10, txt=error)
    else:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="No Errors Found!", ln=True, align='C')

    return pdf.output(dest='S').encode('latin-1')
