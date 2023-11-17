import tkinter as tk
from tkinter import messagebox, simpledialog
import source
import source2
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player_names = {"X": "", "O": ""}
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.create_menu()
        self.create_board_frame()
        self.get_player_names()

    def func(self):
        self.exit_game()
        source.main()
    def func1(self):
        self.exit_game()
        source2.main()
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        menu_bar.add_command(label="Main Menu", command=self.func)
        menu_bar.add_command(label="Player vs AI", command=self.func1)
        menu_bar.add_command(label="Reset", command=self.reset_game)
        menu_bar.add_command(label="Exit", command=self.exit_game)

    def create_board_frame(self):
        board_frame = tk.Frame(self.root)
        board_frame.place(width="300", height="300", relx=.5, rely=.5, anchor="center")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 16),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j)

        self.turn_label = tk.Label(board_frame, text="", font=("Helvetica", 12))
        self.turn_label.grid(row=3, columnspan=3)

    def get_player_names(self):
        player_x_name = simpledialog.askstring("Player X", "Enter name for Player X:")
        player_o_name = simpledialog.askstring("Player O", "Enter name for Player O:")

        if player_x_name:
            self.player_names["X"] = player_x_name
        if player_o_name:
            self.player_names["O"] = player_o_name
        if self.player_names["X"].strip() == "":
            self.player_names["X"] = "X"
        if self.player_names["O"].strip() == "":
            self.player_names["O"] = "O"
        self.update_status()
        self.update_turn_label()

    def make_move(self, row, col):
        if not self.game_over and self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state="disabled")

            if self.check_winner(self.current_player):
                self.show_message(f"{self.player_names[self.current_player]} wins!")
            elif self.is_board_full():
                self.show_message("It's a draw!")
            else:
                self.switch_player()
                self.update_status()
                self.update_turn_label()

    def update_turn_label(self):
        self.turn_label.config(text=f"{self.player_names[self.current_player]}'s turn")

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(
                self.board[j][i] == player for j in range(3)
            ):
                self.game_over = True
                return True

        if all(self.board[i][i] == player for i in range(3)) or all(
            self.board[i][2 - i] == player for i in range(3)
        ):
            self.game_over = True
            return True

        return False

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def show_message(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = "X"

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")

        self.get_player_names()
        self.update_status()
        self.update_turn_label()

    def update_status(self):
        self.root.title(f"Tic Tac Toe - {self.player_names[self.current_player]}'s turn")

    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("400x450")  # Increased height to accommodate the label
    root.mainloop()

if __name__ == "__main__":
    main()
