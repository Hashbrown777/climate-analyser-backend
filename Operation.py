#
# Zoo Adapter for Operations
# Author:		Robert Sinn
# Last modified: 20th April 2014
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

from netCDF4 import Dataset
import sys
import numpy
import zoo
import requests
import correlation
import os.path

def getFileNameFromUrl(url):
        return url.rsplit('/',1)

def getLocation(url):
        return "Thredds/sample/" + getFileNameFromUrl(url)[1]

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

def outputFileName(operation,url1,url2):
        name = str(operation) + '_' + getFileNameFromUrl(url1)[1].strip('.nc')
        name += '_' + getFileNameFromUrl(url2)[1].strip('.nc') + '.nc'
        return name

def Operation(conf,inputs,outputs):
        urls = inputs["urls"]["value"].split(',')
        outputFile = "Thredds/sample/" + outputFileName(inputs["selection"]["value"],urls[0],urls[1])
        if len(urls) < 2:
                        conf["lenv"]["message"] = "There has to be atleast two datasets"
                        return zoo.SERVICE_FAILED
        try:
                if readFileExistsInThredds(outputFile):
                        os.remove(outputFile)
                output = Dataset(outputFile, 'w', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + outputFile + "' for writing."
                return zoo.SERVICE_FAILED
        try:
                #dataset1D = Dataset(urls[0], 'r', format='NETCDF4')
                if readFileExistsInThredds(getLocation(urls[0])) == 0:
                        downloadFile(urls[0])
                dataset1D = Dataset(getLocation(urls[0]), 'r', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + urls[0] + "' for reading."
                return zoo.SERVICE_FAILED
        try:
                #dataset3D = Dataset(urls[1], 'r', format='NETCDF4')
                if readFileExistsInThredds(getLocation(urls[1])) == 0:
                        downloadFile(urls[1])
                dataset3D = Dataset(getLocation(urls[1]), 'r', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + urls[1] + "' for reading."
                return zoo.SERVICE_FAILED

        if inputs["selection"]["value"] == "correlate":
                result = correlation.correlation(dataset1D, dataset3D, output)

        dataset1D.close()
        dataset3D.close()
        output.close()
        outputs["Result"]["value"]="http://130.56.248.143/" + outputFile

        return zoo.SERVICE_SUCCEEDED
                                                                                                                                              90,2-9        Bot

