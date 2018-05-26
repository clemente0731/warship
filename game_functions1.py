# coding=utf-8
"""在主程序中不再需要import sys,因为本模块中已经使用了它"""
import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT: # 这里用elif代码块是因为每个事件都只与一个键相关联,不存在冲突
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
	# 添加一个结束游戏的快捷键Q
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets):
    #check_events简化原有的run_game()并隔离事件管理循环,比如将事件管理与屏幕刷新分离
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: #当按下方向右键时 初始值ship.moving_right False改为True  具体查看ship.py
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: #当松开方向右键时 ship.moving_right 改为 False 停止向右移动
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN: #pygame检测游戏中的鼠标点击事件
            mouse_x, mouse_y = pygame.mouse.get_pos() #get_pos 返回一个元祖,包括玩家单击时的鼠标的x与y坐标 传递给check_play_button
            check_play_button(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True #改变游戏状态,游戏开始
        
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        """清空外星人列表和子弹列表"""
        aliens.empty()
        bullets.empty()
        
        #创建新的舰群,并让本船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):#只包含玩家按空格用于发射子弹的代码
	# 创建一颗子弹,并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,play_button): #更新屏幕函数包括三个形参 ai_settings,screen和ship.
    """"刷新屏幕上的图像,并切换到新屏幕"""
    screen.fill(ai_settings.bg_color) # 每次循环都重绘屏幕

    for bullet in bullets.sprites():# 绘制飞船到屏幕上
        bullet.draw_bullet()
    ship.blitme()# 绘制飞船到屏幕上
    aliens.draw(screen)
    
	#显示得分
    sb.show_score()
    
    if not stats.game_active:#如果游戏处在非活动状态,就绘制Play按钮
        play_button.draw_button()

    pygame.display.flip()# 让最近绘制的屏幕可见,擦除旧屏幕,并且营造平滑移动的效果
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置,并删除已消失的子弹"""
	#更新子弹的位置
    bullets.update()

    #删除已消失的子弹
    for bullet in bullets.copy():# 遍历编组的副本,不应从列表或编组直接删除条目 利用copy()方法来设置for 循环
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)
        
def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):#检测子弹与外星人之间的碰撞 以及外星人被全部消灭之后采取的游戏进程
#检查是否有子弹击中了外星人,如果击中了就删除相应的子弹和外星人
    """先遍历bullets组的每颗子弹,再遍历aliens组中每个外星人,每当子弹与外星人rect重叠时,groupcollide()就会在返回的字典中添加一个键值对,
    两个实参True向Pygame传递删除请求,删除发生碰撞的子弹和外星人,如果将第一个True改为False,子弹将变成穿甲弹,一直抵达屏幕顶端消失"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    """外星人在update_bullets()中被消灭,因此检查舰群编组aliens是否为空"""
    if len(aliens) == 0:
        #删除现有的子弹并新建外星人舰群
        bullets.empty()
        ai_settings.increase_speed()
        
        #提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施
    :rtype: object
    """
    for alien in aliens.sprites():
        if alien.check_edges(): #如果碰壁条件成立 则执行下面的改变舰群移动方向的脚本
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """将舰群整体下移,并在碰壁的时候改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed #下降的速度赋值到舰群的Y坐标
    ai_settings.fleet_direction *= -1 #这里的逻辑是 碰壁之后 先下降设定的距离 然后再改变方向移动的方向 乘以-1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 减少1个单位玩家拥有的人头数(生命数)
        stats.ships_left -= 1
        
       #更新记分牌
        sb.prep_ships()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    
    # 创建新的舰群,并将本船防盗屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # 死亡后停顿,暂停
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#检查是否有外星人位于屏幕边缘,并更新调整舰群的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
            
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width #可放置外星人的水平空间为屏幕宽度减去外星人宽度的两倍
    number_aliens_x = int(available_space_x / (2.1 * alien_width)) #确定一行可以容纳多少个外星人,为了保证外星人之间有足够间距 所以除以两倍的外星人宽度
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -(8 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
