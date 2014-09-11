import drmaa
import os
import time
import zoo

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

def jobScheduler(conf,inputs,outputs):
	serverFile = open('ThreddServer')
	serverAddr = serverFile.read().strip()
	urls = inputs["urls"]["value"]
	jobType = inputs["selection"]["value"]
	jobId = inputs["jobid"]["value"]

        sess = drmaa.Session()
        sess.initialize()
        # 'Creating job template'
        jt = sess.createJobTemplate()
        jt.remoteCommand = 'python Operation2.py'
        jt.args = [urls,jobType,jobId]
	jt.jobName = jobId
        sess.runJob(jt)
        #'Your job has been submitted with id ' + jobid

	sess.deleteJobTemplate(jt)
	sess.exit()

	outputs["Result"]["value"]=(resultOut(jobId,serverAddr))
	return zoo.SERVICE_SUCCEEDED

