#_*_ coding:utf-8_*_  
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        #初始化飞船,screen参数指定了飞船要绘制到什么位置
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings 

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')#这里用的是相对路径 pygame.image.load（）支持jpg,png,gif,bmp,pcx,tif,tga等多种图片格式 绝对路径 r"C:\Users\clemente\PycharmProjects\untitled2\shipx.png"
        self.rect = self.image.get_rect()#把图像当作矩形对象一样处理
        self.screen_rect = screen.get_rect() #把表示屏幕的矩形存储在self.screen_rect中

        #每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx #飞船中心的x坐标赋值为屏幕矩形的centerx中心(属性)
        self.rect.bottom = self.screen_rect.bottom #飞船下边缘的Y坐标赋值为屏幕矩形的bottom位置(属性) 如果要改为位于图像中心 bottom改为centery
        self.center_x = float(self.rect.centerx)#在飞船的属性水平坐标center中储存小数值
        self.center_y= float(self.rect.centery) #在飞船的属性垂直坐标bottom中储存小数值
        
        #移动状态开关
        self.moving_right = False #在方法__init__()中我们添加了属性self.moving_right,并将初始值设置为False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """根据移动标志调整飞船的位置"""
        """当self.moving_right返回值为True时向右移动飞船 这里的参数在game_fuctions20180519.py中修改 
        and 后面 链接的是不超出右边界调节 self.rect.right 返回飞船外接矩形的右边缘x坐标,如果这个值小于self.screen_rect.right的值
        就说明飞船未触及屏幕的左边缘,这确保仅当飞船在画布内,才调整self.center的值"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed_factor #向右移动self.ship_speed_factor的返回值
        if self.moving_left and self.rect.left > 0: #如上同理
            self.center_x -= self.ai_settings.ship_speed_factor
        """上下移动"""
        if self.moving_up and self.rect.top > 0:
            self.center_y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center_x #根据self.center更新rect对象
        self.rect.centery = self.center_y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect) #用blit()方法在screen上绘制self.image和self.rect
