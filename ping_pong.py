import tkinter as tk
from tkinter import simpledialog

class Paddle:
    def __init__(self, canvas, x_position):
        """Initialize the paddle and create it on the canvas."""
        self.canvas = canvas
        self.paddle = canvas.create_rectangle(x_position, 150, x_position + 10, 250, fill="white")

    def move(self, direction):
        """Move the paddle up or down while ensuring it stays within canvas boundaries."""
        paddle_coords = self.canvas.coords(self.paddle)
        if direction == "up" and paddle_coords[1] > 0:
            self.canvas.move(self.paddle, 0, -20)
        elif direction == "down" and paddle_coords[3] < 400:
            self.canvas.move(self.paddle, 0, 20)

class Ball:
    def __init__(self, canvas):
        """Initialize the ball in the center and set its movement speed."""
        self.canvas = canvas
        self.ball = canvas.create_oval(290, 190, 310, 210, fill="white")
        self.dx = 3  # Horizontal speed
        self.dy = 3  # Vertical speed
        self.hit_count = 0  # Count paddle hits to increase speed over time

    def move(self):
        """Move the ball and handle bouncing off walls."""
        self.canvas.move(self.ball, self.dx, self.dy)
        ball_coords = self.canvas.coords(self.ball)

        # Ball bounces off top and bottom walls
        if ball_coords[1] <= 0 or ball_coords[3] >= 400:
            self.dy = -self.dy  # Reverse vertical direction

        return ball_coords

    def increase_speed(self):
        """Increase ball speed every 7 paddle hits."""
        if self.hit_count >= 7:
            self.dx *= 1.1
            self.dy *= 1.1
            self.hit_count = 0  # Reset counter

    def reset_position(self):
        """Reset the ball to the center with default speed."""
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        self.dx = 3
        self.dy = 3
        self.hit_count = 0

class PingPongGame:
    def __init__(self, root):
        """Initialize the main game window."""
        self.root = root
        self.root.title("Ping Pong Game")
        self.root.resizable(False, False)

        # Player Registration
        self.player_1_name = simpledialog.askstring("Player 1", "Enter Player 1's Name:") or "Player 1"
        self.player_2_name = simpledialog.askstring("Player 2", "Enter Player 2's Name:") or "Player 2"

        # Create the game canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        # Initialize game components
        self.init_game()

        # Key bindings for paddle movement
        self.root.bind("<w>", lambda event: self.paddle_1.move("up"))
        self.root.bind("<s>", lambda event: self.paddle_1.move("down"))
        self.root.bind("<Up>", lambda event: self.paddle_2.move("up"))
        self.root.bind("<Down>", lambda event: self.paddle_2.move("down"))

        # Start the game loop
        self.move_ball()

    def init_game(self):
        """Initialize or reset game components."""
        self.canvas.delete("all")  # Clear the canvas

        # Create paddles, ball, and scores
        self.paddle_1 = Paddle(self.canvas, 20)
        self.paddle_2 = Paddle(self.canvas, 570)
        self.ball = Ball(self.canvas)
        self.player_1_score = 0
        self.player_2_score = 0
        self.max_score = 5
        self.game_over = False
        self.winner_text = None  # Store the winner message ID
        self.ball_loop = None  # Store loop ID for canceling later

        # Display player names and scores
        self.score_display = self.canvas.create_text(300, 20,
            text=f"{self.player_1_name}: 0   {self.player_2_name}: 0", font=("Arial", 14), fill="white")

        # Restart button
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.restart_game)
        self.canvas.create_window(300, 50, window=self.restart_button)

    def update_score(self):
        """Update the displayed score."""
        self.canvas.itemconfig(self.score_display,
            text=f"{self.player_1_name}: {self.player_1_score}   {self.player_2_name}: {self.player_2_score}")

    def display_winner(self, winner):
        """Show the winner and stop the game."""
        self.game_over = True
        if self.winner_text:
            self.canvas.delete(self.winner_text)  # Remove previous winner message
        self.winner_text = self.canvas.create_text(300, 200, text=f"{winner} Wins!", font=("Arial", 24), fill="red")

    def move_ball(self):
        """Move the ball, check for collisions, and update the game state."""
        if self.game_over:
            return  # Stop movement if the game is over

        ball_coords = self.ball.move()
        paddle_1_coords = self.canvas.coords(self.paddle_1.paddle)
        paddle_2_coords = self.canvas.coords(self.paddle_2.paddle)

        # Collision with paddles
        if ball_coords[0] <= 30 and paddle_1_coords[1] < ball_coords[3] and paddle_1_coords[3] > ball_coords[1]:
            self.ball.dx = -self.ball.dx
            self.ball.hit_count += 1

        if ball_coords[2] >= 570 and paddle_2_coords[1] < ball_coords[3] and paddle_2_coords[3] > ball_coords[1]:
            self.ball.dx = -self.ball.dx
            self.ball.hit_count += 1

        # Scoring logic
        if ball_coords[0] <= 0:
            self.player_2_score += 1
            self.update_score()
            if self.player_2_score >= self.max_score:
                self.display_winner(self.player_2_name)
            else:
                self.ball.reset_position()

        if ball_coords[2] >= 600:
            self.player_1_score += 1
            self.update_score()
            if self.player_1_score >= self.max_score:
                self.display_winner(self.player_1_name)
            else:
                self.ball.reset_position()

        self.ball.increase_speed()
        self.ball_loop = self.root.after(20, self.move_ball)

    def restart_game(self):
        """Reset everything and restart the game."""
        if self.ball_loop:
            self.root.after_cancel(self.ball_loop)  # Stop ball movement loop
        self.init_game()  # Reset game elements
        self.move_ball()  # Restart ball movement

# Run the game
root = tk.Tk()
game = PingPongGame(root)
root.mainloop()