import tkinter as tk
from tkinter import ttk, messagebox
import random


# Function to check if a player has won
def check_win(player):
    return (
        any(all(board[i][j] == player for i in range(3)) for j in range(3))
        or any(all(board[i][j] == player for j in range(3)) for i in range(3))
        or all(board[i][i] == player for i in range(3))
        or all(board[i][2 - i] == player for i in range(3))
    )


# Function to check if the board is full
def is_board_full():
    return all(board[i][j] != "" for i in range(3) for j in range(3))


# Function to show the game over message
def show_game_over_message(winner):
    message = "It's a tie!" if winner == "tie" else f"Player {winner} wins!"
    messagebox.showinfo("Game Over", message)
    reset_board()

# Function to make a player's move
def make_move(row, col):
    if board[row][col] == "" and not game_over:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")

        if check_win(current_player):
            show_game_over_message(current_player)
        elif is_board_full():
            show_game_over_message("tie")
        else:
            switch_player()
            if current_player == "O":
                ai_move()

# Function to switch the current player
def switch_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    player_turn_label.config(text=f"Player {current_player}'s turn")

# Function for the AI player's move
def ai_move():
    _, move = minimax(board, "O", -float("inf"), float("inf"), 0)
    make_move(move[0], move[1])

# Minimax algorithm for AI move 
# minimax is algorithm in artificial intelligence for decision-making in two-player games
def minimax(board, player, alpha, beta, depth):
    if check_win("O"):
        return 1, None
    if check_win("X"):
        return -1, None
    if is_board_full():
        return 0, None

    if player == "O":
        best_score = -float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score, _ = minimax(board, "X", alpha, beta, depth + 1)
                    board[i][j] = ""

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break

        return best_score, best_move
    else:
        best_score = float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score, _ = minimax(board, "O", alpha, beta, depth + 1)
                    board[i][j] = ""

                    if score < best_score:
                        best_score = score
                        best_move = (i, j)

                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break

        return best_score, best_move

# Function to reset the game board
def reset_board():
    global board, current_player, game_over

    # Reset the 'board' variable to an empty 3x3 grid
    board = [["" for _ in range(3)] for _ in range(3)]

    # Set the 'current_player' back to "X" (the starting player)
    current_player = "X"

    # Set 'game_over' to False to indicate that the game is not over
    game_over = False

    # Update the player turn label to indicate it's "Player X's turn"
    player_turn_label.config(text=f"Player {current_player}'s turn")

    # Reset the text and enable state of all buttons on the game board
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state="normal")



# Creating the main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Initializing the game variables
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False

# Creating a style for buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 18), padding=10)

# Creating a label for displaying player's turn
player_turn_label = ttk.Label(root, text=f"Player {current_player}'s turn")
player_turn_label.grid(row=3, column=0, columnspan=3, pady=20)

# Creating buttons for the game board
buttons = []  # Create an empty list to store the button widgets

for row in range(3):
    button_row = []  #for Creating an empty list to store buttons in a row
    for col in range(3):
        #for Creating a Button widget for each cell in the 3x3 grid
        button = ttk.Button(
            root,               # the main game window
            text="",            # Initial text on the button (empty)
            width=5,            
            command=lambda r=row, c=col: make_move(r, c)  # Lambda function to pass row and column to make_move
        )
        button.grid(row=row, column=col, padx=5, pady=5)  # Grid layout positioning
        button_row.append(button)  # Append the button to the row list
    buttons.append(button_row)  # Append the row of buttons to the buttons list

reset_button = ttk.Button(root, text="Restart", command=reset_board)
reset_button.grid(row=4, column=0, columnspan=3, pady=10)


#for calculating screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#for calculating the center position of the window
x = (screen_width - root.winfo_reqwidth()) / 2
y = (screen_height - root.winfo_reqheight()) / 2

#for Setting the window's position
root.geometry("+%d+%d" % (x, y))

 # this starts the Tkinter main event loop, which listens for user interactions and keeps the GUI application running.
root.mainloop()