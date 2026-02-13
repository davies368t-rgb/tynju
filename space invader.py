import math
import random
import pygame

sw = 800
sh = 500
psx = 370
psy = 380
esy_mi = 50
esy_ma = 150
esx = 4
esy = 40
bsy = 10
cd = 27

pygame.init()

screen = pygame.display.set_mode((sw,sh))
background = pygame.image.load('s_background.png')

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)

p_im = pygame.image.load('player.png')
px = psx
py = psy
px_c = 0

e_im = []
ex = []
ey = []
ex_c = []
ey_c = []
num_e = 6

for i in range(num_e):
    e_im.append(pygame.image.load('enemy.png'))
    ex.append(random.randint(0,sw - 64))
    ey.append(random.randint(esy_mi,esy_ma))
    ex_c.append(esx)
    ey_c.append(esy)

b_im = pygame.image.load('bullet.png')
bx = 0
by = psy
bx_c = 0
by_c = bsy
b_state = "ready"

sv = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

o_font = pygame.font.Font('freesansbold.ttf',64)

def sc(x,y):
    score = font.render("Score: "+str(sv),True,(255,255,255))
    screen.blit(score,(x,y))

def g_o():
    o_t = o_font.render("GAME OVER",True,(255,255,255))
    screen.blit(o_t,(200,250))

def p(x,y):
    screen.blit(p_im,(x,y))

def e(x,y,i):
    screen.blit(e_im[i],(x,y))

def f_b(x,y):
    global b_state
    b_state = "fire"
    screen.blit(b_im,(x+16,y+10))

def is_col(ex,ey,bx,by):
    distance = math.sqrt((ex-bx)**2+(ey-by)**2)
    return distance < cd

run = True
while run:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_c = -5
            if event.key == pygame.K_RIGHT:
                px_c = 5
            if event.key == pygame.K_SPACE and b_state == "ready":
                bx = px
                f_b(bx,by)
        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            px_c = 0

    px += px_c
    px = max(0,min(px,sw-64))

    for j in range(num_e):
        if ey[j] > 340:
            for k in range(num_e):
                ey[k] = 2000
            g_o()
            break

        ex[j] += ex_c[j]
        if ex[j] <= 0 or ex[j] >= sw - 64:
            ex_c[j] *= -1
            ey[j] += ey_c[j]

        if is_col(ex[j],ey[j],bx,by):
            by = psy
            b_state = "ready"
            sv += 1
            ex[j] = random.randint(0,sw-64)
            ey[j] = random.randint(esy_mi,esy_ma)

        e(ex[j],ey[j],j)

    if by <= 0:
        by = psy
        b_state = "ready"
    elif b_state == "fire":
        f_b(bx,by)
        by -= by_c

    p(px,py)
    sc(textX,textY)
    pygame.display.update()