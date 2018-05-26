#_*_ coding:utf-8_*_  
class Settings():
    """储存<外星人入侵>的所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width = 1200 #画布大小
        self.screen_height = 800
        self.bg_color =(0,69,108)  #画布颜色
        #本船设置

        self.ship_limit = 3 #玩家拥有的本船人头数(生命)
        #子弹设置

        self.bullet_width = 3
        self.bullet_height = 22
        self.bullet_color = 179,214,110
        self.bullets_allowed = 7 #同屏最多子弹数量
        #外星人移动相关设置

        self.fleet_drop_speed = 10 #外星人碰到左右边缘时然后向下移动的速度


        # 游戏节奏速度加快系数
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1  # 舰群向左或者向右移动的方向 1表示向右 -1表示向左
        #记分
        self.alien_points = 50

    def increase_speed(self):
        """提高下面三种游戏对象的速度"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_facctor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


