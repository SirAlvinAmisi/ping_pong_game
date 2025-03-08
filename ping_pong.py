import tkinter as tk

class Paddle:
    def __init__(self, canvas, x_position):
        # Initialize the paddle with a rectangle on the canvas
        self.canvas = canvas
        self.paddle = canvas.create_rectangle(x_position, 150, x_position + 10, 250, fill="white")
    
    def move(self, direction):
        # Move the paddle up or down while staying inside the canvas
        paddle_coords = self.canvas.coords(self.paddle)
        if direction == "up" and paddle_coords[1] > 0:
            self.canvas.move(self.paddle, 0, -20)
        elif direction == "down" and paddle_coords[3] < 400:
            self.canvas.move(self.paddle, 0, 20)

class Ball:
    def __init__(self, canvas):
        # Initialize the ball in the center with a set speed
        self.canvas = canvas
        self.ball = canvas.create_oval(290, 190, 310, 210, fill="white")
        self.dx = 3  # Speed in the x-direction
        self.dy = 3  # Speed in the y-direction
        self.hit_count = 0  # Track the number of times the ball hits a paddle
    
    def move(self):
        # Move the ball in its current direction
        self.canvas.move(self.ball, self.dx, self.dy)
        ball_coords = self.canvas.coords(self.ball)
        
        # Check for collision with top and bottom walls
        if ball_coords[1] <= 0 or ball_coords[3] >= 400:
            self.dy = -self.dy  # Reverse direction on vertical collision
        
        return ball_coords  # Return updated coordinates for further processing
    
    def increase_speed(self):
        # Increase ball speed after every 7 paddle hits
        if self.hit_count >= 7:
            self.dx *= 1.1  # Increase speed slightly
            self.dy *= 1.1
            self.hit_count = 0  # Reset counter
    
    def reset_position(self):
        # Reset ball to the center when a player scores
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        self.dx = 3  # Reset speed to default
        self.dy = 3
        self.hit_count = 0

class PingPongGame:
    def __init__(self, root):
        # Initialize the main game window
        self.root = root
        self.root.title("Ping Pong Game")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()
        
        # Create paddles, ball, and score tracking
        self.paddle_1 = Paddle(self.canvas, 20)
        self.paddle_2 = Paddle(self.canvas, 570)
        self.ball = Ball(self.canvas)
        self.player_1_score = 0
        self.player_2_score = 0
        self.max_score = 5
        self.game_over = False
        self.ball_loop = None  # Store the loop ID to cancel later
        
        # Display the score at the top
        self.score_display = self.canvas.create_text(300, 20, text="Player 1: 0   Player 2: 0", font=("Arial", 14), fill="white")
        
        # Create restart button inside the canvas
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.restart_game)
        self.restart_button_window = self.canvas.create_window(300, 50, window=self.restart_button)
        
        # Bind controls to move paddles
        self.root.bind("<w>", lambda event: self.paddle_1.move("up"))
        self.root.bind("<s>", lambda event: self.paddle_1.move("down"))
        self.root.bind("<Up>", lambda event: self.paddle_2.move("up"))
        self.root.bind("<Down>", lambda event: self.paddle_2.move("down"))
        
        # Start the game loop
        self.move_ball()
    
    def update_score(self):
        # Update the on-screen score when a player scores
        self.canvas.itemconfig(self.score_display, text=f"Player 1: {self.player_1_score}   Player 2: {self.player_2_score}")
    
    def display_winner(self, winner):
        # Show the winner and stop the game
        self.game_over = True
        self.canvas.create_text(300, 200, text=f"{winner} Wins!", font=("Arial", 24), fill="red")
    
    def move_ball(self):
        if self.game_over:
            return  # Stop the game if there's a winner
        
        ball_coords = self.ball.move()
        paddle_1_coords = self.canvas.coords(self.paddle_1.paddle)
        paddle_2_coords = self.canvas.coords(self.paddle_2.paddle)
        
        # Check for paddle collision and reverse direction
        if ball_coords[0] <= 30 and paddle_1_coords[1] < ball_coords[3] and paddle_1_coords[3] > ball_coords[1]:
            self.ball.dx = -self.ball.dx
            self.ball.hit_count += 1  # Track paddle hits
        
        if ball_coords[2] >= 570 and paddle_2_coords[1] < ball_coords[3] and paddle_2_coords[3] > ball_coords[1]:
            self.ball.dx = -self.ball.dx
            self.ball.hit_count += 1  # Track paddle hits
        
        # If ball goes past left edge, Player 2 scores
        if ball_coords[0] <= 0:
            self.player_2_score += 1
            self.update_score()
            if self.player_2_score >= self.max_score:
                self.display_winner("Player 2")
            else:
                self.ball.reset_position()
        
        # If ball goes past right edge, Player 1 scores
        if ball_coords[2] >= 600:
            self.player_1_score += 1
            self.update_score()
            if self.player_1_score >= self.max_score:
                self.display_winner("Player 1")
            else:
                self.ball.reset_position()
        
        # Check if it's time to increase speed
        self.ball.increase_speed()
        
        # Schedule the next ball movement update
        self.ball_loop = self.root.after(20, self.move_ball)
    
    def restart_game(self):
        # Stop current game loop
        if self.ball_loop:
            self.root.after_cancel(self.ball_loop)
        
        # Reset everything for a new game
        self.player_1_score = 0
        self.player_2_score = 0
        self.update_score()
        self.game_over = False
        self.ball.reset_position()
        
        # Move paddles back to their starting positions
        self.canvas.coords(self.paddle_1.paddle, 20, 150, 30, 250)
        self.canvas.coords(self.paddle_2.paddle, 570, 150, 580, 250)
        
        # Restart the ball movement
        self.move_ball()

# Run the game
root = tk.Tk()
game = PingPongGame(root)
root.mainloop()
