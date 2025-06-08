import tkinter as tk
from tkinter import messagebox
import math

# Initialize the game window
window = tk.Tk()
window.title("Tic-Tac-Toe: Human (X) vs AI (O)")

# Game variables
board = [' ' for _ in range(9)]
buttons = []

# Win check
def is_winner(b, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(b[i] == b[j] == b[k] == player for i,j,k in wins)

# Check full board
def is_full():
    return ' ' not in board

# Get available moves
def get_available_moves():
    return [i for i, x in enumerate(board) if x == ' ']

# Minimax algorithm
def minimax(b, is_maximizing):
    if is_winner(b, 'O'):
        return 1
    elif is_winner(b, 'X'):
        return -1
    elif is_full():
        return 0

    if is_maximizing:
        best = -math.inf
        for move in get_available_moves():
            b[move] = 'O'
            score = minimax(b, False)
            b[move] = ' '
            best = max(score, best)
        return best
    else:
        best = math.inf
        for move in get_available_moves():
            b[move] = 'X'
            score = minimax(b, True)
            b[move] = ' '
            best = min(score, best)
        return best

# AI makes a move
def ai_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves():
        board[move] = 'O'
        score = minimax(board, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = 'O'
    buttons[best_move].config(text='O', state='disabled')

# Check game state
def check_game_over():
    if is_winner(board, 'X'):
        messagebox.showinfo("Game Over", "You win! 🎉")
        window.quit()
    elif is_winner(board, 'O'):
        messagebox.showinfo("Game Over", "AI wins! 😢")
        window.quit()
    elif is_full():
        messagebox.showinfo("Game Over", "It's a tie! 🤝")
        window.quit()

# Human move
def button_click(i):
    if board[i] == ' ':
        board[i] = 'X'
        buttons[i].config(text='X', state='disabled')
        check_game_over()
        if not is_full() and not is_winner(board, 'X'):
            ai_move()
            check_game_over()

# Create buttons
for i in range(9):
    btn = tk.Button(window, text=' ', font=('Arial', 24), width=5, height=2,
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

# Start GUI loop
window.mainloop()
