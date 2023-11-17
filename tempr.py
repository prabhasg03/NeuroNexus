import tkinter as tk

window = tk.Tk()
window.title("TicTacToe")
window.geometry("400x400")
fra=tk.Frame(window)
fra.place(relx=.5, rely=.5,anchor= "center")
button1 = tk.Button(fra, text="Player vs Player")
button2 = tk.Button(fra, text="Player vs AI")
button3 = tk.Button(fra, text="Exit")
# Pack buttons and center them
button1.pack(side="top", anchor="n")
button2.pack(side="top", anchor="n")
button3.pack(side="top", anchor="n")

window.mainloop()