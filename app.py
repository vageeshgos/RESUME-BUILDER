from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

class ResumePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, 0, 1, 'C')

    def add_section(self, title, content_list):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Arial', '', 11)
        for line in content_list:
            self.multi_cell(0, 10, line)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Fetch form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    linkedin = request.form['linkedin']
    github = request.form['github']
    skills = request.form['skills'].split(',')
    summary = request.form['summary']

    # Start PDF generation
    pdf = ResumePDF()
    pdf.title = name
    pdf.add_page()

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Email: {email}", 0, 1)
    pdf.cell(0, 10, f"Phone: {phone}", 0, 1)
    pdf.cell(0, 10, f"Address: {address}", 0, 1)
    pdf.cell(0, 10, f"LinkedIn: {linkedin}", 0, 1)
    pdf.cell(0, 10, f"GitHub: {github}", 0, 1)
    pdf.ln(5)

    pdf.add_section("Professional Summary", [summary])
    pdf.add_section("Skills", skills)

    # Generate file in memory
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="resume.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)
