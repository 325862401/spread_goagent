#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Request, Response
from spread_goagent import getexsitQQlist,sendmailto
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

@app.route('/to/<int:qq_num>')
def send_mailto(qq_num):
    return sendmailto(qq_num)


if __name__ == '__main__':
    app.run()