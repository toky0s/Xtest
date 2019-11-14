from tkinter import *
from body_exam import CenterExam


class FooterExam(Frame):

    def __init__(self, master, center_exam: CenterExam, **kw):
        super().__init__(master=master, **kw)
        self.center_exam = center_exam
        self.setupUI()

    def setupUI(self):
        self.previousButton = Button(self)
        self.previousButton['text'] = 'Previous'
        self.previousButton['command'] = self.center_exam.previousQuestion
        self.previousButton.pack(side='left')

        self.nextButton = Button(self)
        self.nextButton['text'] = 'Next'
        self.nextButton['command'] = self.center_exam.nextQuestion
        self.nextButton.pack(side='left')

        self.doneButton = Button(self)
        self.doneButton['text'] = 'Done'
        self.doneButton['command'] = self.center_exam.doneExam
        self.doneButton.pack(side='right')

        self.checkCurrentQuestion()

    def checkCurrentQuestion(self):
        '''Để vô hiệu previous button và next button'''
        # print(self.center_exam.current_question)
        if self.center_exam.current_question == 0:
            self.previousButton['state'] = 'disabled'
        elif self.center_exam.current_question > 0:
            if self.center_exam.current_question == len(self.center_exam.listQuestionObjects) -1:
                self.nextButton['state'] = 'disable'
                self.previousButton['state'] = 'normal'
            else:
                self.previousButton['state'] = 'normal'
                self.nextButton['state'] = 'normal'
        
        self.master.after(1, self.checkCurrentQuestion)
