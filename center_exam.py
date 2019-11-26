from tkinter import Tk, Radiobutton, Label, Frame, Button, PhotoImage, Canvas, Scrollbar
from tkinter.ttk import Radiobutton, Label, Frame, Button, Scrollbar
from tkinter.messagebox import askyesno, showwarning, showinfo
from PIL import Image, ImageTk
from question import Question, Answer, convertObject2Question
import os
import json
import string
import logging


class ImageObject(Frame):

    def __init__(self, master,name: str, path: str, width: int, **kw):
        super().__init__(master=master, **kw)
        self.name = name
        self.path = path
        self.width = width
        self.setupUI()

    def setupUI(self):
        self.label_image = Label(self)

        self.image_f = Image.open(self.path)
        self.height = int(self.width*self.image_f.height/self.image_f.width)
        self.image = self.image_f.resize((self.width, self.height), Image.ANTIALIAS)

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

    def __init__(self, master, data, **kw):
        super().__init__(master=master)
        self.master = master
        self.data = data
        self.current_question = 0

        # contain Question objects
        self.listQuestionObjects = [convertObject2Question(master=self.master,question_data=question, index=index) for index, question in enumerate(self.data['questions'])]
        self.setupUI()

    def setupUI(self):
        self.render(self.listQuestionObjects[0])

    def render(self, question: Question):
        '''render the question object'''

        logging.info(f'render {question}')

        # delete the previous question if any
        for widget in self.grid_slaves():
            widget.destroy()

        # render question
        self.label_question = Label(self)
        self.label_question['text'] = str(question.index)+'. '+question.content
        self.label_question.grid(row=0, column=0, sticky='w')

        # get list of answers
        self.list_radiobutton = []
        for answer in question.answers:
            ans = Radiobutton(self)
            ans['text'] = answer.content
            ans['compound'] = 'bottom'
            ans['value'] = answer.name
            ans['variable'] = question.choice
            ans['command'] = self.setStateQuestionIsMark
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

        # render the disabled question
        if question.state == 'sure':
            self.label_question['state'] = 'disabled'
            for radiobutton in self.list_radiobutton:
                radiobutton['state'] = 'disabled'
            self.button_sure['state'] = 'disabled'

    def nextQuestion(self):
        '''go to next question'''
        logging.info(f'next question -> {self.listQuestionObjects[self.current_question + 1]}')
        self.current_question += 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def previousQuestion(self):
        '''go to previous question'''
        logging.info(f'previous question -> {self.listQuestionObjects[self.current_question - 1]}')
        self.current_question -= 1
        self.listWidgets = self.pack_slaves()
        for widget in self.listWidgets:
            widget.destroy()
        self.render(self.listQuestionObjects[self.current_question])

    def allIs(self, value, can_loop):
        '''If all question is mark, it will return True'''
        for i in can_loop:
            if i != value:
                return False
        return True

    def getAmountQuestionStateMark(self):
        return [question.state == 'mark' for question in self.listQuestionObjects].count(True)

    def getAmountQuestionStateDone(self):
        return [question.state == 'sure' for question in self.listQuestionObjects].count(True)

    def checkValid(self):
        logging.info('check valid exam')
        for question in self.listQuestionObjects:
            if question.state == 'no':
                showwarning('Warning', 'You have not completed some question!')
                return

        # check all is mark or mark + sure = totalAmountQuestion
        all_is_mark = self.allIs('mark', [i.state for i in self.listQuestionObjects])
        all_is_mark_or_and_sure = (self.getAmountQuestionStateMark() + self.getAmountQuestionStateDone() == len(self.listQuestionObjects)) and self.getAmountQuestionStateMark() != 0
        if all_is_mark or all_is_mark_or_and_sure:
            if askyesno('Warning', 'Do you want to Sure all and Finish this exam!'):
                for question in self.listQuestionObjects:
                    question.state = 'sure'
                self.doneExam()
            return
        logging.info('check fail')
        logging.info(f'all_is_mark {all_is_mark}')
        logging.info(f'all_is_mark {all_is_mark_or_and_sure}')

    def doneExam(self):
        '''finish the exam and send data to server'''
        logging.info('finish the exam and send data to server')
        # send data to server
        answers = [question.getAnswer() for question in self.listQuestionObjects]
        logging.info(f'Done exam {answers}')
        self.master.quit()

    def timeOut(self):
        '''when time was out, it would call self.doneExam()'''
        logging.info('Time out, your results will be sent to the server!')
        self.doneExam()

    def setStateQuestionIsMark(self):
        logging.info(f'change the state of {self.listQuestionObjects[self.current_question]} to MARK -> {self.listQuestionObjects[self.current_question].getAnswer()}')
        self.listQuestionObjects[self.current_question].changeState2Mark()

    def setStateQuestionIsSure(self):
        logging.info('check if the question has been marked')
        if self.listQuestionObjects[self.current_question].getAnswer() == '':
            showwarning('Warning', 'You have not answered this question!')
            return
        if askyesno('Sure this question', 'Are you sure?'):
            logging.info(f'change the state of question {self.listQuestionObjects[self.current_question]} to SURE')
            self.listQuestionObjects[self.current_question].changeState2Sure()

            # disable that question
            # render the disabled question
            self.label_question['state'] = 'disabled'
            for radiobutton in self.list_radiobutton:
                radiobutton['state'] = 'disabled'
            self.button_sure['state'] = 'disabled'

    def getAmountQuestion(self):
        '''return amount question'''
        return len(self.listQuestionObjects)

