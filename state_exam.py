from tkinter import Canvas, Button, Label, Frame, Tk, Scrollbar, PhotoImage
from tkinter.ttk import  Button, Label, Frame, Scrollbar
from question import Question
from center_exam import CenterExam
from footer_exam import FooterExam

class StatusButton(Frame):

    def __init__(self, master, question: Question, center_exam:CenterExam, footer_exam: FooterExam, **kw):
        super().__init__(master=master)
        self.master = master
        self.question = question
        self.center_exam = center_exam
        self.footer_exam = footer_exam
        self.icons = {'no':'icon/question-24.png','mark':'icon/flag.png','sure':'icon/tick-24.png'}
        self.setupUI()

    def setupUI(self):
        # this frame
        self['relief'] = 'raised'
        self['borderwidth'] = 1
        self.bind('<Button-1>', self.gotoQuestion)
        self.bind('<ButtonRelease-1>', self.releaseMouse)

        self.index = Label(self)
        self.index['text'] = self.question.index
        self.index.grid(row=0, column=0)
        self.index.bind('<Button-1>', self.gotoQuestion)
        self.index.bind('<ButtonRelease-1>', self.releaseMouse)

        self.answer = Label(self)
        self.answer['text'] = self.question.getAnswer()
        self.answer.grid(row=0, column=1)
        self.answer.bind('<Button-1>', self.gotoQuestion)
        self.answer.bind('<ButtonRelease-1>', self.releaseMouse)

        self.icons = {'no':'icon/question-24.png','mark':'icon/flag.png','sure':'icon/tick-24.png'}

        self.statusIcon = Label(self)
        self.photo = PhotoImage(file=self.icons[self.question.state])
        self.statusIcon['image'] = self.photo
        self.statusIcon.image = self.photo
        self.statusIcon.grid(row=0, column=2)
        self.statusIcon.bind('<Button-1>', self.gotoQuestion)
        self.statusIcon.bind('<ButtonRelease-1>', self.releaseMouse)

    def gotoQuestion(self,event):
        # check question before goto and disable next and previous button
        if self.question.index == 0:
            self.footer_exam.previousButton['state'] = 'disabled'
            self.footer_exam.nextButton['state'] = 'normal'
        elif self.question.index == self.center_exam.getAmountQuestion() -1:
            self.footer_exam.nextButton['state'] = 'disabled'
            self.footer_exam.previousButton['state'] = 'normal'

        else:
            self.footer_exam.previousButton['state'] = 'normal'
            self.footer_exam.nextButton['state'] = 'normal'

        # check if the current question == question -> Do not render()
        if self.center_exam.current_question == self.question.index:
            return

        self['relief'] = 'groove'
        self.center_exam.current_question=self.question.index
        self.center_exam.render(self.question)

    def change2Mark(self):
        self.answer['text'] = self.question.getAnswer()
        photo = PhotoImage(file=self.icons[self.question.state])
        self.statusIcon['image'] = photo
        self.statusIcon.image = photo

    def change2Sure(self):
        photo = PhotoImage(file=self.icons[self.question.state])
        self.statusIcon['image'] = photo
        self.statusIcon.image = photo


    def releaseMouse(self, event):
        self['relief'] = 'raised'

class StateExam(Frame):

    def __init__(self, master, center_exam: CenterExam, footer_exam: FooterExam, **kw):
        super().__init__(master=master)
        self.master = master
        self.center_exam = center_exam
        self.footer_exam = footer_exam
        self.setupUI()

    def setupUI(self):
        self.canvas = Canvas(self)

        self.scrollbar = Scrollbar(self)
        self.scrollbar['orient'] = 'vertical'
        self.scrollbar['command'] = self.canvas.yview
        self.scrollbar.pack(side='right', fill='y')

        self.canvas['yscrollcommand'] = self.scrollbar.set
        self.canvas.pack(side='left')

        self.frame = Frame(self.canvas)
        self.frame.bind("<Configure>",self.resizeCanvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='center')
        self.addStatusButton()

    def resizeCanvas(self,event):
        self.canvas['scrollregion'] = self.canvas.bbox('all') # width button inside and height is center_exam's height
        self.canvas['width'] = event.width
        self.canvas['height'] = 150

    def addStatusButton(self):
        self.listStateButton = []
        for question in self.center_exam.listQuestionObjects:
            b = StatusButton(self.frame,question, center_exam=self.center_exam,footer_exam= self.footer_exam)
            self.listStateButton.append(b)
            b.pack(fill='x')

    def checkQuestionState(self):
        '''continuously check the status of questions to display the appropriate icon'''
        self.icons = {'no':'icon/question-24.png','mark':'icon/flag.png','sure':'icon/tick-24.png'}
        while True:
            for b in self.listStateButton:
                b.answer['text'] = b.question.getAnswer()
                photo = PhotoImage(file=self.icons[b.question.state])
                b.statusIcon['image'] = photo
                b.statusIcon.image = photo
        
