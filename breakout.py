import tkinter as tk

WIDTH, HEIGHT = 800, 600
BRICK_ROWS = 3
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 15

class Breakout:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Breakout")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", text="Score: 0")

        paddle_y = HEIGHT - 40
        self.paddle = self.canvas.create_rectangle(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT, fill="blue")
        self.canvas.move(self.paddle, (WIDTH - PADDLE_WIDTH) / 2, paddle_y)

        start_x = WIDTH / 2 - BALL_SIZE / 2
        start_y = paddle_y - BALL_SIZE - 5
        self.ball = self.canvas.create_oval(start_x, start_y, start_x + BALL_SIZE, start_y + BALL_SIZE, fill="white")
        self.ball_dx = 4
        self.ball_dy = -4

        self.bricks = []
        colors = ["red", "orange", "yellow"]
        for row in range(BRICK_ROWS):
            y1 = 50 + row * BRICK_HEIGHT
            for col in range(BRICK_COLS):
                x1 = col * BRICK_WIDTH
                rect = self.canvas.create_rectangle(x1, y1, x1 + BRICK_WIDTH - 2, y1 + BRICK_HEIGHT - 2, fill=colors[row % len(colors)], width=1)
                self.bricks.append(rect)

        master.bind("<Motion>", self.move_paddle)
        self.running = True
        self.update()

    def move_paddle(self, event: tk.Event) -> None:
        x = event.x
        x1 = x - PADDLE_WIDTH / 2
        x1 = max(min(x1, WIDTH - PADDLE_WIDTH), 0)
        y1, y2 = self.canvas.coords(self.paddle)[1], self.canvas.coords(self.paddle)[3]
        self.canvas.coords(self.paddle, x1, y1, x1 + PADDLE_WIDTH, y2)

    def update(self) -> None:
        if not self.running:
            return
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx = -self.ball_dx
        if y1 <= 0:
            self.ball_dy = -self.ball_dy
        if y2 >= HEIGHT:
            self.running = False
            self.canvas.create_text(WIDTH / 2, HEIGHT / 2, fill="white", text="Game Over", font=("Arial", 24))
            return

        paddle_coords = self.canvas.coords(self.paddle)
        if self._overlap(paddle_coords, (x1, y1, x2, y2)):
            self.ball_dy = -abs(self.ball_dy)

        hit_brick = None
        for brick in self.bricks:
            if self._overlap(self.canvas.coords(brick), (x1, y1, x2, y2)):
                hit_brick = brick
                break
        if hit_brick:
            self.bricks.remove(hit_brick)
            self.canvas.delete(hit_brick)
            self.ball_dy = -self.ball_dy
            self.score += 1
            self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
            if not self.bricks:
                self.running = False
                self.canvas.create_text(WIDTH / 2, HEIGHT / 2, fill="white", text="You Win!", font=("Arial", 24))
                return

        self.master.after(16, self.update)

    @staticmethod
    def _overlap(a, b) -> bool:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

if __name__ == "__main__":
    root = tk.Tk()
    Breakout(root)
    root.mainloop()
