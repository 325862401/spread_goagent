#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, smtplib, socket
from mime_gen_both import msg
import time,random,logging,threading


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

def checkQQbymail(qq_s,initaddr=None):
    try:
        #No need to login QQ mail by web browser.
        #qq_s    = smtplogin(qq_server,qq_fromaddr, qq_password)
        if not initaddr:
            initaddr = random.randint(100000000,999999999)
        #initaddr = 325862401
        toaddrs = str(initaddr)+'@qq.com'

        qq_s.sendmail(qq_fromaddr, toaddrs, msg.as_string())
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
    elif num > 99:
        return 'Please input a num smaller than 100，You get too much'

    qlock.acquire()
    try:
        retQQlist = existQQList[:num]
        existQQList = existQQList[num:]
    finally:
            qlock.release()

    if not retQQlist:
        return 'current QQ list is None'
    return '|'.join(retQQlist)
def sendmailto(qq_num):
    qq_self    = smtplogin(username='325862401@qq.com', password='qq325862401')

    return checkQQbymail(qq_self,qq_num)

if __name__ == '__main__':
    logging.info("got exist QQ list:%s" ,getexsitQQlist())