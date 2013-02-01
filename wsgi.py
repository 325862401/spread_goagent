#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Request, Response,send_from_directory
from spread_goagent import getexsitQQlist,sendmailto
import os
application = app = Flask(__name__)

@app.route('/')
def hello_world():
    return getexsitQQlist()

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

@app.route('/share/goagent')
def shareGoAgent():
    with open('goagent.html', 'r') as f:
        return f.read()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.getcwd(),
                               filename)


if __name__ == '__main__':
    app.run()