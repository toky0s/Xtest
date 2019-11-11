from tkinter import *

class InformationExam(Frame):

    def __init__(self, **kw):
        super().__init__(kw)
        self.question = kw['var_question']
        self.room = kw['var_room']
        self.date = kw['var_date']
        self.name = kw['var_name']
        self.id = kw['var_id']
        self.subject = kw['var_subject']
        self.time = kw['var_time']
        self.setupUI()

    def setupUI(self):
        self.numberQuestion = Label(self, textvariable=self.question)
        self.numberQuestion.pack(side='left')

        self.testRoom = Label(self, textvariable=self.room)
        self.testRoom.pack(side='left')
        
        self.testDate = Label(self, textvariable=self.date)
        self.testDate.pack(side='left')

        self.studentName = Label(self, textvariable=self.name)
        self.studentName.pack(side='left')

        self.studentId = Label(self, textvariable=self.id)
        self.studentId.pack(side='left')

        self.testSubject = Label(self, textvariable=self.subject)
        self.testSubject.pack(side='left')

        self.testTime = Label(self, textvariable=self.time)
        self.testTime.pack(side='left')

class CenterExam(Frame):
    
    def __init__(self, master,**kw):
        super().__init__(master=master)
        self.questionData = kw['var_json'] # list of json objects
        self.questions = self.questionData['question']
        self.answers = self.questionData['answers']
        self.images = self.questionData['images']
        self.answerFile = kw['var_path']
        self.setupUI()

    def setupUI(self):
        self.question = Label(self, )

    def write2File(self):
        pass

    def nextQuestion(self):
        pass

    def previousQuestion(self):
        pass
