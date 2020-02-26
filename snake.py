import sys, random, pygame, tkinter as tk
from tkinter import messagebox


SIZE = 500
ROWS = 20
snake = None
snack = None


class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=1, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(width, rows, surface):
    squareSize = width // rows

    x, y = 0, 0
    for l in range(rows):
        x = x + squareSize
        y = y + squareSize

        pygame.draw.line(surface, (255,255,255), (x, 0), (x, width))
        pygame.draw.line(surface, (255,255,255), (0, y), (width, y))


def redrawWindow(surface):
    global ROWS, SIZE, snake, snack
    surface.fill((0,0,0))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(SIZE, ROWS, surface)
    pygame.display.update()


def randomSnack(item):
    global ROWS
    positions = item.body
    while True:
        x = random.randrange(ROWS)
        y = random.randrange(ROWS)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global SIZE, ROWS, snake, snack
    win = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption('Snake by kirsirinnesalo')
    
    snake = snake((255,0,0), (10,10))
    snack = cube(randomSnack(snake), color=(0,255,0))
    
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)   #the lower delay is the faster it goes
        clock.tick(10)          #fps, the lower tick is the slower its gona be
        snake.move()
        
        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = cube(randomSnack(snake), color=(0,255,0))
        
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z:z.pos, snake.body[x+1:])):
                message_box('Hävisit!', 'Sait {} pistettä.\n\nPelaa uudelleen...'.format(len(snake.body)))
                snake.reset((10,10))
                break

        redrawWindow(win)

    pass


if __name__ == '__main__':
    pygame.init()
    main()

