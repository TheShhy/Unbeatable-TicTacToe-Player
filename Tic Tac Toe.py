#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
from tkinter import messagebox
import random

# Initialize the game board
board = [' ' for _ in range(9)]
current_player = 'X'

# Initialize the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Function to check if the board is full
def is_board_full():
    return ' ' not in board

# Function to check if a player has won
def check_win(player):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]

    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

# Function to evaluate the board for the minimax algorithm
def evaluate_board():
    if check_win('X'):
        return -1
    elif check_win('O'):
        return 1
    elif is_board_full():
        return 0
    else:
        return None

# Function to implement the minimax algorithm with alpha-beta pruning
def minimax(depth, is_maximizing, alpha, beta):
    result = evaluate_board()

    if result is not None:
        return result

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

# Function to make the AI's move using the minimax algorithm
def ai_move():
    best_move = -1
    best_eval = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            eval = minimax(0, False, alpha, beta)
            board[i] = ' '
            if eval > best_eval:
                best_eval = eval
                best_move = i

    return best_move

# Function to handle button click events
def on_click(button, index):
    global current_player

    if board[index] == ' ' and current_player == 'X':
        button.config(text=current_player)
        board[index] = current_player

        if check_win(current_player):
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            root.quit()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            root.quit()
        else:
            current_player = 'O'
            ai_button_index = ai_move()
            ai_button = buttons[ai_button_index]
            ai_button.config(text='O')
            board[ai_button_index] = 'O'

            if check_win('O'):
                messagebox.showinfo("Game Over", "AI wins!")
                root.quit()
            elif is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                root.quit()
            else:
                current_player = 'X'

# Create the game board buttons
buttons = []
for i in range(9):
    button = tk.Button(root, text=' ', font=('normal', 20), width=10, height=3,
                       command=lambda i=i: on_click(buttons[i], i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

root.mainloop()

