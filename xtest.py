from tkinter import *
from header_exam import InformationExam
from body_exam import CenterExam
from footer_exam import FooterExam

import json

if __name__ == '__main__':
    with open('data_server_send.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
    master = Tk()
    info_exam = InformationExam(master=master, data=data)
    info_exam.pack()
    center_exam = CenterExam(master=master, data=data)
    center_exam.pack()
    footer_exam = FooterExam(master=master, center_exam=center_exam)
    footer_exam.pack()
    master.mainloop()
