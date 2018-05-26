#_*_ coding:utf-8_*_  
import pygame.font #使pygame能够将文本渲染到屏幕上
# play 按钮的相关设置

class Button():

    def __init__(self, ai_settings, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # 设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.button_color = (1,25,53)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        
        #创建表示按钮的rect对象,并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        
        # 按钮的标签只需创建一次
        self.prep_msg(msg)
		
    def prep_msg(self,msg):
        """将msg渲染成图像并使其在按钮上居中"""
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect() # 根据文本信息创建一个rect
        self.msg_image_rect.center = self.rect.center #将center属性设置为按钮的center的属性

    def draw_button(self):
        # 绘制一个用颜色填充的按钮,再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
