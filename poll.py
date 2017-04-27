import BlindSig as bs
import websocket
import thread
import time
import os
import hashlib

class poll:
    def __init__(self):
        self.signer = bs.Signer()
        self.publicKey = self.signer.getPublicKey()
        self.n = self.publicKey['n']
        self.e = self.publicKey['e']
        
    def begin_poll(self, question):
        
        polling = True       
        
        while(polling):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Welcome to the Poll!")
            print("")
            voter_response_1 = raw_input(str(question) + " (y/n): ")
            voter_response_2 = raw_input("Are you an eligible voter (y/n): ")
            voter_response_3 = raw_input("Submit now (y/n): ")
            if (voter_response_3.lower() == "y"):
                if (voter_response_1.lower() == "y"):
                    voter = bs.Voter(self.n, voter_response_2.lower())
                    message = str(1) + str(voter.getID())
                    message_hash = hashlib.sha256(message).hexdigest()
                    print(message_hash)
                    message_hash = int(message_hash,16)
                    blindMessage = voter.blindMessage(message_hash, self.n, self.e)
                    ws.send("Blinded message: " + str(blindMessage))
                    signedBlindMessage = self.signer.signMessage(blindMessage, voter.getEligibility())
                    if signedBlindMessage == None:
                        ws.send("INELIGIBLE VOTER....VOTE NOT AUTHORIZED!")
                        print("")
                        print("ERROR INELIGIBLE VOTER!")
                    else:
                        ws.send("Signed blinded message: " + str(signedBlindMessage))
                        signedMessage = voter.unwrapSignature(signedBlindMessage, self.n)
                        decodedMessage = str(message)[0]
                        verificationStatus = bs.verifySignature(message, signedMessage, self.e, self.n)
                        ws.send("Signature: " + str(signedMessage))
                        ws.send("Decoded message: " + str(decodedMessage))
                        ws.send("Hashed message: " + str(hashlib.sha256(message).hexdigest()))
                        ws.send("Verification status: " + str(verificationStatus))
                        print("")
                        print("Thanks your vote has been submitted!")
                elif (voter_response_1.lower() == "n"):
                    voter = bs.Voter(self.n, voter_response_2.lower())
                    message = str(0) + str(voter.getID())
                    message_hash = hashlib.sha256(message).hexdigest()
                    print(message_hash)
                    message_hash = int(message_hash,16)
                    blindMessage = voter.blindMessage(message_hash, self.n, self.e)
                    ws.send("Blinded message: " + str(blindMessage))
                    signedBlindMessage = self.signer.signMessage(blindMessage, voter.getEligibility())
                    if signedBlindMessage == None:
                        ws.send("INELIGIBLE VOTER....VOTE NOT AUTHORIZED!")
                        print("")
                        print("ERROR INELIGIBLE VOTER!")
                    else:
                        ws.send("Signed blinded message: " + str(signedBlindMessage))
                        signedMessage = voter.unwrapSignature(signedBlindMessage, self.n)
                        decodedMessage = str(message)[0]
                        verificationStatus = bs.verifySignature(message, signedMessage, self.e, self.n)
                        ws.send("Signature: " + str(signedMessage))
                        ws.send("Decoded message: " + str(decodedMessage))
                        ws.send("Hashed message: " + str(hashlib.sha256(message).hexdigest()))
                        ws.send("Verification status: " + str(verificationStatus))
                        print("")
                        print("Thanks your vote has been submitted!")
            else:
                polling = False
            
            
            time.sleep(3)
        print("")
        print("SYSTEM CLOSING...")     
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
    


    







