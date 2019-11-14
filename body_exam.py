from tkinter import *
import os
import json
import string
from PIL import Image, ImageTk
from question import Question, Answer

def convertObject2Question(question_data):
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
    return Question(content=content, images=images, answers=answers)

class CenterExam(Frame):
    # mac dinh data da duoc conver tu json sang object
    def __init__(self, master, **kw):
        super().__init__(master=master)
        self.master = master
        self.data = kw['data']

        # object to Question
        self.current_question = 0
        self.listQuestionObjects = list(map(convertObject2Question,self.data['questions'])) # contain Question objects
        self.setupUI()
#
    def setupUI(self):
        self.render(self.listQuestionObjects[0])

    def render(self, question:Question):
        self.label_question = Label(self)
        self.label_question['text'] = question.content
        self.label_question.pack(anchor='w')

        self.list_radiobutton = []
        for answer in question.answers:
            ans = Radiobutton(self)
            ans['text'] = answer.content
            ans['compound'] = 'left'
            ans['value'] = answer.name
            ans['variable'] = question.choice
            ans['command'] = lambda: self.showInfo(question) #test
            if os.path.exists(answer.image):
                i = Image.open(answer.image)
                photo = ImageTk.PhotoImage(i)
                ans['image'] = photo
                ans.image = photo
            self.list_radiobutton.append(ans)

        for radiobtt in self.list_radiobutton:
            radiobtt.pack(anchor='w')

    def showInfo(self, question: Question):
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

    def doneExam(self):
        print('nop bai')
        self.master.quit()

    def sendData2Server(self):
        pass

    def setStateQuestion(self):
        '''Thay đổi trạng thái của câu hỏi'''
        pass

if __name__ == '__main__':
    with open('data_server_send.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
    master = Tk()
    a = CenterExam(master, data=data)
    a.pack(anchor='w')
    master.mainloop()