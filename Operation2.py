#
# Zoo Adapter for Correlate
# Author:		Robert Sinn
# Last modified: 13 May 2014
#
# This file is part of Climate Analyser.
#
# Climate Analyser is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Climate Analyser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Climate Analyser.
# If not, see <http://www.gnu.org/licenses/>.
#

import sys
import requests
import correlation
import convolute
import regresion
import os.path
import os
import string
import random
import rsa
import urllib
import base64

from cdo import *

def getFileNameFromUrl(url):
	return url.rsplit('/',1)[1].split('?',1)[0]

def getDownloadLocation(url):
	return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getLocation(url):
	return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url) #delete line when cleanup
	#if localFile(url):
	#	return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)
		#return dataLink(serverAddr,getFileNameFromUrl(url),getVariables(url))	
	#else:
	#	return url
	#return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getVariables(url):
	if "?" in url:
		return "?" + url.rsplit('/',1)[1].split('?',1)[1]
	else:
		return ""

def dataLink(serverAddr,url):
	return (serverAddr + "/thredds/dodsC/datafiles/inputs/" + 
					getFileNameFromUrl(url) + getVariables(url))

def readFileExistsInThredds(name):
	return os.path.isfile(name)

def filecheck(urls):
	for url in urls:
		if readFileExistsInThredds(getDownloadLocation(url)) == 0:
			downloadFile(url)

def localFile(url):
	if not "/dodsC/" in url:	#check this
		return 1
	else:
		return 0

def downloadFile(url):
	if localFile(url):
		filePath = getDownloadLocation(url)
		r = requests.get(url)
		f = open(filePath, 'wb')
		for chunk in r.iter_content(chunk_size=512 * 1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
		f.close()
	else:
		cdo = Cdo()
		print url.split('?',1)[0]
    		cdo.copy(input = url.split('?',1)[0], output = getDownloadLocation(url))
	return 

#def resultOut(filename,serverAddr):
#	outputLink = "[opendap]"
#	outputLink += (serverAddr + "/thredds/catalog/datafiles/outputs/catalog.html?dataset=climateAnalyserStorage/outputs/" + filename)
#	outputLink += "[/opendap]"
#	outputLink += "[ncfile]"
#	outputLink += (serverAddr + "/thredds/fileServer/datafiles/outputs/" + filename)
#	outputLink += "[/ncfile]"
#	outputLink += "[wms]"
#	outputLink += (serverAddr + "/thredds/wms/datafiles/outputs/" + filename + "?service=WMS&version=1.3.0&request=GetCapabilities")
#	outputLink += "[/wms]"
#	return outputLink

def getUrls(inputUrls):
	urls = inputUrls.split(",http")
        for x in range(1, len(urls)):
                urls[x] = 'http' + urls[x]
	return urls

def jobStatus(jobid,status):
	djangoFile = open('DjangoServer')
	djangoAddr = djangoFile.read().strip()
	publicfile = open('publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	wCall = djangoAddr + '/update_computation_status?id='
	wCall += encryptField(pubkey,jobid)
	wCall += '&status='
	wCall += encryptField(pubkey,status)
	urllib.urlopen(wCall)

def encryptField(pubkey, value):
	crypto = rsa.encrypt(value,pubkey)
	return base64.b64encode(urllib.quote_plus(crypto))

def getServerAddr():
	serverFile = open('ThreddServer')
	return serverFile.read().strip()

def Operation(Urls,Selection,Jobid):
	jobStatus(Jobid,'running')
	urls = getUrls(Urls)
	#filename = outputFileName(Selection,urls,Jobid)
	filename = Jobid + '.nc'
	outputFile = "/var/www/cgi-bin/Thredds/outputs/" + filename

	serverAddr = getServerAddr()
	if len(urls) < 1:
		jobStatus(Jobid,'3')
		return
	try:
		if readFileExistsInThredds(outputFile):
			jobStatus(Jobid,'2')
		        return
	except:
		jobStatus(Jobid,'4')
		return # "Could not open '" + outputFile + "' for writing." 
       
	filecheck(urls)
	
	if Selection == "correlate":
		result = correlation.runCorrelate(getLocation(urls[0]),
				getLocation(urls[1]), outputFile)
	if Selection == "convolute":
		result = convolute.runConvolute(getLocation(urls[0]),
				getLocation(urls[1]), outputFile)
	if Selection == "regres":
		regresion.runRegres(dataLink(serverAddr,urls[0]),outputFile)

	jobStatus(Jobid,'2')
        return  

def main():
	#try:
        Operation(sys.argv[1],sys.argv[2],sys.argv[3])
	#except:
	#	jobStatus(sys.argv[3],'7')

if __name__ == '__main__':
        exitCode = main()
        exit(exitCode)
