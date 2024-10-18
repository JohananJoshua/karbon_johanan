from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from model import probe_model_5l_profit  # Importing the model
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Root route to display the file upload form
@app.route('/')
def upload_file():
    return render_template('upload.html')

# Route to handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.json'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Load and process JSON using model.py
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            result = probe_model_5l_profit(data["data"])

        # Pass the result to the result page
        return render_template('results.html', result=result)

    else:
        flash('Only JSON files are allowed!')
        return redirect(request.url)

# Route to display the results
@app.route('/results')
def show_results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
