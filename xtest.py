from tkinter import Tk
from info_exam import InformationExam
from center_exam import CenterExam
from footer_exam import FooterExam
from state_exam import StateExam
from question import Answer,convertObject2Question
import json
import logging
import threading
import time


logging.basicConfig(level=logging.INFO)

class MyInfoExamThread(threading.Thread):

    def __init__(self,name, info_exam:InformationExam):
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

        self.listQuestionObjects = [convertObject2Question(master=self.master,question_data=question, index=index) for index, question in enumerate(self.data['questions'])]
        self.currentQuestion = 0
        self.setupUI()

    def setupUI(self):
        # main window
        # self.master.state('zoomed')  # maximize window
        self.master.title('Xtest - Phần mềm kiểm tra trắc nghiệm trên máy tính')
        self.master.iconbitmap('icon/xtest_icon.ico')
        self.master.grid_rowconfigure(0, minsize=50)
        
        self.center_exam = CenterExam(master=self.master, data=self.data)
        self.center_exam.grid(row=1, column=0)

        self.info_exam = InformationExam(master=self.master, center_exam=self.center_exam, data=self.data)
        self.info_exam.grid(row=0, column=0, columnspan=2)
        self.infoThread = MyInfoExamThread(name='Thread Information Exam', info_exam=self.info_exam)
        self.infoThread.daemon = True
        self.infoThread.start()


        self.footer_exam = FooterExam(master=self.master, center_exam=self.center_exam)
        self.footer_exam.grid(row=2, column=0, columnspan=2)


        self.state_exam = StateExam(self.master, self.center_exam, footer_exam=self.footer_exam)
        self.state_exam.grid(row=1, column=1)
        self.stateThread = MyStateExamThread(name='Thread State Exam', state_exam=self.state_exam)
        self.stateThread.daemon = True
        self.stateThread.start()

    def run(self):
        self.master.mainloop()


if __name__ == '__main__':
    with open('data_server_send.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    a = App(data=data, center_exam=CenterExam, info_exam=InformationExam,
            footer_exam=FooterExam, state_exam=StateExam)
    a.run()