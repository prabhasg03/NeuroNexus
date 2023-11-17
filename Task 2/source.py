import os
import tkinter as tk
from tkinter import messagebox
import source1
import source2


class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")
        self.root.title("TicTacToe")
        self.fra = tk.Frame(root, bg="green")
        self.fra.place(width="400", height="400", relx=.5, rely=.5, anchor="center")
        self.button1 = tk.Button(self.fra, text="Player vs Player", command=self.pla)
        self.button2 = tk.Button(self.fra, text="Player vs AI", command=self.ai)
        self.button3 = tk.Button(self.fra, text="Exit", command=self.ex)
        self.lab = tk.Label(self.fra, text="TicTacToe", bg="yellow", font=("Arial Bold", 30))
        self.lab.pack(ipadx="400", ipady="20", pady="30", side="top", anchor="n")
        self.button1.pack(ipadx="10", pady="20", side="top", anchor="n")
        self.button2.pack(ipadx="20", pady="20", side="top", anchor="n")
        self.button3.pack(ipadx="40", pady="20", side="top", anchor="n")

    def pla(self):
        self.root.destroy()
        # Call your player vs player function or open the corresponding window here
        source1.main()

    def ai(self):
        self.root.destroy()
        # Call your player vs AI function or open the corresponding window here
        source2.main()

    def ex(self):
        if messagebox.askyesno("Exit", "Are you sure to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()