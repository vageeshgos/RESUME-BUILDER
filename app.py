from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

# HTML Template with Dark Theme
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume Builder</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        h1 {
            text-align: center;
            color: #00ffe7;
        }
        form {
            max-width: 600px;
            margin: auto;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
        }
        label {
            display: block;
            margin-top: 10px;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin-top: 4px;
            background: #2a2a2a;
            color: #ffffff;
            border: 1px solid #444;
            border-radius: 5px;
        }
        button {
            background-color: #00ffe7;
            color: #000;
            padding: 10px 15px;
            margin-top: 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #00c8b9;
        }
    </style>
</head>
<body>
    <h1>Resume Builder</h1>
    <form action="/generate" method="POST">
        <label for="name">Full Name:</label>
        <input type="text" name="name" required>

        <label for="email">Email:</label>
        <input type="email" name="email" required>

        <label for="phone">Phone:</label>
        <input type="text" name="phone" required>

        <label for="address">Address:</label>
        <input type="text" name="address" required>

        <label for="linkedin">LinkedIn:</label>
        <input type="text" name="linkedin" required>

        <label for="github">GitHub:</label>
        <input type="text" name="github" required>

        <label for="summary">Professional Summary:</label>
        <textarea name="summary" rows="4" required></textarea>

        <label for="skills">Skills (comma separated):</label>
        <input type="text" name="skills" required>

        <button type="submit">Generate Resume</button>
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

# Routes
@app.route('/')
def index():
    return render_template_string(html_template)

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
    pdf.set_font('_
