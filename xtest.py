from tkinter import Tk
from header_exam import InformationExam
from body_exam import CenterExam
from footer_exam import FooterExam
from state_exam import StateExam
import json
import logging

# logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    with open('data_server_send.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
    
    master = Tk()
    # master.state('zoomed') # maximize window

    center_exam = CenterExam(master=master, data=data)
    center_exam.grid(row=1, column=0)

    info_exam = InformationExam(master=master, center_exam=center_exam ,data=data)
    info_exam.grid(row=0, column=0, columnspan=3)

    state_exam = StateExam(master,center_exam)
    state_exam.grid(row=1, column=1)

    footer_exam = FooterExam(master=master, center_exam=center_exam)
    footer_exam.grid(row=2, column=0, columnspan=2)

    master.mainloop()
