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
	return url.rsplit('/',1)

def getLocation(url):
	return "Thredds/inputs/" + getFileNameFromUrl(url)[1]

def readFileExistsInThredds(name):
	return os.path.isfile(name)

def downloadFile(url):
	filePath = getLocation(url)
	r = requests.get(url)
	f = open(filePath, 'wb')
	for chunk in r.iter_content(chunk_size=512 * 1024): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	f.close()
	return 

def outputFileName(operation,urls):
	name = str(operation)
	for url in urls:
		name += '_' + getFileNameFromUrl(url)[1].strip('.nc')
	name += '.nc'
	return name

def filecheck(urls):
	for url in urls:
		if readFileExistsInThredds(getLocation(url)) == 0:
			downloadFile(url)

def Operation(conf,inputs,outputs):
	urls = inputs["urls"]["value"].split(',')
	filename = outputFileName(inputs["selection"]["value"],urls)
	outputFile = "Thredds/outputs/" + filename
	if len(urls) < 1:
			conf["lenv"]["message"] = "There has to be atleast one datasets"
			return zoo.SERVICE_FAILED
	try:
		if readFileExistsInThredds(outputFile):
			os.remove(outputFile)
	except:
		conf["lenv"]["message"] = "Could not open '" + outputFile + "' for writing."
		return zoo.SERVICE_FAILED
       
	filecheck(urls)

	if inputs["selection"]["value"] == "correlate":
		result = correlation.runCorrelate(getLocation(urls[0]),
				getLocation(urls[1]), outputFile)
	if inputs["selection"]["value"] == "regres":
		regresion.runRegres(getLocation(urls[0]),outputFile)
	
	#outputs["Result"]["value"]="http://130.56.248.143/" + outputFile
	outputs["Result"]["value"]=(
		"http://115.146.84.143:8080/thredds/catalog/datafiles/outputs/catalog.html" +
			"?dataset=climateAnalyserStorage/outputs/" + filename)

	return zoo.SERVICE_SUCCEEDED
