import json
import string
from tkinter import Radiobutton, Label, StringVar
from PIL import Image, ImageTk

class Answer:

    def __init__(self, name, content, image='', **kw):
        self.name = name
        self.content = content
        self.image = image


class Question:

    # mac dinh json data da duoc convert sang object trong python
    def __init__(self, content: str, images=[], answers=[]):
        self.content = content
        self.images = images
        self.answers = answers # [Answer object]
        self.choice = StringVar()
        self.state = 'no'  # mark, sure, no

    def changeState2Mark(self):
        self.state = 'mark'

    def changeState2No(self):
        self.state = 'no'

    def changeState2Sure(self):
        self.state = 'sure'

    def answerSelected(self):
        '''trả về Answer object được chọn trong Question, nếu Question chưa được chọn thì trả về None'''
        for answer in self.answers:
            if answer.name == self.choice:
                return answer
        return None



