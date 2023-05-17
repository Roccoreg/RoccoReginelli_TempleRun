# File created by Rocco Reginelli
# (Kids can code) https://www.youtube.com/watch?v=9S7fWevICtY&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq&index=13
import pygame as pg
import os
import random
from random import randint
from settings import *
from sprites import *
from os import path
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(game_folder, "sounds")

class Game: 
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode ((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        

    def load_data(self):
        self.player_img = pg.image.load(path.join(img_folder, "doodler.png")).convert()
        self.coin_img= pg.image.load(path.join(img_folder, "coin.png")).convert()
        self.cheddy_sound= pg.mixer.Sound(path.join(snd_folder, "recording.mp3"))

        
    def new(self):
        # start a new game
        self.score = 0
        self.score_coin = 0
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
        # self.coin = Coin(self, WIDTH/2, HEIGHT/2)
        self.all_sprites.add(self.player)
        # self.all_sprites.add(self.coin)
        # self.coins.add(self.coin)
        pg.mixer.music.load(path.join(snd_folder, "sound.mp3"))
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
            if randint(0,1) > 0:
                c = Coin(self, p.rect.x, p.rect.y)
                self.all_sprites.add(c)
                self.coins.add(c)
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # if player reaches top 1/2 of screen then screen scrolls down revealing more blocks on the top
        if self.player.rect.top <= HEIGHT / 2:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 1
            for c in self.coins:
                c.rect.y += abs(self.player.vel.y)
                if c.rect.top >= HEIGHT:
                    c.kill()

        coin_hits = pg.sprite.spritecollide(self.player, self.coins, True)
        if coin_hits:
            self.score_coin += 1
            pg.mixer.Sound(self.cheddy_sound).play()
            print(self.score_coin)            

        # If player dies
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

           # spawn new platforms to keep same average number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-50, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)
            # add new randomly placed coins when platforms are created
            if randint(0,1) > 0:
                c = Coin(self, p.rect.x-(randint(-70,70)), p.rect.y-(randint(-70,70)))
                self.all_sprites.add(c)
                self.coins.add(c)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
        
    def draw(self):
        # Game loop
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.draw_text(str(self.score_coin), 22, WHITE, WIDTH / 2 + 200, 15)
        
        # flips the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to Jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Collect the Coins", 22, WHITE, WIDTH / 2 , HEIGHT * 3 / 4 - 80)
        self.draw_text("Game Score", 22, WHITE, WIDTH / 2 , HEIGHT / 2 - 250)
        self.draw_text("__", 22, WHITE, WIDTH / 2 , HEIGHT / 2 - 280)
        self.draw_text("__", 22, WHITE, WIDTH / 2 + 180 , HEIGHT / 2 - 280)
        self.draw_text("Coin Score", 22, WHITE, WIDTH / 2 + 180 , HEIGHT / 2 - 250)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Coins Collected: " + str(self.score_coin), 22, WHITE, WIDTH / 2, HEIGHT / 2 - 40)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()