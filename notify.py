def send(djangoAddr,jobid,status):
	publicfile = open('publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	wCall = djangoAddr + '/update_computation_status?id='
	wCall += encryptField(pubkey,jobid)
	wCall += '&status='
	wCall += encryptField(pubkey,status)
	urllib.urlopen(wCall)
