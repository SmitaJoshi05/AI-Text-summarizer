# from flask import Flask, render_template

# app = Flask(__name__)  # Default uses 'static' and 'templates'

# @app.route('/')
# def landing():
#     return render_template('landing.html')

# if __name__ == '__main__':
#     app.run(debug=True)
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, request
from db import db, init_db
from auth import auth_bp
from model import summarize_text

app = Flask(__name__)
app.secret_key = 'your-secret-key'
init_db(app)
app.register_blueprint(auth_bp)

@app.route('/')
def landing():
    return render_template('landing.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' in session:
#         return render_template('dashboard.html')
#     return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    from db import db, Summary
    user_summaries = Summary.query.filter_by(user_id=session['user_id']).all()

    return render_template('dashboard.html', summaries=user_summaries)


@app.route('/delete_summary/<int:summary_id>')
def delete_summary(summary_id):
    if 'user_id' not in session:
        return redirect('/login')

    from db import db, Summary
    summary = Summary.query.get_or_404(summary_id)

    if summary.user_id == session['user_id']:
        db.session.delete(summary)
        db.session.commit()

    return redirect('/dashboard')



# @app.route('/summarize', methods=['GET', 'POST'])
# def summarize():
#     if request.method == 'POST':
#         text = request.form.get('text')
        
#         # Use the function from model.py to get the summary
#         summary = summarize_text(text)

#         # Save summary to DB if logged in
#         if 'user_id' in session:
#             from db import db, Summary
#             new_summary = Summary(user_id=session['user_id'], text=text, summary=summary)
#             db.session.add(new_summary)
#             db.session.commit()

#         return render_template('summarizer.html', summary=summary, original=text)

#     return render_template('summarizer.html')

UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        text = request.form.get('text')

        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Extract text from file
                text = extract_text_from_file(filepath)

        # Generate the summary using the Pegasus model
        summary = summarize_text(text)

        # Save summary to DB if logged in
        if 'user_id' in session:
            from db import db, Summary
            new_summary = Summary(user_id=session['user_id'], text=text, summary=summary)
            db.session.add(new_summary)
            db.session.commit()

        return render_template('summarizer.html', summary=summary, original=text)

    return render_template('summarizer.html')

def extract_text_from_file(filepath):
    """
    Extract text from uploaded file.
    Currently supports .txt files; you can extend this to .pdf or other formats.
    """
    if filepath.endswith('.txt'):
        with open(filepath, 'r') as file:
            return file.read()
    elif filepath.endswith('.pdf'):
        # Use PyPDF2 or pdfminer to extract text from PDFs
        import PyPDF2
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    return ""


if __name__ == '__main__':
    app.run(debug=True)
