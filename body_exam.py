from tkinter import Tk, Radiobutton,Label, Frame, Button, PhotoImage, Canvas, Scrollbar
from tkinter.messagebox import askyesno, showwarning, showinfo
import os
import json
import string
from PIL import Image, ImageTk
from question import Question, Answer

def convertObject2Question(question_data, index):
    index = index
    content = question_data['question']
    images = question_data['images']
    answers = []
    for i in range(len(question_data['answers'])):
        answer = question_data['answers'][i]
        name = list(string.ascii_uppercase)[i]
        content_ans = answer['content']
        image_ans = answer['image']
        ans = Answer(name=name,content=content_ans, image=image_ans)
        answers.append(ans)
    return Question(index=index,content=content, images=images, answers=answers)

class ImageObject(Frame):

    def __init__(self, master, name:str, path:str, width:int, **kw):
        super().__init__(master=master)
        self.name = name
        self.path = path
        self.width = width
        self.setupUI()

    def setupUI(self):
        self.label_image = Label(self)
        self.image = Image.open(self.path)
        self.height = int(self.width*self.image.height/self.image.width)
        self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.photo = ImageTk.PhotoImage(self.image)

        self.image['image'] = self.photo
        self.image.image = self.photo
        self.image.pack()

        self.label_title = Label(self)
        self.label_title['text'] = self.name
        self.label_title['background'] = '#27ae60'
        self.label_title['foreground'] = 'white'
        self.label_title.pack(fill='x')


class ImageQuestionContainer(Frame):

    def __init__(self, master, images,**kw):
        super().__init__(master=master)
        self.master = master
        self.images = images
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
        for image in self.images:
            b = ImageObject(self.frame,name=image.name, path=image.path, width=self.winfo_width())
            b.pack(fill='x')

class CenterExam(Frame):
    # mac dinh data da duoc conver tu json sang object
    def __init__(self, master, **kw):
        super().__init__(master=master)
        self.master = master
        self.data = kw['data']

        # object to Question
        self.current_question = 0
        # contain Question objects
        self.listQuestionObjects = [convertObject2Question(question_data=question, index=index) for index,question in enumerate(self.data['questions'])]
        print(self.listQuestionObjects)
        self.setupUI()
#
    def setupUI(self):
        self.render(self.listQuestionObjects[0])

    def render(self, question:Question):
        # delete the previous question if any
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        
        # render question
        self.label_question = Label(self)
        self.label_question['text'] = str(question.index)+'. '+question.content
        self.label_question.pack(anchor='w')

        self.list_radiobutton = []
        for answer in question.answers:
            ans = Radiobutton(self)
            ans['text'] = answer.content
            ans['compound'] = 'left'
            ans['value'] = answer.name
            ans['variable'] = question.choice
            ans['command'] = self.setStateQuestionIsMark #test
            if os.path.exists(answer.image):
                i = Image.open(answer.image)
                photo = ImageTk.PhotoImage(i)
                ans['image'] = photo
                ans.image = photo
            self.list_radiobutton.append(ans)

        for radiobtt in self.list_radiobutton:
            radiobtt.pack(anchor='w')
        
        self.list_images_question = []
        for imageObject in question.images:
            if os.path.exists(imageObject.path):
                name = imageObject.name
                path = imageObject.path
                l = Label(self.master)
                image = Image.open(path)
                photo = ImageTk.PhotoImage(image)
                l['image'] = photo
                l.image = photo     
            else:
                name = imageObject.name
                l = Label(self, name)
            self.list_images_question.append(l)
        

        self.button_sure = Button(self)
        self.button_sure['text'] = 'Sure this question'
        icon_tick = PhotoImage(file='icon/tick-24.png')
        self.button_sure['image'] = icon_tick
        self.button_sure.image = icon_tick
        self.button_sure['compound'] = 'left'
        self.button_sure['command'] = self.setStateQuestionIsSure
        self.button_sure.pack()

        self.checkIsDisableQuestion()

    def showInfo(self, question: Question):
        print(question.index)
        print(question.content)
        print(question.images)
        print(question.answers)
        print(question.choice.get())
        print(question.state)

    def nextQuestion(self): # done
        self.current_question += 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def previousQuestion(self):
        self.current_question -= 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def allIsMark(self):
        '''If all question is mark, it will return True'''
        for question in self.listQuestionObjects:
            if question.state == 'no':
                return False
        return True

    def getAmountQuestionStateMark(self):
        return sum(question.state == 'mark' for question in self.listQuestionObjects)

    def getAmountQuestionStateNo(self):
        return sum(question.state == 'no' for question in self.listQuestionObjects)
        
    def getAmountQuestionStateDone(self):
        return sum(question.state == 'done' for question in self.listQuestionObjects)

    def checkValid(self):
        for question in self.listQuestionObjects:
            if question.state == 'no':
                showwarning('Warning', 'You have not completed some question!')
                return

        if self.allIsMark() or (self.getAmountQuestionStateMark() + self.getAmountQuestionStateDone() == len(self.listQuestionObjects) and self.getAmountQuestionStateMark() != 0):
            if askyesno('Warning','Do you want to Sure all and Finish this exam!'):
                for question in self.listQuestionObjects:
                    question.state = 'sure'
                self.doneExam()
            return

    def doneExam(self):
        # check all mark
        print('nop bai')
        # send data to server
        answers = [question.getAnswer() for question in self.listQuestionObjects]
        print(answers)
        self.master.quit()

    def timeOut(self):
        showinfo('Time out', 'Time out, your results will be sent to the server!')
        self.doneExam()

    def checkIsDisableQuestion(self):
        '''when this question was sure, it would disable the question'''
        if self.listQuestionObjects[self.current_question].state == 'sure':
            self.label_question['state'] = 'disabled'
            for radiobutton in self.list_radiobutton:
                radiobutton['state'] = 'disabled'
            self.button_sure['state'] = 'disabled'
        self.after(100, self.checkIsDisableQuestion)

    def setStateQuestionIsMark(self):
        print('change state')
        self.listQuestionObjects[self.current_question].changeState2Mark()

    def setStateQuestionIsSure(self):
        if self.listQuestionObjects[self.current_question].getAnswer() == '':
            showwarning('Warning', 'You have not answered this question!')
            return
        if askyesno('Sure this question','Are you sure?'):
            self.listQuestionObjects[self.current_question].changeState2Sure()


if __name__ == '__main__':
    with open('data_server_send.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
    master = Tk()
    a = CenterExam(master, data=data)
    a.pack(anchor='w')
    master.mainloop()