import tkinter as tk
import random

WIDTH = 400
HEIGHT = 600
BIRD_SIZE = 20
PIPE_WIDTH = 60
GAP_SIZE = 180
PIPE_INTERVAL = 2500  # milliseconds
GRAVITY = 0.3
FLAP_STRENGTH = -8
UPDATE_DELAY = 20  # milliseconds

class FlappyBird:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("Flappy Bird")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.bird = self.canvas.create_oval(0, 0, BIRD_SIZE, BIRD_SIZE, fill="yellow")
        self.canvas.move(self.bird, WIDTH / 4, HEIGHT / 2)
        self.vel_y = 0

        self.pipes: list[tuple[int, int, int, int]] = []
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="black", text="Score: 0", font=("Arial", 16))

        self.started = False
        self.game_over = False
        self.game_over_text = None
        self.start_text = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="Press Space to Start",
            fill="white",
            font=("Arial", 24),
        )

        master.bind("<space>", self.handle_space)

    def handle_space(self, _event: tk.Event) -> None:
        if not self.started:
            self.started = True
            self.canvas.delete(self.start_text)
            self.spawn_pipe()
            self.update()
            return
        if self.game_over:
            self.reset()
            return
        self.flap()

    def flap(self) -> None:
        if not self.game_over and self.started:
            self.vel_y = FLAP_STRENGTH

    def reset(self) -> None:
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
        self.canvas.delete("pipe")
        self.pipes.clear()
        self.canvas.coords(self.bird, 0, 0, BIRD_SIZE, BIRD_SIZE)
        self.canvas.move(self.bird, WIDTH / 4, HEIGHT / 2)
        self.vel_y = 0
        self.score = 0
        self.canvas.itemconfigure(self.score_text, text="Score: 0")
        self.started = False
        self.game_over = False
        self.start_text = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="Press Space to Start",
            fill="white",
            font=("Arial", 24),
        )

    def spawn_pipe(self) -> None:
        if not self.started or self.game_over:
            return
        gap_y = random.randint(100, HEIGHT - 100 - GAP_SIZE)
        top_pipe = self.canvas.create_rectangle(
            WIDTH,
            0,
            WIDTH + PIPE_WIDTH,
            gap_y,
            fill="green",
            tags="pipe",
        )
        bottom_pipe = self.canvas.create_rectangle(
            WIDTH,
            gap_y + GAP_SIZE,
            WIDTH + PIPE_WIDTH,
            HEIGHT,
            fill="green",
            tags="pipe",
        )
        self.pipes.append((top_pipe, bottom_pipe))
        self.master.after(PIPE_INTERVAL, self.spawn_pipe)

    def update(self) -> None:
        if self.game_over or not self.started:
            return

        # Apply gravity
        self.vel_y += GRAVITY
        self.canvas.move(self.bird, 0, self.vel_y)
        bx1, by1, bx2, by2 = self.canvas.coords(self.bird)

        # Move pipes
        passed_pipes = []
        for top, bottom in self.pipes:
            self.canvas.move(top, -2, 0)
            self.canvas.move(bottom, -2, 0)
            tx1, _, tx2, _ = self.canvas.coords(top)
            if tx2 < 0:
                passed_pipes.append((top, bottom))
            elif tx2 < bx1 and not self.canvas.gettags(top):
                self.canvas.itemconfig(top, tags="counted")
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")

        for pipe in passed_pipes:
            self.pipes.remove(pipe)
            self.canvas.delete(pipe[0])
            self.canvas.delete(pipe[1])

        # Collision detection
        if by1 <= 0 or by2 >= HEIGHT:
            self.end_game()
            return
        for top, bottom in self.pipes:
            if self._overlap(self.canvas.coords(top), (bx1, by1, bx2, by2)) or \
               self._overlap(self.canvas.coords(bottom), (bx1, by1, bx2, by2)):
                self.end_game()
                return

        self.master.after(UPDATE_DELAY, self.update)

    def end_game(self) -> None:
        self.game_over = True
        self.started = False
        self.game_over_text = self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="Game Over - Press Space to Restart",
            fill="red",
            font=("Arial", 24),
        )

    @staticmethod
    def _overlap(a, b) -> bool:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

if __name__ == "__main__":
    root = tk.Tk()
    FlappyBird(root)
    root.mainloop()
