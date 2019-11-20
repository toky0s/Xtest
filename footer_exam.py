from tkinter import Button, Frame
from tkinter.ttk import Button, Frame
from body_exam import CenterExam
import logging


class FooterExam(Frame):

    def __init__(self, master, center_exam: CenterExam, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.center_exam = center_exam
        self.setupUI()

    def setupUI(self):
        self.previousButton = Button(self)
        self.previousButton['text'] = 'Previous'
        self.previousButton['command'] = self.center_exam.previousQuestion
        self.previousButton.pack(side='left')


        self.nextButton = Button(self)
        self.nextButton['text'] = 'Next'
        self.nextButton['command'] = self.beforeCallNextQuestion#self.center_exam.nextQuestion        
        self.nextButton.pack(side='left')

        self.doneButton = Button(self)
        self.doneButton['text'] = 'Done'
        self.doneButton['command'] = self.beforeCallPreviousQuestion
        self.doneButton.pack(side='right')

        self.checkCurrentQuestion()

    def beforeCallNextQuestion(self):
        if self.center_exam.current_question + 1 == self.center_exam.getAmountQuestion()-1:
            # disable the next question button/bind

            pass
        pass

    def beforeCallPreviousQuestion(self):
        if self.center_exam.current_question - 1 == 0:
            # disable the previous question button/bind
            self.nextButton['state'] = 'normal'
            self.master.bind('<Right>', lambda event: self.center_exam.nextQuestion())
            self.master.unbind('<Left>')
            self.previousButton['state'] = 'disabled'
        

    def checkCurrentQuestion(self):
        '''Để vô hiệu previous button và next button khi ở đầu và cuối câu hỏi'''
        if self.center_exam.current_question == 0:
            self.nextButton['state'] = 'normal'
            self.master.bind('<Right>', lambda event: self.center_exam.nextQuestion())
            self.master.unbind('<Left>')
            self.previousButton['state'] = 'disabled'
        elif self.center_exam.current_question > 0:
            if self.center_exam.current_question == len(self.center_exam.listQuestionObjects) -1:
                self.master.unbind('<Right>')
                self.nextButton['state'] = 'disable'
                self.previousButton['state'] = 'normal'
            else:
                self.previousButton['state'] = 'normal'
                self.master.bind('<Left>', lambda event: self.center_exam.previousQuestion())
                self.nextButton['state'] = 'normal'
        
        self.after(1000, self.checkCurrentQuestion)
