#_*_ coding:utf-8_*_  

class GameStats():
    """追踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        #让游戏刚启动时处于非活动状态
        self.game_active = False
        #在任何情况下都不应重置最高得分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit #剩余的本船人头数
        self.score = 0
        self.level = 1
