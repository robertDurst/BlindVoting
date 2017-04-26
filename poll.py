import BlindSig as bs
import websocket
import thread
import time

class poll:
    def __init__(self):
        self.signer = bs.Signer()
        self.publicKey = self.signer.getPublicKey()
        self.n = self.publicKey['n']
        self.e = self.publicKey['e']
        
    def begin_poll(self, question):
        polling = True
        
        print("Welcome to the Poll!")
        #print("public mod: ", self.n)
        #print("public exponent: ", self.e)
        print("")
        
        
        while(polling):
            
            voter_response = raw_input(str(question) + " (y/n): ")
            if (voter_response.lower() == "y"):
                voter = bs.Voter(self.n)
                message = str(1) + str(voter.getID())
                message = int(message)
                blindMessage = voter.blindMessage(message, self.n, self.e)
                ws.send("")
                ws.send("Blinded message: " + str(blindMessage))
                signedBlindMessage = self.signer.signMessage(blindMessage)
                ws.send("")
                ws.send("Signed blinded message: " + str(signedBlindMessage))
                signedMessage = voter.unwrapSignature(signedBlindMessage, self.n)
                decodedMessage = pow(signedMessage, self.e, self.n)
                verificationStatus = bs.verifySignature(decodedMessage, signedMessage, self.e, self.n)
                plaintextMessage = str(decodedMessage)[0:1]
                ws.send("")
                ws.send("Signature: " + str(signedMessage))
                ws.send("Decoded message: " + str(plaintextMessage))
                ws.send("Verification status: " + str(verificationStatus))
            elif (voter_response.lower() == "n"):
                voter = bs.Voter(self.n)
                message = str(2) + str(voter.getID())
                message = int(message)
                blindMessage = voter.blindMessage(message, self.n, self.e)
                ws.send("")
                ws.send("Blinded message: " + str(blindMessage))
                signedBlindMessage = self.signer.signMessage(blindMessage)
                ws.send("")
                ws.send("Signed blinded message: " + str(signedBlindMessage))
                signedMessage = voter.unwrapSignature(signedBlindMessage, self.n)
                decodedMessage = pow(signedMessage, self.e, self.n)
                verificationStatus = bs.verifySignature(decodedMessage, signedMessage, self.e, self.n)
                plaintextMessage = str(decodedMessage)[0:1]
                ws.send("")
                ws.send("Signature: " + str(signedMessage))
                ws.send("Decoded message: " + str(plaintextMessage))
                ws.send("Verification status: " + str(verificationStatus))
            else:
                polling = False
                
        ws.close() 
      


def on_message(ws, message):
    pass
    
def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        p = poll()
        p.begin_poll("Is Bitcoin cool?")
    thread.start_new_thread(run, ())


#websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://localhost:8000",
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
ws.on_open = on_open
ws.run_forever()
    


    







