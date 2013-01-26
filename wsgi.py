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

@app.route('/to/<addr>')
def send_mailto(addr):
    return sendmailto(addr)


if __name__ == '__main__':
    app.run()