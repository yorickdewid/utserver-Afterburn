#!/usr/bin/env python

from smtplib import SMTPException
from os.path import dirname
from utorrent.client import UTorrentClient
import ConfigParser
import smtplib
import time
import sys
import os
import shutil
import getopt

base_path = dirname(os.path.abspath(__file__))
fconf = os.path.join(base_path, 'settings.conf')

Config = ConfigParser.ConfigParser()
Config.read(fconf)

doMail = Config.get("Mail", "notice");
rName = Config.get("Mail", "name");
From = Config.get("Mail", "from");
Receiver = Config.get("Mail", "receiver");
Server = Config.get("Mail", "smtp");

def getContent(name, status):
   message  = "From: CouchPotato Afterburn <%s><br />\r\n" % From
   message += "To: %s <%s>\r\n" % (rName, Receiver)
   message += "MIME-Version: 1.0\r\n"
   message += "Content-type: text/html\r\n"
   message += "Subject: Download has finished\r\n"
   message += "The download <b>'%s'</b> is done and ready for transfer<br />\r\n" % name
   message += "Status: %s<br />\r\n" % status
   message += "<br />\r\n"
   message += "Greets,<br />\r\n"
   message += "Potato"
   return message

def removeTorrent(hash):
   ut = UTorrentClient('localhost', '8080')
   ut.remove(hash)

def sendMail(f, r, m, s):
   if doMail == 'true':
      try:
         smtpObj = smtplib.SMTP(s)
         smtpObj.sendmail(f, r, m)         
         print "Successfully sent email"
      except SMTPException:
         print "Error: unable to send email"

def done():
   ''' And we are done '''
   localtime = time.asctime(time.localtime(time.time()))
   print "[%s] done." % localtime 

def help():
   ''' Show help message '''
   print sys.argv[0]+' -n <name> -s <status>'

def parseArgs(argv):
   ''' parse commandline argument '''
   name = ''
   hash = ''
   status = ''

   try:
      opts, args = getopt.getopt(argv, "hn:s:i:", ["name=", "status=", "info="])
   except getopt.GetoptError:
      help()
   for opt, arg in opts:
      if opt == '-h':
         help()
      elif opt in ("-n", "--name"):
         name = arg
      elif opt in ("-s", "--status"):
         status = arg
      elif opt in ("-i", "--info-hash"):
         hash = arg

   removeTorrent(hash)
   Context = getContent(name, status)
   sendMail(From, Receiver, Context, Server)
   done()

if __name__ == "__main__":
   if len(sys.argv) < 3:
      help()
      sys.exit()
   else:
      parseArgs(sys.argv[1:])

