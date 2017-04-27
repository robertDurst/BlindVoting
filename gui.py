from tkinter import *
master = Tk()
master.wm_title("Election Poll Demo")
master.geometry('200x100') # Size 200, 200

def var_states():
   print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))

question = Label(master, text="Is Bitcoin cool?").grid(row=0, sticky=W, padx=50)
var1 = IntVar()
yesBox = Checkbutton(master, text="Yes", variable=var1).grid(row=1, sticky=W, padx=75)
var2 = IntVar()
noBox = Checkbutton(master, text="No", variable=var2).grid(row=2, sticky=W, padx=75)
submitButton = Button(master, text='Submit', command=var_states).grid(row=3, sticky=W, pady=4, padx=65)
mainloop()