from tkinter import Tk, Frame, StringVar, PhotoImage, Canvas
from tkinter.messagebox import askyesno, showwarning
from tkinter.ttk import Label, Button, Radiobutton, Scrollbar, Frame
# from info_exam import InformationExam
# from center_exam import CenterExam
# from footer_exam import FooterExam
# from state_exam import StateExam
# from question import Answer, convertObject2Question
from PIL import Image, ImageTk
import os
import json
import logging
import threading
import time
import string

logging.basicConfig(level=logging.INFO)
def allIs(value, can_loop):
    '''If all question is mark, it will return True'''
    for i in can_loop:
        if i != value:
            return False
    return True

class Question:

    # mac dinh json data da duoc convert sang object trong python
    def __init__(self,master, index: int, content: str, images=[], answers=[]):
        self.master = master
        self.index = index
        self.content = content
        self.images = images
        self.answers = answers # [Answer objects]
        self.choice = StringVar(master=self.master)
        self.state = 'no'  # mark, sure, no

    def __repr__(self):
        return f'''<Question {self.index}>\ncontent: {self.content}\nanswers: {self.answers}\nchoice: {self.choice.get()}\nstate: {self.state}'''

    def changeState2Mark(self):
        '''change state of question to Mark'''
        self.state = 'mark'

    def changeState2No(self):
        '''change state of question to No'''
        self.state = 'no'

    def changeState2Sure(self):
        '''change state of question to Sure'''
        self.state = 'sure'

    def getAnswer(self):
        '''return a string which contain answer'''
        return self.choice.get()

    def getAmountAnswer(self):
        '''return amount answer of this question'''
        return len(self.answers)

    def answerSelected(self):
        '''trả về Answer object được chọn trong Question, nếu Question chưa được chọn thì trả về None'''
        for answer in self.answers:
            if answer.name == self.choice.get():
                return answer
        return None


class Answer:

    def __init__(self, name, content, image='', **kw):
        self.name = name
        self.content = content
        self.image = image

    def __repr__(self):
        return self.content

        
def convertObject2Question(master,question_data, index):
    logging.info('Convert data from json to Python object')
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
    return Question(master=master,index=index, content=content, images=images, answers=answers)


class StatusButton(Button):

    def __init__(self, master, index, callback,**kw):
        super().__init__(master=master)
        self.master = master
        self.index = index
        self.callback =callback

        self.text_variable = StringVar()
        self.text_variable.set(f'{self.index}')
        self['textvariable'] = self.text_variable

        self.photo = PhotoImage(file='icon/question-24.png')
        self['image'] = self.photo
        self.image = self.photo
        self['compound'] = 'right'
        self['command'] = lambda: self.callback(self.index)

    def __str__(self):
        return f'<StatusButton {self.index}>'
    
    def changeThisButtonToMark(self):
        self.photo = PhotoImage(file='icon/flag.png')
        self['image'] = self.photo
        self.image = self.photo

    def changeThisButtonToSure(self):
        self.photo = PhotoImage(file='icon/tick-24.png')
        self['image'] = self.photo
        self.image = self.photo

class StateExam(Frame):

    def __init__(self, master, listQuestionObjects:list, callback,**kw):
        super().__init__(master=master)
        self.master = master
        self.listQuestionObjects = listQuestionObjects
        self.callback = callback
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
        self.listStateButton = []
        for index in range(len(self.listQuestionObjects)):
            b = StatusButton(self.frame, index=index, callback=self.callback)
            self.listStateButton.append(b)
            b.pack(fill='x')


