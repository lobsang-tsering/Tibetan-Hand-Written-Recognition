from tkinter import *
import PIL
import numpy as np
from PIL import Image, ImageDraw
import cv2
import  pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import Imputer
class PaintApp:
    xcor = []
    ycor = []
    drawing_tool = "pencil"
    left_but = "up"
    x_pos, y_pos = None, None

    def left_but_down(self, event=None):
        self.left_but = "down"

        self.x1_line_pt = event.x
        self.y1_line_pt = event.y


    def left_but_up(self, event=None):
        self.left_but = "up"

        self.x_pos = None
        self.y_pos = None

        self.x2_line_pt = event.x
        self.y2_line_pt = event.y


    def motion(self, event=None):

        if self.drawing_tool == "pencil":
            self.pencil_draw(event)


    def pencil_draw(self, event=None):
        if self.left_but == "down":

            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos, self.y_pos, event.x, event.y, smooth=TRUE, width=4)
                draw.line([self.x_pos, self.y_pos, event.x, event.y], fill="black", width=5)

            self.x_pos = event.x
            self.y_pos = event.y

    def __init__(self, root):
        drawing_area = Canvas(root, bg="white", width=300, height= 300)
        drawing_area.pack()
        button1 = Button(text="save", command=save)
        button1.pack()
        button = Button(text="predict", command=predict)
        button.pack()
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.left_but_down)
        drawing_area.bind("<ButtonRelease-1>", self.left_but_up)
        drawing_area.delete("all")

def predict():
        print("Predict fuc")
        data = pd.read_csv('trainTibetanAlphanumeric.csv').as_matrix()
        xtrain = data[0:, 1:]
        train_lable = data[0:, 0]
        X = Imputer().fit_transform(xtrain)
        clf = DecisionTreeClassifier()
        clf.fit(X, train_lable)
        print("done training the data")
        print("start reading the paint")
        im = cv2.imread('image.png', 0)
        a = []
        for x in np.nditer(im, op_flags=['readwrite']):
            if x[...] > 250:
                x[...] = int(1)
                a.append(1)
            else:
                x[...] = int(0)
                a.append(0)
        print(im)
        print("modified values")
        print(a)
        print("done reading the paint")
        print("i am trying to predict the paint")
        print(clf.predict(a))


def save():
        fileName = "image.png"
        image1.save(fileName)
        pix_val = list(image1.getdata())
        image1.thumbnail((28, 28))
        x = np.asanyarray(image1)
        gray_image = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        print(type(gray_image))
        print(gray_image.shape)
        image1.save('image.png')
        print(gray_image)
image1 = PIL.Image.new("RGB", (300, 300), (255, 255, 255))
draw = ImageDraw.Draw(image1)
root = Tk()
paint_app = PaintApp(root)
root.mainloop()