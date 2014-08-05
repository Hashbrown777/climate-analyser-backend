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
import zoo
import requests
import correlation
import regresion
import os.path
import os

def getFileNameFromUrl(url):
	return url.rsplit('/',1)[1].split('?',1)[0]

def getDownloadLocation(url):
	return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getLocation(url,serverAddr):
	if localFile(url):
		return dataLink(serverAddr,getFileNameFromUrl(url),getVariables(url))	
	else:
		return url
	#return "/var/www/cgi-bin/Thredds/inputs/" + getFileNameFromUrl(url)

def getVariables(url):
	return "?" + url.rsplit('/',1)[1].split('?',1)[1]

def dataLink(serverAddr,filename):
	return (serverAddr + "/thredds/dodsC/datafiles/inputs/" + filename)

def outputFileName(operation,urls):
	name = str(operation)
	for url in urls:
		name += '_' + getFileNameFromUrl(url).strip('.nc')
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
	if not "/dodsC/" in url:
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

def Operation(conf,inputs,outputs):
	urls = inputs["urls"]["value"].split(',')
	filename = outputFileName(inputs["selection"]["value"],urls)
	outputFile = "/var/www/cgi-bin/Thredds/outputs/" + filename
	serverAddr = "http://115.146.84.143:8080"
	if len(urls) < 1:
			conf["lenv"]["message"] = "There has to be atleast one dataset"
			return zoo.SERVICE_FAILED
	try:
		if readFileExistsInThredds(outputFile):
		        #outputs["Result"]["value"]=(resultOut(filename))
		        #return zoo.SERVICE_SUCCEEDED
			os.remove(outputFile)
	except:
		conf["lenv"]["message"] = "Could not open '" + outputFile + "' for writing."
		return zoo.SERVICE_FAILED
       
	filecheck(urls)

	if inputs["selection"]["value"] == "correlate":
		result = correlation.runCorrelate(getLocation(urls[0],serverAddr),
				getLocation(urls[1],serverAddr), outputFile)
	if inputs["selection"]["value"] == "regres":
		regresion.runRegres(getLocation(urls[0],serverAddr),outputFile)
	
        outputs["Result"]["value"]=(resultOut(filename,serverAddr))

	return zoo.SERVICE_SUCCEEDED
