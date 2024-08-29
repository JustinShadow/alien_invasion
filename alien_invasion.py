import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 创建时钟实例，用于控制帧率
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # 设置背景色
        # self.bg_color = (230, 230, 230)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            # 使用pygame的时钟计时，控制帧率为60（每秒运行60次）
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件的辅组方法"""
        # 侦听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """处理键盘按下事件的辅助方法"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """处理键盘松开事件的辅助方法"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """更新游戏画面，并切换到新屏幕的辅助方法"""
        # 每次循环重绘画面
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _fire_bullet(self):
        """创建一颗子弹，将其加入到编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_aliens(self):
        """检查外星人是否位于屏幕边缘，更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

    def _update_bullets(self):
        """更新子弹位置，删除已消失的子弹"""
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width, alien.rect.height

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height / 2):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._creat_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _creat_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x, new_alien.y = x_position, y_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在有外星人到达屏幕边缘时采取对应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星人舰队向下移动，并改变水平移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += alien.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
