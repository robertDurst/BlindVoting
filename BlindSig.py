import cryptomath, random, hashlib

class Signer:
    
    def __init__(self):
        self.publicKey, self.privateKey = (self.generateInformation())
    
    def generateInformation(self):
        # Generates public and private keys and saves them to a file.
        p = cryptomath.findPrime()
        q = cryptomath.findPrime()
        phi = (p - 1)*(q - 1)
        n = p*q
    
    
        foundEncryptionKey = False
        while not foundEncryptionKey:
            e = random.randint(2, phi - 1)
            if cryptomath.gcd(e, phi) == 1:
                foundEncryptionKey = True
    
        d = cryptomath.findModInverse(e, phi)
   
        publicInfo = {"n" : n, "e": e}
        privateInfo = {"n" : n, "d": d}
    
        return[(publicInfo),(privateInfo)]
        
    def getPublicKey(self):
        return self.publicKey
    
    def signMessage(self, message, eligible):
        if eligible == "y":
            return pow(message, self.privateKey['d'], self.publicKey['n'])
        else:
            return None
        
    def verifyVoter(self, eligible):
        pass
        
 
class Voter:
    def __init__(self, n, eligible):
        self.eligible = eligible
        
        foundR = False
        while not foundR:
            self.r = random.randint(2, n - 1)
            if cryptomath.gcd(self.r, n) == 1:
                foundR = True
        
    def blindMessage(self, m, n, e):
         
         blindMessage = (m * pow(self.r,e,n)) % n
         
         return blindMessage
         
    def unwrapSignature(self, signedBlindMessage, n):
        rInv = cryptomath.findModInverse(self.r, n)
        
        return ((signedBlindMessage * rInv) % n)
    
    def getEligibility(self):
        return self.eligible

def verifySignature(message, randNum, signature, publicE, publicN):
    return (int(hashlib.sha256(str(message) + str(randNum)).hexdigest(),16) == pow(signature, publicE, publicN))        
        

