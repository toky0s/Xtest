from tkinter import StringVar
from tkinter.ttk import Frame, Label
from center_exam import CenterExam
import time

class InformationExam(Frame):

    def __init__(self, master, center_exam:CenterExam,**kw):
        super().__init__(master=master)
        self.master = master
        self.center_exam = center_exam
        self.data = kw['data']
        self.data['questions']
        self.numberQuestion = len(self.data['questions'])
        self.room = self.data['informations']['room']
        self.date = self.data['informations']['date']
        self.name = self.data['informations']['name']
        self.id = self.data['informations']['id']
        self.subject = self.data['informations']['subject']
        self.time = self.data['informations']['time']
        self.time = int(self.time)
        self.setupUI()

    def setupUI(self):
        self.currentQuestion = Label(self)
        self.currentQuestion['text'] = f'Số câu hỏi: {self.center_exam.getAmountQuestion()}'
        self.currentQuestion.grid(column=0, row=0)

        self.testRoom = Label(self, text=self.room)
        self.testRoom.grid(column=1, row=0)

        self.testDate = Label(self, text=self.date)
        self.testDate.grid(column=2, row=0)

        self.studentName = Label(self, text=self.name)
        self.studentName.grid(column=3, row=0)

        self.studentId = Label(self, text=self.id)
        self.studentId.grid(column=4, row=0)

        self.testSubject = Label(self, text=self.subject)
        self.testSubject.grid(column=5, row=0)

        self.timeVar = StringVar()
        self.testTime = Label(self, textvariable=self.timeVar)
        self.testTime.grid(column=6, row=0)

        # self.countdown()

    def countdown(self):
        '''Start countdown'''
        while self.time>=0:
            mins, secs = divmod(self.time, 60)
            self.timeVar.set('{:02d}:{:02d}'.format(mins, secs))
            time.sleep(1)
            self.time -= 1

        self.center_exam.doneExam()

        # self.master.after(1000, self.countdown)
