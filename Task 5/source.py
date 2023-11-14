import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    cords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        cords = [x, y, w, h]
    return cords, img
def detect(img, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0)}
    cords, img = draw_boundary(img, faceCascade, 1.2, 10, color['green'], "Human")
    return img
def select_camera():
    vc = cv2.VideoCapture(0)
    detect_and_display(vc)


def select_image():
    try:
        messagebox.showinfo("Disclaimer", "Select only Images")
        file_path = filedialog.askopenfilename()
        x=file_path.split(".")[-1]
        if(x=='jpg'or x=='jpeg' or x=='png'):
            if file_path:
                detect_and_display(file_path)
        else:
            messagebox.showwarning("Warning", "You must select Image file only")

    except:
            messagebox.showwarning("Warning", "You must select image file only")
            root.mainloop()


def select_video():
    try:
        messagebox.showinfo("Disclaimer", "Select only Videos")
        file_path = filedialog.askopenfilename()
        x=file_path.split('.')[-1]
        if(x=='mp4' or x=='mpeg4' or x=='avi' or x=='mov'):
            if file_path:
                vc = cv2.VideoCapture(file_path)
                detect_and_display(vc)
        else:
            messagebox.showwarning("Warning", "You must select Video file only")
    except:
        messagebox.showwarning("Warning", "You must select Video file only")
        root.mainloop()

def detect_and_display(source):
    root.withdraw()  # Hide the Tkinter window during video/image display
    window_width, window_height = 800, 600  # Adjust window size as needed
    root.geometry(f"{window_width}x{window_height}")
    if isinstance(source, cv2.VideoCapture):  # If source is a video
        while True:
            _, img = source.read()
            img = detect(img, faceCascade)
            img = cv2.resize(img, (window_width, window_height))
            cv2.imshow("face detection", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    elif isinstance(source, str):  # If source is an image file
        img = cv2.imread(source)
        img = detect(img, faceCascade)
        img = cv2.resize(img, (window_width, window_height))
        cv2.imshow("face detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    root.deiconify()  # Show the Tkinter window after video/image display


def ex():
    x = messagebox.askyesno("Exit", "Are you sure to exit")
    if (x):
        root.destroy()

def on_window_resize(event):
    window_width, window_height = event.width, event.height
    background_label.config(width=window_width, height=window_height)


# Initialize Tkinter window
root = tk.Tk()
root.title("Face Detection")
root.geometry("400x400")
# Load background image
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)
# Create buttons with labels
camera_button = tk.Button(root, text="Select Camera", command=select_camera, font=("Helvetica", 14))
camera_button.pack(pady=20,anchor='center')
image_button = tk.Button(root, text="Select Image", command=select_image, font=("Helvetica", 14))
image_button.pack(pady=20,anchor='center')
video_button = tk.Button(root, text="Select Video", command=select_video, font=("Helvetica", 14))
video_button.pack(pady=20,anchor='center')
exit_button = tk.Button(root, text="Exit", command=ex, font=("Helvetica", 14))
exit_button.pack(pady=20,anchor='center')
# Bind the window resize event
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
root.bind("<Configure>", on_window_resize)
# Start Tkinter main loop
root.mainloop()