import BlindSig as bs
import websocket
import thread
import time
import os
import hashlib
from tkinter import *

class poll:
    def __init__(self, ws):
        self.ws = ws
        self.signer = bs.Signer()
        self.publicKey = self.signer.getPublicKey()
        self.n = self.publicKey['n']
        self.e = self.publicKey['e']
        
    def poll_response(self, poll_answer, eligble_answer):
       
       if (poll_answer == 0): poll_answer = 2;
       if (eligble_answer == 0): eligble_answer = "n";
       if (eligble_answer == 1): eligble_answer = "y";
       
       voter = bs.Voter(self.n, eligble_answer)
       message = str(poll_answer) + str(voter.getID())
       message_hash = hashlib.sha256(message).hexdigest()
       message_hash = int(message_hash,16)
       blindMessage = voter.blindMessage(message_hash, self.n, self.e)
       self.ws.send("Blinded message: " + str(blindMessage))
       signedBlindMessage = self.signer.signMessage(blindMessage, voter.getEligibility())
       if signedBlindMessage == None:
           self.ws.send("INELIGIBLE VOTER....VOTE NOT AUTHORIZED!")
       else:
           self.ws.send("Signed blinded message: " + str(signedBlindMessage))
           signedMessage = voter.unwrapSignature(signedBlindMessage, self.n)
           decodedMessage = str(message)[0]
           verificationStatus = bs.verifySignature(message, signedMessage, self.e, self.n)
           self.ws.send("Signature: " + str(signedMessage))
           self.ws.send("Decoded message: " + str(decodedMessage))
           self.ws.send("Hashed message: " + str(hashlib.sha256(message).hexdigest()))
           self.ws.send("Verification status: " + str(verificationStatus))
       
       
class poll_machine:
    
    def __init__(self):
        self.ws = websocket.WebSocketApp("ws://localhost:8000",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.p = poll(self.ws)
        self.master = Tk()
        self.master.configure(background='yellow')
        self.var_poll = IntVar()
        self.var_answer = IntVar()
        
        self.question_poll = Label(self.master, text="Is Bitcoin cool?")
        self.yesBox_poll = Radiobutton(self.master, text="Yes", variable=self.var_poll, value=1)
        self.noBox_poll = Radiobutton(self.master, text="No", variable=self.var_poll, value=0)
        self.question_eligible = Label(self.master, text="Are you eligible to vote?")
        self.yesBox_eligible = Radiobutton(self.master, text="Yes", variable=self.var_answer, value=1)
        self.noBox_eligible = Radiobutton(self.master, text="No", variable=self.var_answer, value=0)
        self.submitButton = Button(self.master, text='Submit', command=self.make_vote)
        
        self.pollLabel = Label(self.master, text="Welcome to the Poll Booth")
        self.takePollButton = Button(self.master, text='Take Poll', command=self.reset_poll)
    def on_message(self,ws, message):
        pass
    
    def on_error(self,ws, error):
        print error

    def on_close(self,ws):
        print "### closed ###"

    def on_open(self,ws):
        self.master.wm_title("Election Poll Demo")
        self.master.geometry('200x200')
        self.pollLabel.grid(row=0, sticky=W, padx=10, pady=4)
        self.takePollButton.grid(row=1, sticky=W, padx=62)
        
        mainloop()
        
    def make_vote(self):
        self.p.poll_response(self.var_poll.get(),self.var_answer.get())
        self.question_poll.grid_remove()
        self.yesBox_poll.grid_remove()
        self.noBox_poll.grid_remove()
        self.question_eligible.grid_remove()
        self.yesBox_eligible.grid_remove()
        self.noBox_eligible.grid_remove()
        self.submitButton.grid_remove()
        
        if self.var_answer.get() == 0:
            root = Tk()
            root.wm_title("Unsuccessful Vote")
            root.geometry('200x100')
            label = Label(root, text="Please try again!").grid(row=0, sticky=W)
            root.configure(background='red')
        else:      
            root = Tk()
            root.wm_title("Successful Vote")
            root.geometry('200x100')
            label = Label(root, text="Thanks for voting!").grid(row=0, sticky=W)
            root.configure(background='green')
        
        self.pollLabel.grid(row=0, sticky=W, padx=10, pady=4)
        self.takePollButton.grid(row=1, sticky=W, padx=62)
        
        
    def reset_poll(self):
        
        self.question_poll.grid(row=0, sticky=W, padx=50, pady=4)
        self.yesBox_poll.grid(row=1, sticky=W, padx=75)
        self.noBox_poll.grid(row=2, sticky=W, padx=75)
        self.question_eligible.grid(row=3, sticky=W, padx=20, pady=4)
        self.yesBox_eligible.grid(row=4, sticky=W, padx=75)
        self.noBox_eligible.grid(row=5, sticky=W, padx=75)
        self.submitButton.grid(row=6, sticky=W, pady=4, padx=62)
        
        self.pollLabel.grid_remove()
        self.takePollButton.grid_remove()

    def main(self):    
        #websocket.enableTrace(True)
       
        self.ws.on_open = self.on_open
        self.ws.run_forever()
    
pm = poll_machine()
pm.main()


    







