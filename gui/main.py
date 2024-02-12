import io
import tkinter as tk
from tkinter import ttk

from PIL import Image, EpsImagePlugin

from .config import SO_PATH, NN_DUMP_PATH, GS_PATH
from .predict import load_predict
from .preprocess import prepare_image


EpsImagePlugin.gs_windows_binary = GS_PATH
EpsImagePlugin.gs_binary = GS_PATH


predict = None


def get_prediction(*args, **kwargs):
    global predict
    if predict is None:
        predict = load_predict(SO_PATH)
    return predict(*args, **kwargs)


class NumberRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Recognition App")

        drawingFrame = tk.Frame(root)
        self.canvas = tk.Canvas(
            drawingFrame, bg="white", bd=3, width=560, height=560
        )
        self.canvas.grid(row=0, column=0)
        self.label = tk.Label(
            drawingFrame,
            text="Draw a number using left-click"
        )
        self.label.grid(row=1, column=0, pady=5, padx=5)
        self.clearButton = tk.Button(drawingFrame, text="Clear")
        self.clearButton.bind("<Button-1>", self.clearCanvas)
        self.clearButton.grid(
            row=1, column=1, ipadx=5, ipady=5, padx=5, pady=5
        )
        drawingFrame.grid(row=0, column=0)

        numberFrame = tk.Frame(root)
        self.number_probabilities = {}
        for i in range(10):
            frame_i = tk.Frame(numberFrame)
            scale_label = tk.Label(frame_i, text=str(i))
            scale_label.grid(row=0, column=0, padx=10, pady=10)
            self.number_probabilities[i] = var = tk.IntVar()
            scale = ttk.Progressbar(
                frame_i, orient="horizontal",
                mode="determinate", length=200,
                variable=var
            )
            scale.grid(row=0, column=1, padx=10, pady=10)
            frame_i.grid(row=i, column=0, padx=10, pady=10)
        numberFrame.grid(row=0, column=1)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.predict_number)

    def clearCanvas(self, _):
        self.canvas.delete("all")
        for v in self.number_probabilities.values():
            v.set(0)

    def predict_number(self, _):
        ps = self.canvas.postscript(colormode="color")
        img = Image.open(io.BytesIO(ps.encode("utf-8")))
        normalized_values = prepare_image(img)

        # Provide a valid path to the neural network dump
        prediction = get_prediction(
            NN_DUMP_PATH,
            list(normalized_values)
        )
        for i, prob in enumerate(prediction):
            self.number_probabilities[i].set(prob * 100)

    def draw(self, event):
        x1, y1 = (event.x - 10), (event.y - 10)
        x2, y2 = (event.x + 10), (event.y + 10)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=0)


def main():
    root = tk.Tk()
    _ = NumberRecognitionApp(root)
    root.mainloop()
