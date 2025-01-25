import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np
import tensorflow


model = tensorflow.keras.models.load_model('best_model_95.keras')

classes = {
    0: 'Annual Crop',
    1: 'Forest',
    2: 'Herbaceous Vegetation',
    3: 'Highway',
    4: 'Industrial',
    5: 'Pasture',
    6: 'Permanent Crop',
    7: 'Residential',
    8: 'River',
    9: 'Sea or Lake'
}


top = tk.Tk()
top.geometry('800x600')
top.title('Land Use Classification')
top.configure(background='#CDCDCD')

label = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
image_display = Label(top)


def classify(file_path):
    try:

        image = Image.open(file_path).convert('RGB')
        image = image.resize((64, 64))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        pred = np.argmax(model.predict(image), axis=1)[0]
        land_use = classes[pred]
        label.configure(foreground='#011638', text=land_use)
    except Exception as e:
        label.configure(foreground='red', text=f"Error: {e}")
        print(f"Error: {e}")
def show_classify_button(file_path):

    classify_b = Button(
        top, text="Classify Image", command=lambda: classify(file_path),
        padx=10, pady=5
    )
    classify_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    classify_b.place(relx=0.79, rely=0.46)

def upload_image():

    try:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return


        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        image_display.configure(image=im)
        image_display.image = im
        label.configure(text='')

        show_classify_button(file_path)
    except Exception as e:
        print(f"Error: {e}")


upload = Button(top, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background='#DAA520', foreground='black', font=('arial', 10, 'bold'))
upload.pack(side=BOTTOM, pady=50)

image_display.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)

heading = Label(top, text="Land Use Classification", pady=20, font=('times new roman', 30, 'bold'))
heading.configure(background='#364156', foreground='#DAA520')
heading.pack()
top.configure(background='#282828')
top.mainloop()

