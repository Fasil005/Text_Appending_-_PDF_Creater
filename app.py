from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from fpdf import FPDF


from werkzeug.utils import secure_filename

import os

MAIN_PATH = 'static/main'
SECONDARY_PATH = 'static/secondary'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'html', 'py', 'css', 'js'}

pdf = FPDF()  
app = Flask(__name__)

app.config['SECRET_KEY'] = '1234issecret'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/appending", methods=['POST'])
def fileuploading():
    try:
        file = request.files['mainfile']
        file2 = request.files['secondaryfile']
        if file.filename == '':
            if file2.filename == '':
                flash('Select All Files')
                return redirect(url_for('home'))
        
        if file.filename == file2.filename:
 
            flash('Same File Selected')
            return redirect(url_for('home'))

        if file and allowed_file(file.filename) and allowed_file(file2.filename):
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(MAIN_PATH, filename))
            filename = secure_filename(file2.filename)
            file2.save(os.path.join(SECONDARY_PATH, filename))

            appending(file.filename,file2.filename)
    
        return render_template('index.html', filepath = f'{MAIN_PATH}/{file.filename}')
    except Exception as e:
        print(e)


def appending(file1,file2):

    try:

        mainfile = open(f'{MAIN_PATH}/{file1}','a')
        secondaryfile = open(f'{SECONDARY_PATH}/{file2}','r')

        for line in secondaryfile:

            mainfile.write(line)
        mainfile.close()
        secondaryfile.close()

    except Exception as e:
        print(e)








@app.route("/pdfcreating", methods=['POST'])
def fileuploading2():
    try:
        file = request.files['mainfile']
        if file.filename == '':
            flash('Select a File to Create PDF')
            return redirect(url_for('home'))
        

        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(MAIN_PATH, filename))
            print(file.filename)
            file = creating(file.filename)
    
        return render_template('index.html', filepath = f'{MAIN_PATH}/{file}.pdf')
    except Exception as e:
        print(e)


def creating(file):

    try:

        mainfile = open(f'{MAIN_PATH}/{file}','r')
        
        pdf.add_page()

        pdf.set_font("Arial", size = 15)

        for x in mainfile:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
        file = file.split('.',1)[0]
        pdf.output(f'{MAIN_PATH}/{file}.pdf')   

        return file

    except Exception as e:
        print(e)
        


if __name__ == "__main__":
    app.run(debug=True)