class FooterExam(Frame):

    def __init__(self, master,listQuestionObjects: list, **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.setupUI()

    def setupUI(self):
        self.previousButton = Button(self)
        self.previousButton['text'] = 'Previous'
        self.previousButton['state'] = 'disabled'
        self.previousButton.pack(side='left')

        self.nextButton = Button(self)
        self.nextButton['text'] = 'Next'
        self.nextButton.pack(side='left')

        self.doneButton = Button(self)
        self.doneButton['text'] = 'Done'
        self.doneButton.pack(side='right')


class InformationExam(Frame):

    def __init__(self, master, data, **kw):
        super().__init__(master=master)
        self.master = master
        self.data = data
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
        self.currentQuestion = Label(self)
        self.currentQuestion['text'] = f'Số câu hỏi: {self.numberQuestion}'
        self.currentQuestion.grid(column=0, row=0)

        self.testRoom = Label(self, text=self.room)
        self.testRoom.grid(column=1, row=0)

        self.testDate = Label(self, text=self.date)
        self.testDate.grid(column=2, row=0)

        self.studentName = Label(self, text=self.name)
        self.studentName.grid(column=3, row=0)

        self.studentId = Label(self, text=self.id)
        self.studentId.grid(column=4, row=0)

        self.testSubject = Label(self, text=self.subject)
        self.testSubject.grid(column=5, row=0)

        self.timeVar = StringVar()
        self.testTime = Label(self, textvariable=self.timeVar)
        self.testTime.grid(column=6, row=0)

    def countdown(self):
        '''Start countdown'''
        while self.time >= 0:
            mins, secs = divmod(self.time, 60)
            self.timeVar.set('{:02d}:{:02d}'.format(mins, secs))
            time.sleep(1)
            self.time -= 1


class ImageObject(Frame):

    def __init__(self, master, name: str, path: str, width: int, **kw):
        super().__init__(master=master, **kw)
        self.name = name
        self.path = path
        self.width = width
        self.setupUI()

    def setupUI(self):
        self.label_image = Label(self)

        self.image_f = Image.open(self.path)
        self.height = int(self.width*self.image_f.height/self.image_f.width)
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
            b = ImageObject(
                self.frame, name=image['name'], path=image['path'], width=500)
            b.pack(fill='x')


class CenterExam(Frame):
    '''this frame contain questions and render them'''
    # mac dinh data da duoc conver tu json sang object

    def __init__(self, master, listQuestionObjects:list, radioCallback, sureCallback,**kw):
        super().__init__(master=master)
        self.master = master
        self.callback = radioCallback
        self.sureCallback = sureCallback

        # contain Question objects
        self.listQuestionObjects = listQuestionObjects
        self.setupUI()

    def setupUI(self):
        self.render(self.listQuestionObjects[0])

    def render(self, question: Question):
        '''render the question object'''

        logging.info(f'render question {question.index}')

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
            ans['command'] = self.callback
            if os.path.exists(answer.image):
                i = Image.open(answer.image)
                width = 100
                height = int(width*i.height/i.width)
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
        if allIs(True, [os.path.exists(i['path']) for i in question.images]):
            self.frame_images_of_question = ImageQuestionContainer(
                self, question.images)
            location_column_frame_images_of_question = len(self.grid_slaves())
            self.frame_images_of_question.grid(
                row=0, column=1, rowspan=location_column_frame_images_of_question)

        self.button_sure = Button(self)
        self.button_sure['text'] = 'Sure this question'
        icon_tick = PhotoImage(file='icon/tick-24.png')
        self.button_sure['image'] = icon_tick
        self.button_sure.image = icon_tick
        self.button_sure['compound'] = 'left'
        self.button_sure['command'] = self.sureCallback

        # determind location of sure button, this button will be end of the frame
        location_row = len(self.grid_slaves())
        self.button_sure.grid(row=location_row, column=0)

        # render the disabled question
        if question.state == 'sure':
            self.label_question['state'] = 'disabled'
            for radiobutton in self.list_radiobutton:
                radiobutton['state'] = 'disabled'
            self.button_sure['state'] = 'disabled'




class MyInfoExamThread(threading.Thread):

    def __init__(self, name, info_exam: InformationExam):
        threading.Thread.__init__(self)
        self.name = name
        self.info_exam = info_exam

    def run(self):
        self.info_exam.countdown()


class MyStateExamThread(threading.Thread):

    def __init__(self, name, state_exam: StateExam):
        threading.Thread.__init__(self)
        self.name = name
        self.state_exam = state_exam

    def run(self):
        self.state_exam.checkQuestionState()


class App():

    def __init__(self, data, center_exam: CenterExam, info_exam: InformationExam, footer_exam: FooterExam, state_exam: StateExam):
        self.data = data
        self.master = Tk()
        self.center_exam = center_exam
        self.info_exam = info_exam
        self.footer_exam = footer_exam
        self.state_exam = state_exam

        self.listQuestionObjects = [convertObject2Question(
            master=self.master, question_data=question, index=index) for index, question in enumerate(self.data['questions'])]
        self.currentQuestion = 0
        self.setupUI()

    def setupUI(self):
        self.master.title('Xtest')
        self.master.iconbitmap('icon/xtest_icon.ico')
        self.master.grid_rowconfigure(0, minsize=50)

        self.center_exam = CenterExam(master=self.master, listQuestionObjects=self.listQuestionObjects, radioCallback=self.changeSateQuestionToMark, sureCallback=self.changeStateQuestionToSure)
        self.center_exam.grid(row=1, column=0)

        self.info_exam = InformationExam(master=self.master,data=self.data)
        self.info_exam.grid(row=0, column=0, columnspan=2)
        self.infoThread = MyInfoExamThread(name='Thread Information Exam', info_exam=self.info_exam)
        self.infoThread.daemon = True
        self.infoThread.start()

        self.footer_exam = FooterExam(master=self.master, listQuestionObjects=self.listQuestionObjects)
        self.footer_exam.grid(row=2, column=0, columnspan=2)
        self.footer_exam.previousButton['command'] = self.gotoPreviousQuestion
        self.footer_exam.nextButton['command'] = self.gotoNextQuestion
        self.footer_exam.doneButton['command'] = self.doneExam

        self.state_exam = StateExam(master=self.master, listQuestionObjects=self.listQuestionObjects, callback=self.gotoQuestion)
            
        self.state_exam.grid(row=1, column=1)

    def changeSateQuestionToMark(self):
        logging.info(f'change state question {self.currentQuestion} to mark')
        self.listQuestionObjects[self.currentQuestion].changeState2Mark()
        logging.info(self.listQuestionObjects[self.currentQuestion].state)

        self.state_exam.listStateButton[self.currentQuestion].changeThisButtonToMark()
        text = f'{self.state_exam.listStateButton[self.currentQuestion].index}. {self.listQuestionObjects[self.currentQuestion].choice.get()}'
        self.state_exam.listStateButton[self.currentQuestion].text_variable.set(text)

    def changeStateQuestionToSure(self):
        logging.info(f'change state question {self.currentQuestion} to sure')
        if self.listQuestionObjects[self.currentQuestion].choice.get() == '':
            logging.warning(f'Have no complete the question {self.currentQuestion}')
            showwarning('Cảnh báo','Bạn chưa trả lời câu hỏi này!')
        else:
            if askyesno('Thông tin',f'Chúng tôi sẽ chốt câu hỏi này với đáp án {self.listQuestionObjects[self.currentQuestion].choice.get()}, bạn chắc chứ?'):
                self.listQuestionObjects[self.currentQuestion].changeState2Sure()
                self.state_exam.listStateButton[self.currentQuestion].changeThisButtonToSure()
                self.center_exam.label_question['state'] = 'disabled'
                for btt in self.center_exam.list_radiobutton:
                    btt['state'] = 'disable'
                self.center_exam.button_sure['state'] = 'disabled'

    def getAmountQuestion(self):
        '''Trả về sổ lượng câu hỏi'''
        return len(self.listQuestionObjects)

    def gotoNextQuestion(self):
        logging.info(f'go to next question {self.currentQuestion+1}')
        self.currentQuestion = self.currentQuestion +1
        self.footer_exam.previousButton['state'] = 'normal'
        self.center_exam.render(self.listQuestionObjects[self.currentQuestion])
        if self.currentQuestion == self.getAmountQuestion() -1:
            self.footer_exam.nextButton['state'] = 'disabled'
            self.footer_exam.previousButton['state'] = 'normal'

    def gotoPreviousQuestion(self):
        logging.info(f'go to previous question {self.currentQuestion-1}')
        self.currentQuestion = self.currentQuestion -1
        self.footer_exam.nextButton['state'] = 'normal'
        self.center_exam.render(self.listQuestionObjects[self.currentQuestion])
        if self.currentQuestion==0:
            self.footer_exam.previousButton['state'] = 'disabled'
            self.footer_exam.nextButton['state'] = 'normal'

    def gotoQuestion(self, index):
        logging.info(f'goto the question {index}')
        if self.currentQuestion == index:
            return
        logging.info(f'go to question {index}')
        self.currentQuestion = index
        if self.currentQuestion == 0:
            self.footer_exam.previousButton['state'] = 'disabled'
            self.footer_exam.nextButton['state'] = 'normal'
        elif self.currentQuestion == self.getAmountQuestion()-1:
            self.footer_exam.previousButton['state'] = 'normal'
            self.footer_exam.nextButton['state'] = 'disabled'
        else:
            self.footer_exam.previousButton['state'] = 'normal'
            self.footer_exam.nextButton['state'] = 'normal'
        self.center_exam.render(self.listQuestionObjects[index])

    def doneExam(self):
        logging.info('Done exam')
        if allIs('sure',[question.state for question in self.listQuestionObjects]):
            if askyesno('Thông báo','Bạn thật sự muốn nộp bài chứ?'):
                logging.info(f'{[question.getAnswer() for question in self.listQuestionObjects]}')
                self.master.quit()
        elif [question.state for question in self.listQuestionObjects].count('mark') + [question.state for question in self.listQuestionObjects].count('sure') == self.getAmountQuestion():
            if askyesno('Thông báo','Bạn có muốn chốt tất cả các câu hỏi còn lại và nộp bài không?'):
                logging.info(self.getAllAnswers())
                self.master.quit()
        else:
            unanswered_question = ', '.join([str(question.index) for question in self.listQuestionObjects if question.state == 'no'])
            showwarning('Cảnh báo',f'Bạn chưa trả lời {self.getAmountUnansweredQuestion()} câu hỏi, đó là {unanswered_question}')

    def timeOut(self):
        showwarning('Hết giờ','Đã hết giờ, đáp án của bạn sẽ được gửi lên server, chờ một chút để có được điểm của mình!')
        logging.info(self.getAllAnswers())

    def getAmountUnansweredQuestion(self):
        return [question.state for question in self.listQuestionObjects].count('no')

    def getAmountMarkedQuestion(self):
        return [question.state for question in self.listQuestionObjects].count('mark')

    def getAmountCompletedQuestion(self):
        return [question.state for question in self.listQuestionObjects].count('sure')

    def getAllAnswers(self)->list:
        '''Trả về một list chứa đáp án'''
        return [question.getAnswer() for question in self.listQuestionObjects]

    def run(self):
        self.master.mainloop()


if __name__ == '__main__':
    with open('data_server_send.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    a = App(data=data, center_exam=CenterExam, info_exam=InformationExam,footer_exam=FooterExam, state_exam=StateExam)
    a.run()
