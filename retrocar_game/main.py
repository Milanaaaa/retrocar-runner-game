import pygame
import random

pygame.init()
pygame.display.set_icon(pygame.image.load("runner_images/icon.png"))
win = pygame.display.set_mode((500, 500))
screen = pygame.Surface((400, 400))

pygame.display.set_caption('Cubes Game')
clock = pygame.time.Clock()

bg = pygame.image.load('runner_images/bg.png')
walkRight = [pygame.image.load('runner_images/car1.png'),
             pygame.image.load('runner_images/car2.png'),
             pygame.image.load('runner_images/car3.png'),
             pygame.image.load('runner_images/car1.png'),
             pygame.image.load('runner_images/car2.png'),
             pygame.image.load('runner_images/car3.png')]

moneyPic = [pygame.image.load('runner_images/coin1.png'), pygame.image.load(
    'runner_images/coin2.png'),
            pygame.image.load('runner_images/coin3.png'), pygame.image.load(
        'runner_images/coin4.png'),
            pygame.image.load('runner_images/coin5.png'), pygame.image.load(
        'runner_images/coin6.png'),
            pygame.image.load('runner_images/coin7.png'), pygame.image.load(
        'runner_images/coin8.png'),
            pygame.image.load('runner_images/coin9.png'), pygame.image.load(
        'runner_images/coin10.png')]

starPic = [pygame.image.load('runner_images/star1.png'), pygame.image.load(
    'runner_images/star2.png'),
           pygame.image.load('runner_images/star3.png'), pygame.image.load(
        'runner_images/star4.png'),
           pygame.image.load('runner_images/star5.png'), pygame.image.load(
        'runner_images/star6.png'),
           pygame.image.load('runner_images/star7.png'), pygame.image.load(
        'runner_images/star8.png'),
           pygame.image.load('runner_images/star9.png'), pygame.image.load(
        'runner_images/star10.png')]

X = 40
Y = 425
WIDTH = 60
HEIGHT = 71
speed = 5

isJump = False
jumpCount = 13

right = False
animCount = 0
lastMove = 'right'
scoreCount = 0
my_font = pygame.font.SysFont('monospace', 15)


def inter(self_x1, self_y1, self_x2, self_y2, other_x1, other_y1, other_x2, other_y2):
    if any([all([other_x1 <= self_x1 <= other_x2, other_y1 <= self_y1 <= other_y2]),
            all([other_x1 <= self_x2 <= other_x2, other_y1 <= self_y1 <= other_y2]),
            all([other_x1 <= self_x1 <= other_x2, other_y1 <= self_y2 <= other_y2]),
            all([other_x1 <= self_x2 <= other_x2, other_y1 <= self_y2 <= other_y2])]):
        return True
    return False


def drawWindow():
    global animCount, win, obstacles, coins, string, string2, string0, star, won
    win.blit(bg, (0, 0))

    if animCount + 1 >= 30:
        animCount = 0
    if won:
        win.blit(starPic[animCount // 5], (star.x, star.y))
    win.blit(walkRight[animCount // 5], (X, Y))
    for c in coins:
        win.blit(moneyPic[animCount // 5], (c.x, c.y))
    animCount += 1

    for o in obstacles:
        # print(o.x, o.y)
        # win.blit(pygame.image.load('runner_images/test.png'), (o.x, o.y))
        pygame.draw.rect(win, o.color, ((o.x, o.y), (o.width, o.height)))

    win.blit(string0, (0, 30))
    win.blit(string, (0, 50))
    win.blit(string2, (0, 70))

    pygame.display.update()


class Obstacle:
    def __init__(self):
        self.height = random.randrange(5, 160)
        self.width = random.randrange(5, 50)
        self.color = self.color = random.choice(
            ((66, 170, 255), (255, 255, 0), (0, 255, 255), (253, 233, 16), (255, 163, 67),
             (255, 73, 108), (102, 0, 255), (153, 50, 204)))
        self.x = 500 - self.width
        self.y = 500 - self.height


class Coin:
    def __init__(self):
        self.x = 500
        self.y = 500 - 73


class Star:
    def __init__(self):
        self.x = random.randrange(30, 450)
        self.y = random.randrange(20, 450)


obstacles = []
coins = []
count = 0
allCoins = 0
string2 = my_font.render('', 0, (0, 255, 0))
run = True
gameOver = False
won = False
obstCount = 0
needObstToWon = 10
star = 0
while run:
    clock.tick(30)
    pygame.time.delay(10)  # цикл выполняется каждую сотую секунды

    if len(obstacles) + len(coins) < 1 and gameOver is False and won is False:
        if random.choice((True, False)) is True:
            obstacles.append(Obstacle())
        else:
            coins.append(Coin())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    for o in obstacles:
        o.x -= 12
        if not gameOver and (o.x + o.width) <= 0:
            obstCount += 1
        if o.x + o.width < 0:
            obstacles.pop(obstacles.index(o))
            o.x = 1000
            o.y = 1000
        if inter(o.x, o.y, o.x + o.width, o.y + o.height, X, Y, X + 180, Y + 159):
            if (count - 5) < 0:
                string2 = my_font.render('GAME OVER', 0, (255, 0, 0))
                gameOver = True
            else:
                obstCount += 1
                o.x = 1000
                o.y = 1000
                obstacles.pop(obstacles.index(o))
                count -= 5

    for c in coins:
        c.x -= 12
        if inter(c.x, c.y, c.x + 73, c.y + 73, X, Y, X + 180, Y + 159):
            coins.pop(coins.index(c))
            c.x = 1000
            c.y = 1000
            count += 1
            allCoins += 1
        if c.x <= 0:
            coins.pop(coins.index(c))
            c.x = 1000
            c.y = 1000
            allCoins += 1

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -13:
            if jumpCount < 0:
                Y += (jumpCount ** 2) / 1.8
            else:
                Y -= (jumpCount ** 2) / 1.8
            jumpCount -= 1

        else:
            isJump = False
            jumpCount = 13
    string0 = my_font.render('Passed: ' + str(obstCount) + '/' + str(needObstToWon), 0, (0, 0, 255))
    string = my_font.render('Coins: ' + str(count), 0, (0, 255, 0))

    if obstCount == needObstToWon:
        won = True
        string2 = my_font.render('!YOU WON!', 0, (255, 0, 0))

    if won is True:
        star = Star()

    drawWindow()

pygame.quit()
