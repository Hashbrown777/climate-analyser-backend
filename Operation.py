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
import urllib
import correlation

def Operation(conf,inputs,outputs):
        urls = inputs["urls"]["value"].split(',')
        if len(urls) < 2:
                        conf["lenv"]["message"] = "There has to be atleast two datasets"
                        return zoo.SERVICE_FAILED
        try:
                output = Dataset('data/sample.nc', 'w', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + "sample.nc" + "' for writing."
                return zoo.SERVICE_FAILED
        try:
                #dataset1D = Dataset(, 'r', format='NETCDF4')
                urllib.urlretrieve(urls[0],"data/url1.nc")
                dataset1D = Dataset("data/url1.nc", 'r', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + urls[0] + "' for reading."
                return zoo.SERVICE_FAILED
        try:
                #dataset3D = Dataset(inputs["url2"]["value"], 'r', format='NETCDF4')
                urllib.urlretrieve(urls[1],"data/url2.nc")
                dataset3D = Dataset("data/url2.nc", 'r', format='NETCDF4')
        except:
                conf["lenv"]["message"] = "Could not open '" + urls[1] + "' for reading."
                return zoo.SERVICE_FAILED

        if inputs["selection"]["value"] == "Coorelate":
                result = correlation.correlation(dataset1D, dataset3D, output)

        dataset1D.close()
        dataset3D.close()
        output.close()
        outputs["Result"]["value"]="http://130.56.248.143/data/sample.nc"

        return zoo.SERVICE_SUCCEEDED
                                                                                                                                              63,10-17      Bot

