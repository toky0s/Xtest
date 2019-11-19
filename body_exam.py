from tkinter import Tk, Radiobutton, Label, Frame, Button, PhotoImage, Canvas, Scrollbar
from tkinter.messagebox import askyesno, showwarning, showinfo
import os
import json
import string
from PIL import Image, ImageTk
from question import Question, Answer
import logging

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
        ans = Answer(name=name, content=content_ans, image=image_ans)
        answers.append(ans)
    return Question(index=index, content=content, images=images, answers=answers)


class ImageObject(Frame):

    def __init__(self, master, name: str, path: str, width: int, **kw):
        super().__init__(master=master)
        self.name = name
        self.path = path
        self.width = width
        self.setupUI()

    def setupUI(self):
        self.label_image = Label(self)

        self.image_f = Image.open(self.path)
        self.height = int(self.width*self.image_f.height/self.image_f.width)
        # The (250, 250) is (height, width)
        self.image = self.image_f.resize(
            (self.width, self.height), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(self.image)
        self.label_image['image'] = self.photo
        self.label_image.image = self.photo
        self.label_image.pack()

        self.label_title = Label(self)
        self.label_title['text'] = self.name
        self.label_title['background'] = '#27ae60'
        self.label_title['foreground'] = 'white'
        self.label_title.pack(fill='x')


class ImageQuestionContainer(Frame):
    '''this class will contain images of question'''

    def __init__(self, master, images: list, **kw):
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
        self.frame.bind("<Configure>", self.resizeCanvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='center')
        self.addStatusButton()

    def resizeCanvas(self, event):
        # width button inside and height is center_exam's height
        self.canvas['scrollregion'] = self.canvas.bbox('all')
        self.canvas['width'] = event.width
        self.canvas['height'] = 150

    def addStatusButton(self):
        for image in self.images:
            b = ImageObject(self.frame, name=image['name'], path=image['path'], width=500)
            b.pack(fill='x')


class CenterExam(Frame):
    '''this frame contain questions and render them'''
    # mac dinh data da duoc conver tu json sang object

    def __init__(self, master, **kw):
        super().__init__(master=master)
        self.master = master
        self.data = kw['data']

        # object to Question
        self.current_question = 0
        # contain Question objects
        self.listQuestionObjects = [convertObject2Question(question_data=question, index=index) for index, question in enumerate(self.data['questions'])]
        logging.info(self.listQuestionObjects)
        self.setupUI()

    def setupUI(self):
        self.render(self.listQuestionObjects[0])

    def render(self, question: Question):
        '''render the question object'''
        # delete the previous question if any
        self.listWidgets = self.grid_slaves()
        for widget in self.listWidgets:
            widget.destroy()

        # render question
        self.label_question = Label(self)
        self.label_question['text'] = str(question.index)+'. '+question.content
        self.label_question.grid(row=0, column=0, sticky='w')

        # get list of answers
        self.list_radiobutton = []
        print(question.answers)
        for answer in question.answers:
            ans = Radiobutton(self)
            ans['text'] = answer.content
            ans['compound'] = 'bottom'
            ans['value'] = answer.name
            ans['variable'] = question.choice
            ans['command'] = self.setStateQuestionIsMark  # test
            if os.path.exists(answer.image):
                i = Image.open(answer.image)
                width = 100
                height = int(width*i.height/i.width)
                # The (250, 250) is (height, width)
                i = i.resize((width, height), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(i)
                ans['image'] = photo
                ans.image = photo
            self.list_radiobutton.append(ans)

        # render answers
        for i in range(len(self.list_radiobutton)):
            # +1 because question's row is 0
            self.list_radiobutton[i].grid(row=i+1, column=0, sticky='w')

        # render frame which contains images of question
        # logging.info(self.allIs(True,[os.path.exists(i['path']) for i in question.images]))
        if self.allIs(True,[os.path.exists(i['path']) for i in question.images]):
            self.frame_images_of_question = ImageQuestionContainer(self, question.images)
            location_column_frame_images_of_question = len(self.grid_slaves())
            self.frame_images_of_question.grid(row=0, column=1, rowspan=location_column_frame_images_of_question)

        self.button_sure = Button(self)
        self.button_sure['text'] = 'Sure this question'

        icon_tick = PhotoImage(file='icon/tick-24.png')
        self.button_sure['image'] = icon_tick
        self.button_sure.image = icon_tick
        self.button_sure['compound'] = 'left'
        self.button_sure['command'] = self.setStateQuestionIsSure

        # determind location of sure button, this button will be end of the frame
        location_row = len(self.grid_slaves())
        self.button_sure.grid(row=location_row, column=0)

        # check question was sure, didn't
        self.checkIsDisableQuestion()

    def showInfo(self, question: Question):
        print(question.index)
        print(question.content)
        print(question.images)
        print(question.answers)
        print(question.choice.get())
        print(question.state)

    def nextQuestion(self):  # done
        logging.info('next question')
        self.current_question += 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def previousQuestion(self):
        logging.info('previous question')
        self.current_question -= 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def allIs(self, value, can_loop):
        '''If all question is mark, it will return True'''
        for i in can_loop:
            print('ok',i)
            if i != value:
                return False
        return True

    def getAmountQuestionStateMark(self):
        return sum(question.state == 'mark' for question in self.listQuestionObjects)

    def getAmountQuestionStateNo(self):
        return sum(question.state == 'no' for question in self.listQuestionObjects)

    def getAmountQuestionStateDone(self):
        return sum(question.state == 'done' for question in self.listQuestionObjects)

    def checkValid(self):
        logging.info('check valid exam')
        for question in self.listQuestionObjects:
            if question.state == 'no':
                showwarning('Warning', 'You have not completed some question!')
                return

        # check all is mark or mark + sure = totalAmountQuestion
        all_is_mark = self.allIs('mark', [i.state for i in self.listQuestionObjects])
        all_is_mark_or_and_sure = self.getAmountQuestionStateMark() + self.getAmountQuestionStateDone() == len(self.listQuestionObjects) and self.getAmountQuestionStateMark() != 0
        if all_is_mark or all_is_mark_or_and_sure:
            if askyesno('Warning', 'Do you want to Sure all and Finish this exam!'):
                for question in self.listQuestionObjects:
                    question.state = 'sure'
                self.doneExam()
            return

    def doneExam(self):
        # send data to server
        answers = [question.getAnswer() for question in self.listQuestionObjects]
        logging.info(f'Done exam {answers}')
        self.master.quit()

    def timeOut(self):
        logging.info('Time out, your results will be sent to the server!')
        self.doneExam()

    def checkIsDisableQuestion(self):
        '''when this question was sure, it would disable the question'''
        if self.listQuestionObjects[self.current_question].state == 'sure':
            logging.info(f'Disable question {self.listQuestionObjects[self.current_question]}')
            self.label_question['state'] = 'disabled'
            for radiobutton in self.list_radiobutton:
                radiobutton['state'] = 'disabled'
            self.button_sure['state'] = 'disabled'
        self.after(100, self.checkIsDisableQuestion)

    def setStateQuestionIsMark(self):
        logging.info(f'change the state of question {self.listQuestionObjects[self.current_question]} to MARK')
        self.listQuestionObjects[self.current_question].changeState2Mark()

    def setStateQuestionIsSure(self):
        if self.listQuestionObjects[self.current_question].getAnswer() == '':
            showwarning('Warning', 'You have not answered this question!')
            return
        if askyesno('Sure this question', 'Are you sure?'):
            logging.info(f'change the state of question {self.listQuestionObjects[self.current_question]} to SURE')
            self.listQuestionObjects[self.current_question].changeState2Sure()


if __name__ == '__main__':
    with open('data_server_send.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    master = Tk()
    a = CenterExam(master, data=data)
    a.pack(anchor='w')
    master.mainloop()
