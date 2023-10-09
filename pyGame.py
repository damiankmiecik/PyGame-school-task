import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hopsachu')

tile_size = 50
gameover = 0

bg_img = pygame.image.load('img/sky1.png')

#def draw_grid():
#    for line in range(0, 20):
#        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
#        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('img/pikachu.png')
        self.image = pygame.transform.scale(img, (50, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump = False
        

    def update(self, gameover):
        dx = 0
        dy = 0
        
        if gameover == 0:    
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jump == False:
                self.vel_y = -10
                self.jump = True
            if key[pygame.K_SPACE] == False:
                self.jump = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5
            
            
            self.vel_y += 1
            if self.vel_y > 5:
                self.vel_y = 5
            dy += self.vel_y
            
            
            for tile in world.tile_list: #tile[1] = data, tile[0] = image
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            
            
            if pygame.sprite.spritecollide(self, monster_group, False):
                gameover = -1
                
            if pygame.sprite.spritecollide(self, ivy_low_group, False):
                gameover = -1
            
            if pygame.sprite.spritecollide(self, ivy_high_group, False):
                gameover = -1    
            
            if pygame.sprite.spritecollide(self, gate_group, False):
                gameover = -1         
                
            print(gameover)
            
                    
            self.rect.x += dx
            self.rect.y += dy
            
            
                
        #    if self.rect.bottom > screen_height:
        #        self.rect.bottom = screen_height
        #        dy = 0
            
            
            screen.blit(self.image, (self.rect.x, self.rect.y))
        #    pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
            
            return gameover

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    monster = Enemy(col_count * tile_size, row_count * tile_size)
                    monster_group.add(monster)    
                if tile == 4:
                    ivy_high = Ivy(col_count * tile_size, row_count * tile_size)
                    ivy_high_group.add(ivy_high)
                if tile == 5:
                    gate = Gate(col_count * tile_size, row_count * tile_size)   
                    gate_group.add(gate) 
                if tile == 6:
                    ivy_low = Ivy(col_count * tile_size, row_count * tile_size + 25)
                    ivy_low_group.add(ivy_low)       
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/monster.png')
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = 2
        self.move_counter = 0


    def update(self):
        self.rect.x += self.move
        self.move_counter += 1
        if self.move_counter == 100:
            self.move *= -1
            self.move_counter = 0

class Ivy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/ivy.png')
        self.image = pygame.transform.scale(img, (50, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y      

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/gate.png')
        self.image = pygame.transform.scale(img, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        
        
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 0, 0, 0, 5, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 6, 6, 2, 2, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
[1, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1], 
[1, 2, 2, 6, 6, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 140)

monster_group = pygame.sprite.Group()
ivy_low_group = pygame.sprite.Group()
ivy_high_group = pygame.sprite.Group()
gate_group = pygame.sprite.Group()

world = World(world_data)


run = True
while run:
    clock.tick(fps)
    
    screen.blit(bg_img, (0, 0))

    world.draw()
    
    if gameover == 0:
        monster_group.update()
    
    monster_group.draw(screen)
    ivy_low_group.draw(screen)
    ivy_high_group.draw(screen)
    gate_group.draw(screen)
    

    gameover = player.update(gameover)


    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()