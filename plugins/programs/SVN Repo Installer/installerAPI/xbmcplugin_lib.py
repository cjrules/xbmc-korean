"""
 Common functions
"""

import os,sys
import xbmc
from urllib import unquote_plus, urlopen

__plugin__ = sys.modules["__main__"].__plugin__
__date__ = '19-06-2009'

#################################################################################################################
def log(msg):
	xbmc.log("[%s]: %s" % (__plugin__, msg), xbmc.LOGDEBUG)

log("Module: %s Dated: %s loaded!" % (__name__, __date__))

#################################################################################################################
def handleException(msg=""):
	import traceback
	import xbmcgui
	traceback.print_exc()
	xbmcgui.Dialog().ok(__plugin__ + " ERROR!", msg, str(sys.exc_info()[ 1 ]))

#################################################################################################################
class Info:
	def __init__( self, *args, **kwargs ):
		self.__dict__.update( kwargs )
		log( "Info() dict=%s" % self.__dict__ )
	def has_key(self, key):
		return self.__dict__.has_key(key)

#################################################################################################################
def loadFileObj( filename ):
	log( "loadFileObj() " + filename)
	try:
		file_handle = open( filename, "r" )
		loadObj = eval( file_handle.read() )
		file_handle.close()
	except Exception, e:
		log( "loadFileObj() " + str(e) )
		loadObj = None
	return loadObj

#################################################################################################################
def saveFileObj( filename, saveObj ):
	log( "saveFileObj() " + filename)
	try:
		file_handle = open( filename, "w" )
		file_handle.write( repr( saveObj ) )
		file_handle.close()
		return True
	except Exception, e:
		log( "save_file_obj() " + str(e) )
		return False

#################################################################################################################
def readURL( url ):
	log("readURL() url=" + url)
	try:
		sock = urlopen( url )
		doc = sock.read()
		sock.close()
		if ( "404 Not Found" in doc ):
			log("readURL() 404, Not found")
			doc = ""
		return doc
	except:
		log("readURL() %s" % sys.exc_info()[ 1 ])
		return None

#################################################################################################################
def deleteFile( fn ):
	try:
		os.remove( fn )
		log("deleteFile() deleted: " + fn)
	except: pass
