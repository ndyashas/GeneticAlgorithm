from ga2.gaUtils.gaDeamon import *
from . import gaDisc 
import os,signal

def aexit(a,b):
	os.system('rm -Rf '+os.path.dirname(os.path.realpath(__file__))+'/gaUtils/utilFiles/*')
	os.sys.exit()

signal.signal(signal.SIGTERM,aexit)
signal.signal(signal.SIGINT,aexit)
signal.signal(signal.SIGABRT,aexit)

version = "0.2.9"
