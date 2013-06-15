#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, smtplib, socket
from mime_gen_both import msg
import time,random,logging,threading
import re

qq_server = 'smtp.qq.com'
qq_fromaddr = '1281795027@qq.com'
qq_password = 'a6857018'
initaddr = ''
existQQList = []
qlock = threading.Lock()
def serverstarttls(s):
    code = s.ehlo()[0]
    usesesmtp = 1
    if not (200 <= code <= 299):
        usesesmtp = 0
        code = s.helo()[0]
        if not (200 <= code <= 299):
            raise SMTPHeloError(code, resp)

    if usesesmtp and s.has_extn('starttls'):
        logging.info("Negotiating TLS....")
        s.starttls()
        code = s.ehlo()[0]
        if not (200 <= code <= 299):
            logging.info("Couldn't EHLO after STARTTLS")

        logging.info("Using TLS connection.")
    else:
        logging.info("server does not support TLS; using normal connection.")


def smtplogin(server=qq_server,username=qq_fromaddr, password=qq_password):
    try:
        s = smtplib.SMTP(server)
        logging.info("%s start TLS" ,server)
        serverstarttls(s)
        try:
            s.login(username, password)
        except smtplib.SMTPException, e:
            logging.info("Authentication failed:%s", repr(e))

    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
        e:
        loging.info('%s',repr(e))

    else:
        logging.info("You have connected to %s and login successfully",server)


        return s

def checkQQbymail(qq_s,fromaddr=qq_fromaddr,initaddr=None):
    try:
        if not initaddr:
            initaddr = str(random.randint(100000000,9999999999))

        if '@' in initaddr:
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', initaddr):
                logging.error('email format wrong,please input you valid mail address!')
                return 'please input correct mail address'
            else:
                toaddrs = initaddr
        else:
            toaddrs = str(initaddr)+'@qq.com'

        qq_s.sendmail(fromaddr, toaddrs, msg.as_string())
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), \
                e:
        logging.info('%s',repr(e))
        if 'Mailbox not found' in repr(e):
            logging.info('%s does not exist',str(initaddr))
            return None
        else:
            logging.info('%s exist',str(initaddr))
            return str(initaddr)
    else:
        logging.info('successfully send a mail by QQ server')
        return str(initaddr)

def threadcode():
    qq_s    = smtplogin(qq_server,qq_fromaddr, qq_password)
    global existQQList,qlock
    while 1:
        time.sleep(1)
        reval = checkQQbymail(qq_s)
        if reval:
            qlock.acquire()
            try:
                existQQList.append(reval)
            finally:
                qlock.release()

            #logging.info("add a new exist qq num:%s", ','.join(existQQList))
        while len(existQQList) > 100000:
            time.sleep(1000)
class runOnceThread:

    mythreadNotexist = True

    def __init__(self):
        self.thread = runOnceThread.mythreadNotexist and threading.Thread(target=threadcode,name='mythread') or None
        runOnceThread.mythreadNotexist = False


def getexsitQQlist(num=1):
    global existQQList,qlock
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    if not existQQList:
        t = runOnceThread()
        if t.thread:
                t.thread.setDaemon(1)
                t.thread.start()
                logging.info('t create thread successfully')
        else:
            del t

    if num < 0:
        return 'Please input a num larger than 0'
    elif num == 0:
        return '325862401'
    elif num == 200:
        return str(len(existQQList))
    elif num > 200:
        return 'Please input a num smaller than 200，You get too much'

    qlock.acquire()
    try:
        retQQlist = existQQList[:num]
        existQQList = existQQList[num:]
    finally:
            qlock.release()

    if not retQQlist:
        return 'current QQ list is None'
    return '|'.join(retQQlist)
def sendmailto(addr):
    qq_self    = smtplogin(server='smtp.163.com',username='663696mm@163.com', password='663696')
    return checkQQbymail(qq_self,'663696mm@163.com',addr)

if __name__ == '__main__':
    logging.info("got exist QQ list:%s" ,getexsitQQlist())