# coding=utf-8
import pygame
from pygame.sprite import Sprite
"""除了位置不同以外,这个类大多数的代码都与ship类相似"""
class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像,并设置其rect属性
        self.image = pygame.image.load('images/alien.png')#要用绝对路径可换为r"C:\Users\clemente\PycharmProjects\untitled2\alien.png"
        self.rect = self.image.get_rect()

        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width #我们将每个那个人的左边距都设置为外星人的一个宽度单位
        self.rect.y = self.rect.height # 顶边距离设置为外星人的矩形高度

        #存储外星人准确的位置
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right: #外星人右边缘 大于等于 屏幕矩形的右边缘
            return True #返回1
        elif self.rect.left <= 0: #外星人左边缘 小于等于 屏幕矩形的最左边 即0坐标
            return True #返回1
        
    def update(self):
        """向左或右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction) #因为fleet_direction 向右移动为1 向左移动为-1 由此控制外星人x坐标增减
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
	