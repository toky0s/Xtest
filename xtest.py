from tkinter import *
import json
import time
import string
import os
from PIL import Image, ImageTk


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
        self.master = master
        self.data = kw['data']

        self.data_client_edit = {}
        self.len_questions = len(self.data['questions'])

        self.data_client_edit['questions'] = [{"state": "no", "answer": ""}]
        self.data_client_edit['questions'] *= self.len_questions

        self.data_questions_show = self.data['questions'] #contain list question

        self.current_question = 0
        self.setupUI()

    def setupUI(self):
        self.questionVar = StringVar()
        self.questionVar.set(self.data_questions_show[0]["question"])

        self.question = Label(self)
        self.question['textvariable'] = self.questionVar
        self.question.pack(anchor='w')

        self.ticked = StringVar()
        self.listAnswersRadiobutton = [] # [<ans radiobutton obj>, <ans radiobutton obj>,...]
        self.listTextVariable = []
        for answer in self.data_questions_show[0]['answers']:
            ans_index = self.data_questions_show[0]['answers'].index(answer)
            names = tuple(string.ascii_uppercase)
            ans_name = names[ans_index]

            ans = Radiobutton(self)

            textvar = StringVar()
            textvar.set(answer['content'])
            self.listTextVariable.append(textvar)

            ans['textvariable'] = textvar
            ans['variable'] = self.ticked
            ans['command'] = self.setStateQuestion
            ans['value'] = ans_name

            # add image for answer
            if answer['image'] != '' and os.path.exists(answer['image']):
                i = Image.open(answer['image'])
                photo = ImageTk.PhotoImage(i)
                ans['justify'] = 'left'
                ans.config(image=photo)
                ans.image = photo

            self.listAnswersRadiobutton.append(ans)

        for i in self.listAnswersRadiobutton:
            i.pack(anchor='w')

    def write2File(self):
        pass

    def nextQuestion(self):
        '''Chuyển sang câu hỏi tiếp theo'''
        print('cau tiep theo')
        self.current_question += 1
        self.questionVar.set(self.data_questions_show[self.current_question]['question'])
        amountAnswer = len(self.data_questions_show[self.current_question]['answers'])

        for i in range(amountAnswer):
            if len(self.listAnswersRadiobutton) == i:
                ansAddVar = StringVar()
                ansAddVar.set(self.data_questions_show[self.current_question]['answers'][i]['content'])
                ansAdd = Radiobutton(self)
                ansAdd['textvariable'] = ansAddVar
                ansAdd['value'] = tuple(string.ascii_uppercase)[i]
                ansAdd['variable'] = self.ticked
                ansAdd['command'] = self.setStateQuestion

                self.listTextVariable.append(ansAddVar)
                self.listAnswersRadiobutton.append(ansAdd)

                ansAdd.pack(anchor='w')
                pass # toi cau hoi co do so luong cau tra loi nhieu hon hoac it hon
            else:
                ans = self.data_questions_show[self.current_question]['answers'][i]
                self.listTextVariable[i].set(ans['content'])
                if ans['image'] != '' and os.path.exists(ans['image']):
                    i = Image.open(ans['image'])
                    photo = ImageTk.PhotoImage(i)
                    self.listAnswersRadiobutton['image'] = photo
                    self.image = photo




    def previousQuestion(self):
        print('cau truoc')
        self.current_question -=1

    def doneExam(self):
        print('nop bai')
        self.master.quit()

    def sendData2Server(self):
        return self.data_client_edit

    def setStateQuestion(self):
        '''Thay đổi trạng thái của câu hỏi'''
        print(self.ticked.get())


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
    with open('data_server_send.json', 'r',encoding='utf-8') as f:
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
