import drmaa
import os
import time
import zoo

def jobScheduler(conf,inputs,outputs):
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

	outputs["Result"]["value"]= "job deployed"
	return zoo.SERVICE_SUCCEEDED

