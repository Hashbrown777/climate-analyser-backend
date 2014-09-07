import rsa
import urllib
import zoo
import base64

def ChangeDjango(conf,inputs,outputs):
	crypto = inputs["url"]["value"]
	
	privatefile = open('rsa/privateKey.pem')
	keydata = privatefile.read()
	privatekey = rsa.PrivateKey.load_pkcs1(keydata)
	unquote = urllib.unquote(base64.b64decode(crypto))
	#try:
	newurl = rsa.decrypt(unquote,privatekey)
	#except:
	#	conf["lenv"]["message"] = str(inputs)
	#        return zoo.SERVICE_FAILED

	DjangoServer = open('DjangoServer','w')
	DjangoServer.write(newurl)

	return zoo.SERVICE_SUCCEEDED
