from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []    


class SimpleChat(WebSocket):
    yes_num = 0
    no_num = 0
    
    def handleMessage(self):
       if "Decoded message" in self.data:
           answer = int(self.data[-1])
           if (answer == 1):
               SimpleChat.yes_num += 1
           else:
               SimpleChat.no_num += 1
          
       
       print(self.data)
       
       if "Verification" in self.data:
           print("")
           print("")
           print("")
           print("")
           print("------------------------------------------------------------------------               YES VOTES: " + str(SimpleChat.yes_num) + " NO VOTES: " + str(SimpleChat.no_num) + "               ---------------------------------------------------------------------------")
           print("")
           print("")
           print("")
           print("")
       
       for client in clients:
          if client != self:
             client.sendMessage(self.address[0] + u' - ' + self.data)

    def handleConnected(self):
       print(self.address, 'connected')
       for client in clients:
          client.sendMessage(self.address[0] + u' - connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, SimpleChat)
print("Public Polling Center Listener")
server.serveforever()