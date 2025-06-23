from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

# HTML Template
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Resume Builder</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            color: #00ffe7;
            text-align: center;
        }
        form {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: auto;
        }
        label, input, textarea {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }
        input, textarea {
            background-color: #2a2a2a;
            color: white;
            padding: 10px;
            border: 1px solid #444;
            border-radius: 5px;
        }
        button {
            background-color: #00ffe7;
            color: #000;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #00c8b9;
        }
    </style>
</head>
<body>
    <h1>Resume Builder</h1>
    <form method="POST" action="/generate">
        <label>Full Name:</label>
        <input type="text" name="name" required>

        <label>Email:</label>
        <input type="email" name="email" required>

        <label>Phone:</label>
        <input type="text" name="phone" required>

        <label>Address:</label>
        <input type="text" name="address" required>

        <label>LinkedIn:</label>
        <input type="text" name="linkedin" required>

        <label>GitHub:</label>
        <input type="text" name="github" required>

        <label>Summary:</label>
        <textarea name="summary" rows="4" required></textarea>

        <label>Skills (comma-separated):</label>
        <input type="text" name="skills" required>

        <button type="submit">Generate PDF</button>
    </form>
</body>
</html>
'''

# PDF Generator Class
class ResumePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.title, ln=True, align='C')

    def add_section(self, title, content_list):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 11)
        for line in content_list:
            self.multi_cell(0, 10, line)

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate():
    # Form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    linkedin = request.form['linkedin']
    github = request.form['github']
    summary = request.form['summary']
    skills = request.form['skills'].split(',')

    # Create PDF
    pdf = ResumePDF()
    pdf.title = name
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Phone: {phone}", ln=True)
    pdf.cell(0, 10, f"Address: {address}", ln=True)
    pdf.cell(0, 10, f"LinkedIn: {linkedin}", ln=True)
    pdf.cell(0, 10, f"GitHub: {github}", ln=True)
    pdf.ln(5)

    pdf.add_section("Professional Summary", [summary])
    pdf.add_section("Skills", skills)

    # Write PDF to memory
    buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_bytes)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
