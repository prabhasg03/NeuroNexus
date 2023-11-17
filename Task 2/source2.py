import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x450")  # Increased height to accommodate the label
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player_turn = True
        self.game_over = False
        self.ai_level = "Hard"
        self.create_menu()
        self.create_board_frame()
        self.get_player_names()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        ai_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="AI Level", menu=ai_menu)
        ai_menu.add_command(label="Easy", command=lambda: self.set_ai_level("Easy"))
        ai_menu.add_command(label="Medium", command=lambda: self.set_ai_level("Medium"))
        ai_menu.add_command(label="Hard", command=lambda: self.set_ai_level("Hard"))
        menu_bar.add_command(label="Reset", command=self.reset_game)
        menu_bar.add_command(label="Exit", command=self.exit_game)

    def create_board_frame(self):
        board_frame = tk.Frame(self.root)
        board_frame.place(relx=.5, rely=.5, anchor="center")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 16),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.make_player_move(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j)

        self.turn_label = tk.Label(board_frame, text="", font=("Helvetica", 12))
        self.turn_label.grid(row=3, columnspan=3)

    def set_ai_level(self, level):
        self.ai_level = level

    def get_player_names(self):
        player_name = simpledialog.askstring("Player", "Enter your name:")
        if player_name:
            self.player_name = player_name
        else:
            self.player_name = "Player"

        self.update_turn_label()

    def make_player_move(self, row, col):
        if not self.game_over and self.board[row][col] == " ":
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state="disabled")
            self.check_game_state()

            if not self.game_over:
                self.make_ai_move()

    def make_ai_move(self):
        if not self.game_over:
            available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
            if self.ai_level == "Hard":
                move = self.get_ai_move_minimax(available_moves)
            else:
                move = self.get_random_move(available_moves)

            if move:
                row, col = move
                self.board[row][col] = "O"
                self.buttons[row][col].config(text="O", state="disabled")
                self.check_game_state()

    def get_random_move(self, available_moves):
        return random.choice(available_moves) if available_moves else None

    def get_ai_move_minimax(self, available_moves):
        best_val = float("-inf")
        best_move = None

        for move in available_moves:
            row, col = move
            self.board[row][col] = "O"
            eval = self.minimax(0, False)
            self.board[row][col] = " "

            if eval > best_val:
                best_move = move
                best_val = eval

        return best_move

    def minimax(self, depth, maximizing_player):
        score = self.evaluate()
        if score == 1 or score == -1 or self.is_board_full():
            return score

        if maximizing_player:
            max_eval = float("-inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        eval = self.minimax(depth + 1, False)
                        self.board[i][j] = " "
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X"
                        eval = self.minimax(depth + 1, True)
                        self.board[i][j] = " "
                        min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self):
        for i in range(3):
            if all(self.board[i][j] == "X" for j in range(3)):
                return -1
            if all(self.board[i][j] == "O" for j in range(3)):
                return 1
            if all(self.board[j][i] == "X" for j in range(3)):
                return -1
            if all(self.board[j][i] == "O" for j in range(3)):
                return 1

        if all(self.board[i][i] == "X" for i in range(3)) or all(self.board[i][2 - i] == "X" for i in range(3)):
            return -1
        if all(self.board[i][i] == "O" for i in range(3)) or all(self.board[i][2 - i] == "O" for i in range(3)):
            return 1

        return 0

    def check_game_state(self):
        if self.check_winner("X"):
            self.show_message(f"{self.player_name} wins!")
        elif self.check_winner("O"):
            self.show_message("AI wins!")
        elif self.is_board_full():
            self.show_message("It's a draw!")

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
        for i in range(3):
            for j in range(3):
                self.board[i][j] = " "
                self.buttons[i][j].config(text="", state="normal")

        self.player_turn = True
        self.game_over = False
        self.update_turn_label()

    def update_turn_label(self):
        if self.player_turn:
            self.turn_label.config(text=f"{self.player_name}'s turn")
        else:
            self.turn_label.config(text="AI's turn")

    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry("+{}+{}".format(position_right, position_down))
    root.mainloop()


if __name__ == "__main__":
    main()
