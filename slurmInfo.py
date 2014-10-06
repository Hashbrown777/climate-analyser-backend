import subprocess
import os
import zoo

def callCommand(option):
	ret = subprocess.Popen([option], stdout=subprocess.PIPE)
	return ret.communicate()[0] + '\n'

def slurmInfo(conf,inputs,outputs):
        option = inputs["option"]["value"]
	slurmOut = ''
        if option == 'sinfo' or option == 'sall':
		slurmOut += callCommand('sinfo -N -l')
	if option == 'squeue' or option == 'sall':
		slurmOut += callCommand('squeue')
	if option == 'snodes' or option == 'sall':
		slurmOut += callCommand('scontrol -o show nodes')
	outputs["Result"]["value"] = slurmOut
	return zoo.SERVICE_SUCCEEDED
        
if __name__ == '__main__':
        slurmInfo()

