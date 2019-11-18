from tkinter import Frame, Label, StringVar
from body_exam import CenterExam

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
        self.currentQuestionVar = StringVar()
        self.currentQuestionVar.set(f'1/{self.numberQuestion}')
        self.currentQuestion = Label(
            self, textvariable=self.currentQuestionVar)
        self.currentQuestion.pack(side='left')

        self.testRoom = Label(self, text=self.room)
        self.testRoom.pack(side='left')

        self.testDate = Label(self, text=self.date)
        self.testDate.pack(side='left')

        self.studentName = Label(self, text=self.name)
        self.studentName.pack(side='left')

        self.studentId = Label(self, text=self.id)
        self.studentId.pack(side='left')

        self.testSubject = Label(self, text=self.subject)
        self.testSubject.pack(side='left')

        self.timeVar = StringVar()
        self.testTime = Label(self, textvariable=self.timeVar)
        self.testTime.pack(side='left')

        self.countdown()

    def countdown(self):
        self.time -= 1
        mins, secs = divmod(self.time, 60)
        self.timeVar.set('{:02d}:{:02d}'.format(mins, secs))
        if self.time == 0:
            self.center_exam.timeOut()  # <======== callback
            return
        self.master.after(1000, self.countdown)
