#_*_ coding:utf-8_*_  
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    
    pygame.init() #初始化游戏背景设置
    ai_settings = Settings() #创建一个Settings实例 并储存在变量ai_settings中
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) #创建一个屏幕对象 调用类Settings()中的参数
    pygame.display.set_caption("小航海时代 made by clemente")
    
    play_button = Button(ai_settings, screen, "Play")#创建Play按钮实例
    
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats) #创建记分牌
    
    #实例化一艘飞船
    ship = Ship(ai_settings, screen)
    bullets = Group()#创建一个用于储存子弹的编组
    aliens = Group()#创造外星人编组
    
    #创造外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #游戏主循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
