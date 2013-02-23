#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# MIME generation of embedded multiparts - Chapter 9
# mime_gen_both.py
# This program requires Python 2.2.2 or above

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Utils, Encoders
import mimetypes, sys

def genpart(data, contenttype):
    maintype, subtype = contenttype.split('/')
    if maintype == 'text':
        retval = MIMEText(data, _subtype=subtype)
    else:
        retval = MIMEBase(maintype, subtype)
        retval.set_payload(data)
        Encoders.encode_base64(retval)
    return retval


def attachment(filename):
    fd = open(filename, 'rb')
    mimetype, mimeencoding = mimetypes.guess_type(filename)
    if mimeencoding or (mimetype is None):
        mimetype = 'application/octet-stream'
    retval = genpart(fd.read(), mimetype)
    retval.add_header('Content-Disposition', 'attachment',
            filename = filename)
    fd.close()
    return retval

messagetext = """Hello,

This is a *great* test message from Chapter 9.  I hope you enjoy it!

-- Anonymous"""
messagehtml = """Hello 你好,<P>
This is a <B>great</B> test message from Chapter 9.  I hope you enjoy
it!<P>
-- <I>Anonymous</I>"""
fd = open('goagent.html', 'rb')
messagehtml = fd.read()
fd.close()
msg = MIMEMultipart()
msg['To'] = 'goagent@goagent.org'
msg['From'] = 'Goagent <http://code.google.com/p/goagent/>'
msg['Subject'] = '使用GoAgent看YouTube视频,上BBC学英语'
msg['Date'] = Utils.formatdate(localtime = 1)
msg['Message-ID'] = Utils.make_msgid()

body = MIMEMultipart('alternative')
#body.attach(genpart(messagetext, 'text/plain'))
body.attach(genpart(messagehtml, 'text/html'))
msg.attach(body)
#filelist = ['goagenthome.jpg','IE_set.jpg','ie_con_proxy.jpg','proxy_set.jpg']
#for filename in filelist:
#    msg.attach(attachment(filename))
#print msg.as_string()
