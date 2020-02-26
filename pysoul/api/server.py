from flask import Flask , render_template , request , jsonify, Response
import sys
import os
from flask_cors import CORS , cross_origin
import json
import base64
from PIL import Image
from io import BytesIO
import re
from pathlib import Path
from werkzeug import secure_filename
from pysoul.extract import extract_content
from pysoul.detect import detect
from pysoul.generatepdf import generate_pdf
from pysoul.generatetext import generate_text
from pysoul.filter import filter_content






app = Flask(__name__)
#cors
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app , resources={ r'/*': {'origins': "http://10.10.0.7:30976"}})
# app.config.from_object(os.environ['APP_SETTINGS'])
CRNT_DIR = os.getcwd()
path = Path(CRNT_DIR)
path = path
UPLOAD_FOLDER =str(Path(path)) + '/input'
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


def perform_deidentification(path):
    extract_content(path,0)
    detect.detect_phi()
    generate_pdf(path ,0)
    generate_text()
    filter_content()
    
    
    


@app.route('/')
def index():
    return render_template('index.html')    





@app.route('/upload' , methods=['POST'])
def imageupload():
    if request.method == 'POST':
        file = request.files['file']
        filename = ''
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #perform model script
            path = 'input/' + filename
            perform_deidentification(path)
        pdf_file = str(CRNT_DIR) + '/output/' + filename.split('.')[0] + '/'+'output.pdf'
        pdf = open(pdf_file, 'rb').read()
        response=pdf_response(pdf , filename)
    return response

def pdf_response(pdf, filename):
    resp = Response(pdf)
    # resp.headers['Content-Disposition'] = "inline; filename=%s" % filename
    resp.mimetype = 'application/pdf'
    resp.headers['Content-Type']='application/pdf'
    return resp



# def toBase64(filename , codec):
#     #converts image to binary and saves it
#     data = re.sub('^data:image/.+;base64,', '', codec)
#     byte_data = base64.b64decode(data)
#     img_data = BytesIO(byte_data)
#     img = Image.open(img_data)
#     img.save(uploads + filename , "PNG")
#     image_path = uploads + filename
#     return image_path

def run_server():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,threaded=False)