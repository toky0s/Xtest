import json
import string
from tkinter import Radiobutton, Label, StringVar
from PIL import Image, ImageTk


class Question:

    # mac dinh json data da duoc convert sang object trong python
    def __init__(self, index: int, content: str, images=[], answers=[]):
        self.index = index
        self.content = content
        self.images = images
        self.answers = answers # [Answer object]
        self.choice = StringVar()
        self.state = 'no'  # mark, sure, no

    def __repr__(self):
        return f'<Question {self.index}>'

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

    def showQuestion(self):
        '''Show full question'''
        q = f'{self.index}. {self.content}'
        print(q)
        for ans in self.answers:
            print(f'{ans.name}. {ans.content}')

class Answer:

    def __init__(self, name, content, image='', **kw):
        self.name = name
        self.content = content
        self.image = image

    def __repr__(self):
        return self.content