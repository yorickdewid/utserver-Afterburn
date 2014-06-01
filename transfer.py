#!/usr/bin/env python

from os.path import dirname
import ConfigParser
import time
import sys
import os
import shutil

base_path = dirname(os.path.abspath(__file__))
fconf = os.path.join(base_path, 'settings.conf')

Config = ConfigParser.ConfigParser()
Config.read(fconf)

des = Config.get("Directory", "destination");
src = Config.get("Directory", "source");

def done():
   localtime = time.asctime(time.localtime(time.time()))
   print "[%s] done." % localtime 

def walk():
   for filename in os.listdir(src):
      shutil.move(os.path.join(src, filename), os.path.join(des, filename))

if __name__ == "__main__":
   walk()
   done()
