#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response,send_from_directory,redirect, url_for
from werkzeug import secure_filename
from spread_goagent import getexsitQQlist,sendmailto
import os

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','html'])

application = app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/uploads" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/')
def shareGoAgent():
    with open('goagent-home.html', 'r') as f:
        return f.read()

@app.route('/test')
def test():
    return getexsitQQlist(0)
    #return 'test url'

@app.route('/<int:num>')
def ret_num(num):
    return getexsitQQlist(num)

@app.route('/to/<addr>')
def send_mailto(addr):
    return sendmailto(addr)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run()