from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 15)
        self.cell(0, 10, "Code Quality Analysis Report", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_table(self, data, headers):
        self.set_font('Helvetica', 'B', 9)
        col_width = 190 / len(headers)
        for header in headers:
            self.cell(col_width, 7, header, 1, 0, 'C')
        self.ln()

        self.set_font('Helvetica', '', 8)
        for row in data:
            for header in headers:
                cell_value = str(row.get(header, ''))
                self.cell(col_width, 6, cell_value, 1, 0, 'L')
            self.ln()
        self.ln(5)

def create_pdf_report(analysis_results, output_path="output/code_analysis_report.pdf"):
    os.makedirs("output", exist_ok=True)
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Overall Analysis Results")
    if analysis_results:
        headers = ["file", "line_count", "function_count", "avg_function_length", "max_function_length"]
        pdf.add_table(analysis_results, headers)
    else:
        pdf.chapter_body("No Python files found to analyze.")
    pdf.output(output_path)
