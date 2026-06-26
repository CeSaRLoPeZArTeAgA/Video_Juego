import pygame

class CollisionDetector:
    def __init__(self):
        pass

    def bullets_vs_enemies(self, bullets, enemies):
        gained = 0
        for bullet in list(bullets):
            for enemy in list(enemies):
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    if enemy.damage(bullet.damage):
                        gained += enemy.points
                        if enemy in enemies:
                            enemies.remove(enemy)
                    break
        return gained

    def bullets_vs_boss(self, bullets, boss):
        if boss is None:
            return 0, False
        gained = 0
        defeated = False
        for bullet in list(bullets):
            if bullet.rect.colliderect(boss.rect):
                bullet.kill()
                if boss.damage(bullet.damage):
                    defeated = True
                    gained += boss.points
                break
        return gained, defeated

    def player_vs_enemies(self, player, enemies):
        hits = 0
        for enemy in list(enemies):
            if player.hitbox.colliderect(enemy.rect):
                if player.hit():
                    hits += 1
                enemy.kill()
                if enemy in enemies:
                    enemies.remove(enemy)
        return hits

    def player_vs_powerups(self, player, powerups):
        gained = 0
        for p in list(powerups):
            if player.hitbox.colliderect(p.rect):
                if p.kind == "score":
                    gained += 1
                else:
                    player.apply_power(p.kind)
                p.kill()
                if p in powerups:
                    powerups.remove(p)
        return gained
