from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Scan file (replace with actual scanning logic as needed)
        scan_result = scan_file(file_path)

        # Generate PDF report
        report_path = generate_pdf_report(scan_result, filename)
        
        # Provide the downloadable report
        return send_file(report_path, as_attachment=True)

    flash('File type not allowed')
    return redirect(request.url)

def scan_file(file_path):
    # Placeholder for actual file scanning logic
    # Mock result for demonstration
    scan_result = {
        'file_name': os.path.basename(file_path),
        'file_size': os.path.getsize(file_path),
        'scan_time': '17:44:45',
        'scan_date': '15/10/2014',
        'positive_matches': 41,
        'total_engines': 53,
        'engine_results': [
            {'engine': 'Bkav', 'detected': 'true', 'malware': 'MW.Clod26f.Trojan.4e44', 'version': '1.3.0.4959', 'date': '20141014'},
            {'engine': 'MicroWorld-eScan', 'detected': 'true', 'malware': 'Android.Trojan.Zsone.A', 'version': '12.0.250.0', 'date': '20141015'},
            # Add more entries as needed
        ]
    }
    return scan_result

def generate_pdf_report(scan_result, filename):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Scan Report', ln=True, align='C')
    
    # File information
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"File name: {scan_result['file_name']}")
    pdf.multi_cell(0, 10, f"File size: {scan_result['file_size']} KB")
    pdf.multi_cell(0, 10, f"Analysis time: {scan_result['scan_time']}")
    pdf.multi_cell(0, 10, f"Analysis date: {scan_result['scan_date']}")
    pdf.multi_cell(0, 10, f"Number of positive matches: {scan_result['positive_matches']} out of {scan_result['total_engines']} antimalware engines.")
    
    # Table header
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Antimalware Engine', 1)
    pdf.cell(30, 10, 'Malware Detected', 1)
    pdf.cell(60, 10, 'Malware Type', 1)
    pdf.cell(30, 10, 'Engine Version', 1)
    pdf.cell(30, 10, 'Last Engine Update', 1)
    pdf.ln()

    # Table rows
    pdf.set_font('Arial', '', 10)
    for result in scan_result['engine_results']:
        pdf.cell(40, 10, result['engine'], 1)
        pdf.cell(30, 10, result['detected'], 1)
        pdf.cell(60, 10, result['malware'], 1)
        pdf.cell(30, 10, result['version'], 1)
        pdf.cell(30, 10, result['date'], 1)
        pdf.ln()
    
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_report.pdf")
    pdf.output(report_path)
    
    return report_path

if __name__ == '__main__':
    app.run(debug=True)
