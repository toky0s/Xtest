from tkinter import Canvas, Button, Label, Frame, Tk, Scrollbar, GROOVE

def data():
    for i in range(50):
       Label(frame,text=i).grid(row=i,column=0)
       Label(frame,text="my text"+str(i)).grid(row=i,column=1)
       Label(frame,text="..........").grid(row=i,column=2)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
    canvas['background'] = 'red'

root=Tk()
sizex = 280
sizey = 250
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,bd=1)
myframe.place(x=10,y=10)

canvas=Canvas(myframe)
frame=Frame(canvas)
frame['background'] = 'green'
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data()
root.mainloop()

# import string
# from question import Question, Answer
# import json


# def convertObject2Question(question_data, index):
#     index = index
#     content = question_data['question']
#     images = question_data['images']
#     answers = []
#     for i in range(len(question_data['answers'])):
#         answer = question_data['answers'][i]
#         name = list(string.ascii_uppercase)[i]
#         content_ans = answer['content']
#         image_ans = answer['image']
#         ans = Answer(name=name,content=content_ans, image=image_ans)
#         answers.append(ans)
#     return Question(index=index,content=content, images=images, answers=answers)

# with open('data_server_send.json', 'r',encoding='utf-8') as f:
#     data = json.load(f)

# q = data['questions']
# lQuestions = [convertObject2Question(question_data=question, index=index) for index,question in enumerate(q)] 

# print(lQuestions)
# lQuestions[0].showQuestion()
# lQuestions[1].showQuestion()
# lQuestions[2].showQuestion()