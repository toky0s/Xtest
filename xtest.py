from tkinter import *
import json
import time
import string
import os
from PIL import Image, ImageTk


class FrameGroupRadiobutton(Frame):

    def __init__(self, master=None, side='left', variable=None, dict_option={}, initialize="", callback=None):
        super().__init__(master=master)
        self.side = side
        self.variable = variable
        self.dict_option = dict_option
        self.initialize = initialize
        self.command = callback
        self.setupUI()

    def setupUI(self):

        self.variable.set(self.initialize)  # initialize
        for text, value in self.dict_option.items():
            radiobt_quality = Radiobutton(
                self, text=text, variable=self.variable, value=value, command=self.command)
            radiobt_quality.pack(side=self.side, anchor='w')


class InformationExam(Frame):

    def __init__(self, **kw):
        super().__init__(master=master)
        self.master = master
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
            print('time out')  # <======== callback
            return
        self.master.after(1000, self.countdown)


class Answer:

    def __init__(self, content, image=''):
        self.content = content
        self.image = image


class Question:

    # mac dinh json data da duoc convert sang object trong python
    def __init__(self, data):
        self.question = data['question']
        self.images = data['images']
        self.answers = data['answers']
        self.state = 'no'  # mark, sure, no

    def changeState2Mark(self):
        self.state = 'mark'

    def changeState2No(self):
        self.state = 'no'

    def changeState2Sure(self):
        self.state = 'sure'


class CenterExam(Frame):
    # mac dinh data da duoc conver tu json sang object
    def __init__(self, master, **kw):
        super().__init__(master=master)
        self.data = kw['data']

        self.data_client_edit = {}
        self.len_questions = len(self.data['questions'])

        self.data_client_edit['questions'] = []
        for i in range(self.len_questions):
            self.data_client_edit['questions'].append(
                {"state": "no", "answer": ""})

        self.data_questions_show = self.data['questions']
        self.setupUI()

    def setupUI(self):
        self.questionVar = StringVar()
        self.questionVar.set(self.data_questions_show[0]["question"])
        self.question = Label(self, textvariable=self.questionVar)
        self.question.pack(anchor='w')

        self.ticked = StringVar()
        for answer in self.data_questions_show[0]['answers']:
            ans_index = self.data_questions_show[0]['answers'].index(answer)
            names = tuple(string.ascii_uppercase)
            ans_name = names[ans_index]

            ans = Radiobutton(self)
            ans['text'] = answer['content']
            ans['variable'] = self.ticked
            ans['command'] = self.setStateQuestion
            ans['value'] = ans_name

            if answer['image'] != '' and os.path.exists(answer['image']):
                i = Image.open(answer['image'])
                photo = ImageTk.PhotoImage(i)
                ans['justify'] = 'left'
                ans.config(image=photo)
                ans.image = photo

            ans.pack(anchor='w')

    def write2File(self):
        pass

    def nextQuestion(self):
        print('cau tiep theo')

    def previousQuestion(self):
        print('cau truoc')

    def doneExam(self):
        print('nop bai')

    def getDataClientSend(self):
        return self.data_client_edit

    def setStateQuestion(self):
        print('choose')


class FooterExam(Frame):

    def __init__(self, master, previous_callback,  next_callback, done_callback, **kw):
        super().__init__(master=master, **kw)
        self.previousCallback = previous_callback
        self.nextCallback = next_callback
        self.doneCallback = done_callback
        self.setupUI()

    def setupUI(self):
        self.previousButton = Button(self)
        self.previousButton['text'] = 'Previous'
        self.previousButton['command'] = self.previousCallback
        self.previousButton.pack(side='left')

        self.nextButton = Button(self)
        self.nextButton['text'] = 'Next'
        self.nextButton['command'] = self.nextCallback
        self.nextButton.pack(side='left')

        self.doneButton = Button(self)
        self.doneButton['text'] = 'Done'
        self.doneButton['command'] = self.doneCallback
        self.doneButton.pack(side='right')


if __name__ == '__main__':
    with open('data_server_send.json', 'r') as f:
        data = json.load(f)
    master = Tk()
    info_exam = InformationExam(master=master, data=data)
    info_exam.pack()
    center_exam = CenterExam(master=master, data=data)
    center_exam.pack()
    footer_exam = FooterExam(master=master, previous_callback=center_exam.previousQuestion,
                             next_callback=center_exam.nextQuestion, done_callback=center_exam.doneExam)
    footer_exam.pack()
    master.mainloop()
