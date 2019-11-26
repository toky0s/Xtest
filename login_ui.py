from tkinter import Tk, StringVar
from tkinter.ttk import Button, Label, Entry, Frame
import logging
class LoginFrame(Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master=master)
        self.setupUI()

    def setupUI(self):
        self.label_title = Label(self)
        self.label_title['text']='Login'
        self.label_title.grid(row=0, column =0, columnspan=2)

        self.label_username = Label(self)
        self.label_username['text'] = 'Username:'
        self.label_username.grid(row=1, column =0, sticky='w')

        self.label_password = Label(self)
        self.label_password['text'] = 'Password:'
        self.label_password.grid(row=2, column =0, sticky='w')


        self.var_username = StringVar()
        self.text_username = Entry(self)
        self.text_username['textvariable'] = self.var_username
        self.text_username.grid(row=1, column =1)

        self.var_password = StringVar()
        self.text_password = Entry(self)
        self.text_password['show'] = '*'
        self.text_password['textvariable'] = self.var_password
        self.text_password.grid(row=2, column =1)

        self.label_noti = Label(self)
        self.label_noti['text'] = ''
        self.label_noti.grid(row=3, column =0)

        self.btt_login = Button(self)
        self.btt_login['text'] = 'login'
        self.btt_login['command'] = self.login
        self.btt_login.grid(row=4, column =0, columnspan=2)

    def login(self):
        # send this to server
        print(self.var_username.get())
        print(self.var_password.get())

if __name__ == '__main__':
    master = Tk()
    LoginFrame(master=master).pack()
    master.mainloop()