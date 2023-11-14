import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human_player = 'X'
        self.ai_player = 'O'

    def available_moves(self):
        return [i for i, val in enumerate(self.board) if val == ' ']

    def make_move(self, position, player):
        self.board[position] = player

    def is_winner(self, player):
        for i in range(0, 9, 3):
            if all(self.board[j] == player for j in range(i, i + 3)):
                return True
        for i in range(3):
            if all(self.board[j] == player for j in range(i, i + 7, 3)):
                return True
        if all(self.board[j] == player for j in range(0, 9, 4)) or all(self.board[j] == player for j in range(2, 7, 2)):
            return True
        return False

    def is_board_full(self):
        return ' ' not in self.board

    def game_over(self):
        return self.is_winner(self.human_player) or self.is_winner(self.ai_player) or self.is_board_full()

class AIPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, game):
        _, move = self.minimax(game, float('-inf'), float('inf'))
        return move

    def minimax(self, game, alpha, beta):
        if game.is_winner(game.human_player):
            return -1, None
        elif game.is_winner(self.symbol):
            return 1, None
        elif game.is_board_full():
            return 0, None

        best_score = float('-inf') if self.symbol == 'O' else float('inf')
        best_move = None

        for move in game.available_moves():
            game.make_move(move, self.symbol)
            score, _ = self.minimax(game, alpha, beta)
            game.make_move(move, ' ')

            if self.symbol == 'O':
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score, best_move

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.game = TicTacToe()
        self.ai_player = AIPlayer('O')

        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(self.root, text='', width=6, height=3,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=row, column=col)
            self.buttons.append(button)

    def make_move(self, position):
        if self.game.board[position] == ' ' and not self.game.game_over():
            self.game.make_move(position, self.game.human_player)
            self.buttons[position].config(text='X')
            if self.game.game_over():
                self.show_result()
            else:
                ai_move = self.ai_player.get_move(self.game)
                self.game.make_move(ai_move, self.ai_player.symbol)
                self.buttons[ai_move].config(text='O')
                if self.game.game_over():
                    self.show_result()

    def show_result(self):
        result = ""
        if self.game.is_winner(self.game.human_player):
            result = "Congratulations! You win!"
        elif self.game.is_winner(self.ai_player.symbol):
            result = "AI wins! Better luck next time."
        else:
            result = "It's a draw!"

        messagebox.showinfo("Game Over", result)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = TicTacToeGUI()
    gui.run()