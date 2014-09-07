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
import regresion
import os.path
import os
import string
import random
import rsa
import urllib
import base64

def getFileNameFromUrl(url):
		return url.rsplit('/',1)[1].split('?',1)[0]

def getDownloadLocation(url):
	return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getLocation(url,serverAddr):
	if localFile(url):
		return dataLink(serverAddr,getFileNameFromUrl(url),getVariables(url))	
	else:
		if "http" not in url:
			url = "http" + url
		return url
	#return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getVariables(url):
	if "?" in url:
		return "?" + url.rsplit('/',1)[1].split('?',1)[1]
	else:
		return ""

def dataLink(serverAddr,filename,variables):
	return (serverAddr + "/thredds/dodsC/datafiles/inputs/" + filename + variables)

def outputFileName(operation,urls,jobid):
	name = str(operation)
	for url in urls:
		name += '_' + getFileNameFromUrl(url).strip('.nc')
	if any('?' in url for url in urls):
		name += (jobid)
		if readFileExistsInThredds("/var/www/cgi-bin/Thredds/outputs/"+name+'.nc'):
			return outputFileName
	name += '.nc'
	return name

def readFileExistsInThredds(name):
	return os.path.isfile(name)

def filecheck(urls):
	for url in urls:
		if readFileExistsInThredds(getDownloadLocation(url)) == 0:
			if localFile(url):
				downloadFile(url)

def localFile(url):
	if not "/dodsC/" in url:	#check this
		return 1
	else:
		return 0

def downloadFile(url):
	filePath = getDownloadLocation(url)
	r = requests.get(url)
	f = open(filePath, 'wb')
	for chunk in r.iter_content(chunk_size=512 * 1024): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	f.close()
	return 

def resultOut(filename,serverAddr):
	outputLink = "[opendap]"
	outputLink += (serverAddr + "/thredds/catalog/datafiles/outputs/catalog.html?dataset=climateAnalyserStorage/outputs/" + filename)
	outputLink += "[/opendap]"
	outputLink += "[ncfile]"
	outputLink += (serverAddr + "/thredds/fileServer/datafiles/outputs/" + filename)
	outputLink += "[/ncfile]"
	outputLink += "[wms]"
	outputLink += (serverAddr + "/thredds/wms/datafiles/outputs/" + filename + "?service=WMS&version=1.3.0&request=GetCapabilities")
	outputLink += "[/wms]"
	return outputLink

def getUrls(inputUrls):
	urls = inputUrls.split(",http")
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

def Operation(Urls,Selection,Jobid):
	jobStatus(Jobid,'running')
	urls = getUrls(Urls)
	filename = outputFileName(Selection,urls,Jobid)
	outputFile = "/var/www/cgi-bin/Thredds/outputs/" + filename
	serverFile = open('ThreddServer')
	serverAddr = serverFile.read().strip()
	if len(urls) < 1:
		jobStatus(Jobid,'failed')
		return
	try:
		if readFileExistsInThredds(outputFile):
			jobStatus(Jobid,'successful')
		        return
	except:
		jobStatus(Jobid,'failed')
		return # "Could not open '" + outputFile + "' for writing." 
       
	filecheck(urls)

	if Selection == "correlate":
		result = correlation.runCorrelate(getLocation(urls[0],serverAddr),
				getLocation(urls[1],serverAddr), outputFile)
	if Selection == "regres":
		regresion.runRegres(getLocation(urls[0],serverAddr),outputFile)

	jobStatus(Jobid,'successful')
        return (resultOut(filename,serverAddr)) #Use ben's script to send back this info

def main():
	try:
        	Operation(sys.argv[1],sys.argv[2],sys.argv[3])
	except:
		jobStatus(sys.argv[3],'failed')

if __name__ == '__main__':
        exitCode = main()
        exit(exitCode)
