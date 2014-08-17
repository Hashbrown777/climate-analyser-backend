import rsa

def main():
	test = "http://115.146.84.143:8080"
	privatefile = open('privateKey.pem')
	keydata = privatefile.read()
	privatekey = rsa.PrivateKey.load_pkcs1(keydata)
	publicfile = open('publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	signature = rsa.sign(test, privatekey, 'SHA-1')	

	print rsa.verify(test, signature, pubkey)
	print signature
