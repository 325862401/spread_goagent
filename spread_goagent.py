#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, smtplib, socket
from mime_gen_both import msg
import time,random

gmail_server = 'smtp.gmail.com'
gmail_fromaddr = 'your-id@gmail.com'
gmail_password = 'xxxxxx'

qq_server = 'smtp.qq.com'
qq_fromaddr = 'your_qq@qq.com'
qq_password = 'xxxxxx'
initaddr = ''
cnt = 0
try:
    last_line = file('success_sendmail.txt', "r").readlines()[-1]
    if last_line.split('\t')[1].isdigit():
        cnt =  int(last_line.split('\t')[1]) 
    else:
        cnt = 0
    if len(last_line.split('\t')) >= 3:
        print "You last sent email successfully at %s" %last_line.split('\t')[2]
except IOError:
    print "open success_sendmail.txt occur error"
    
def saveintofile():
    fd = open('success_sendmail.txt','a')    
    fd.write(str(initaddr)+'\t'+str(cnt)+'\t'+time.asctime()+'\n')
    fd.close()
def serverstarttls(s):
    code = s.ehlo()[0]
    usesesmtp = 1
    if not (200 <= code <= 299):
        usesesmtp = 0
        code = s.helo()[0]
        if not (200 <= code <= 299):
            raise SMTPHeloError(code, resp)

    if usesesmtp and s.has_extn('starttls'):
        print "Negotiating TLS...."
        s.starttls()
        code = s.ehlo()[0]
        if not (200 <= code <= 299):
            print "Couldn't EHLO after STARTTLS"
            sys.exit(5)
        print "Using TLS connection."
    else:
        print "server does not support TLS; using normal connection."
def smtplogin(server,username, password):
    try:
        #You must enable 'smtp' at you QQ mail setting
        #You must login your gmail by web browser first,otherwise authentication will fail.
        s = smtplib.SMTP(server)
        print "%s start TLS" %server
        serverstarttls(s)
        try:
            s.login(username, password)
        except smtplib.SMTPException, e:
            print "Authentication failed:", e
            sys.exit(1)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
        e:
        print " %s connect smtp server error!" %server
        print e
        sys.exit(2)
    else:
        print "You have connected to %s and login successfully" %server
        return s
 
try:
    #You must login your gmail by web browser first,otherwise authentication will fail.
    gmail_s = smtplogin(gmail_server,gmail_fromaddr, gmail_password)
    #No need to login QQ mail by web browser.
    qq_s    = smtplogin(qq_server,qq_fromaddr, qq_password)
    while 1:
        initaddr = random.randint(100000000,999999999)
        toaddrs = str(initaddr)+'@qq.com'
        time.sleep(1)
        try:
            qq_s.sendmail(qq_fromaddr, toaddrs, msg.as_string())
        except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
                e:
            print e              
            if 'Mailbox not found' in repr(e):
                continue
            print " *** Your message may not have been sent by QQ server and try gmail again!"
            try:
                gmail_s.sendmail(gmail_fromaddr, toaddrs, msg.as_string())
            except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
                e:
                print " *** Your message may not have been sent by gmail server!"
                print e
                if 'Daily sending quota exceeded' in repr(e):
                    exit(0)
                continue    
            print "Message successfully sent to one recipient by gmail server"        
            cnt += 1
            saveintofile()
            continue

        print "Message successfully sent to one recipient by QQ server"
        cnt += 1
        saveintofile()
        continue
                
except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
        e:
    print " *** Your message may not have been sent!"
    print e
    sys.exit(1)