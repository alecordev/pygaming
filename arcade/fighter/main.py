import random

from pygame.locals import *

from entity import *

background_img = "resources/images/background.png"
shoot_img = "resources/images/shoot.png"
game_over = pygame.image.load("resources/images/gameover.png")

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

shoot_frequency = 0
enemy_frequency = 0
enemy2_frequency = 0
player_down_index = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

background = pygame.image.load(background_img)

all_shoot = pygame.image.load(shoot_img)

player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))  # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(all_shoot, player_rect, player_pos)

bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = all_shoot.subsurface(bullet_rect)

enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = all_shoot.subsurface(enemy1_rect)

enemy1_down_imgs = []
enemy1_down_imgs.append(all_shoot.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(all_shoot.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(all_shoot.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(all_shoot.subsurface(pygame.Rect(930, 697, 57, 43)))

enemy2_rect = pygame.Rect(430, 520, 71, 108)
enemy2_img = all_shoot.subsurface(enemy2_rect)
enemy2_down_imgs = []
enemy2_down_imgs.append(all_shoot.subsurface(pygame.Rect(533, 655, 71, 108)))
enemy2_down_imgs.append(all_shoot.subsurface(pygame.Rect(602, 648, 71, 105)))
enemy2_down_imgs.append(all_shoot.subsurface(pygame.Rect(672, 648, 71, 105)))
enemy2_down_imgs.append(all_shoot.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

enemies_down = pygame.sprite.Group()

clock = pygame.time.Clock()
score = 0
Level = 1
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    if Level > 2:
        num = random.randint(1, 3)
        for num in range(1, num):
            enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect.width), 0]
            enemy2 = Enemy(enemy2_img, enemy2_down_imgs, enemy2_pos)
            enemies1.add(enemy2)
            enemy2_frequency += 1
            if enemy2_frequency >= 50:
                enemy2_frequency = 0

    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:
        enemy.move()

        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
        if enemy.rect.top < 0:
            enemies1.remove(enemy)

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    screen.fill(0)
    screen.blit(background, (0, 0))

    if not player.is_hit:
        screen.blit(player.images[int(player.img_index)], player.rect)
        player.img_index = shoot_frequency / 8
    else:
        player.img_index = player_down_index / 8
        screen.blit(player.images[int(player.img_index)], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
            # enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 100
            if score > 1000:
                Level = score / 1000 + 1
            continue
        screen.blit(
            enemy_down.down_image[int(enemy_down.down_index / 2)], enemy_down.rect
        )
        enemy_down.down_index += 1

    player.bullets.draw(screen)
    enemies1.draw(screen)

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    level_font = pygame.font.Font(None, 36)
    level_text = score_font.render("Level:" + str(Level), True, (128, 128, 128))
    level_rect = level_text.get_rect()
    level_rect.topleft = [370, 10]
    screen.blit(level_text, level_rect)

    pygame.display.update()

    key_presslist = pygame.key.get_pressed()
    if key_presslist[K_UP]:
        player.moveUp()
    if key_presslist[K_DOWN]:
        player.moveDown()
    if key_presslist[K_LEFT]:
        player.moveLeft()
    if key_presslist[K_RIGHT]:
        player.moveRight()
