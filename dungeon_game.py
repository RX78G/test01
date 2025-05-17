import random

WIDTH = 5
HEIGHT = 5
HEALTH_START = 10
TREASURES = 3
MONSTERS = 3

MOVES = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}

def generate_board():
    board = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    positions = set()
    def random_pos():
        while True:
            pos = (random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1))
            if pos not in positions:
                positions.add(pos)
                return pos
    exit_pos = random_pos()
    board[exit_pos[1]][exit_pos[0]] = 'X'
    for _ in range(MONSTERS):
        x, y = random_pos()
        board[y][x] = 'M'
    for _ in range(TREASURES):
        x, y = random_pos()
        board[y][x] = 'T'
    start_pos = random_pos()
    return board, start_pos, exit_pos

def print_board(board, player):
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if (x, y) == player:
                row.append('P')
            else:
                cell = board[y][x]
                if cell == 'M':
                    row.append('.')
                else:
                    row.append(cell)
        print(' '.join(row))
    print()


def main():
    board, player, exit_pos = generate_board()
    health = HEALTH_START
    score = 0
    print("Welcome to Dungeon Adventure! Reach 'X' to escape.")
    while True:
        print_board(board, player)
        print(f"Health: {health}  Score: {score}")
        move = input("Move (WASD): ").strip().lower()
        if move not in MOVES:
            print("Invalid move. Use W/A/S/D keys.")
            continue
        dx, dy = MOVES[move]
        nx, ny = player[0] + dx, player[1] + dy
        if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
            print("You hit a wall!")
            continue
        player = (nx, ny)
        cell = board[ny][nx]
        if cell == 'X':
            print("You found the exit! You win!")
            print(f"Final score: {score}")
            break
        elif cell == 'T':
            score += 1
            board[ny][nx] = '.'
            print("You found a treasure!")
        elif cell == 'M':
            if random.random() < 0.5:
                board[ny][nx] = '.'
                print("You defeated a monster!")
            else:
                health -= 5
                print("The monster hit you!")
                if health <= 0:
                    print("You have perished in the dungeon...")
                    break
    print("Thanks for playing!")

if __name__ == '__main__':
    main()
