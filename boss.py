import pygame
import random
import math
from sprite_loader import SpriteLoader

class Boss:
    def __init__(self, x, y):
        """Inicializa o chefe (polvo gigante)"""
        self.x = x
        self.y = y
        self.largura = 120
        self.altura = 80
        self.vida_maxima = 200
        self.vida_atual = self.vida_maxima
        self.velocidade = 1
        self.direcao = 1  # 1 para direita, -1 para esquerda
        
        # Carrega sprite do boss
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite("boss_octopus")
        
        # Projéteis do chefe
        self.projeteis = []
        self.ultimo_tiro = 0
        self.intervalo_tiro = 1500  # 1.5 segundos
        
        # Movimento
        self.tempo_movimento = 0
        self.intervalo_movimento = 3000  # 3 segundos
        
        # Tentáculos
        self.tentaculos = []
        self.criar_tentaculos()
    
    def criar_tentaculos(self):
        """Cria os tentáculos do polvo"""
        for i in range(8):
            angulo = (i * 45) * (math.pi / 180)  # 45 graus cada
            x_tent = self.x + self.largura // 2 + math.cos(angulo) * 30
            y_tent = self.y + self.altura // 2 + math.sin(angulo) * 30
            self.tentaculos.append((x_tent, y_tent))
    
    def atualizar(self, largura_tela, altura_tela, tempo_atual):
        """Atualiza o chefe"""
        # Movimento
        if tempo_atual - self.tempo_movimento > self.intervalo_movimento:
            self.direcao *= -1
            self.tempo_movimento = tempo_atual
        
        self.x += self.velocidade * self.direcao
        
        # Limita movimento
        if self.x <= 0 or self.x >= largura_tela - self.largura:
            self.direcao *= -1
        
        # Atualiza tentáculos
        self.atualizar_tentaculos()
        
        # Tiro
        if tempo_atual - self.ultimo_tiro > self.intervalo_tiro:
            self.atirar()
            self.ultimo_tiro = tempo_atual
        
        # Atualiza projéteis
        for proj in self.projeteis[:]:
            proj.atualizar()
            if proj.x < 0:
                self.projeteis.remove(proj)
    
    def atualizar_tentaculos(self):
        """Atualiza a posição dos tentáculos"""
        for i in range(len(self.tentaculos)):
            angulo = (i * 45) * (math.pi / 180)
            x_tent = self.x + self.largura // 2 + math.cos(angulo) * 30
            y_tent = self.y + self.altura // 2 + math.sin(angulo) * 30
            self.tentaculos[i] = (x_tent, y_tent)
    
    def atirar(self):
        """Dispara projéteis em direções aleatórias"""
        for _ in range(3):  # 3 projéteis por vez
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = 4
            
            proj_x = self.x + self.largura // 2
            proj_y = self.y + self.altura // 2
            
            proj = BossProjetil(proj_x, proj_y, velocidade, angulo)
            self.projeteis.append(proj)
    
    def receber_dano(self, dano):
        """Recebe dano e retorna se foi derrotado"""
        self.vida_atual -= dano
        return self.vida_atual <= 0
    
    def desenhar(self, tela):
        """Desenha o chefe"""
        if self.sprite:
            tela.blit(self.sprite, (self.x, self.y))
        else:
            # Fallback para formas geométricas se sprite não carregar
            # Corpo principal (roxa)
            corpo_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.ellipse(tela, (128, 0, 128), corpo_rect)
            
            # Olhos
            pygame.draw.circle(tela, (255, 255, 255), (self.x + 40, self.y + 30), 10)
            pygame.draw.circle(tela, (255, 255, 255), (self.x + 80, self.y + 30), 10)
            pygame.draw.circle(tela, (0, 0, 0), (self.x + 40, self.y + 30), 5)
            pygame.draw.circle(tela, (0, 0, 0), (self.x + 80, self.y + 30), 5)
            
            # Tentáculos
            for tent_x, tent_y in self.tentaculos:
                pygame.draw.circle(tela, (100, 0, 100), (int(tent_x), int(tent_y)), 8)
        
        # Barra de vida do chefe
        self.desenhar_barra_vida(tela)
        
        # Desenha projéteis
        for proj in self.projeteis:
            proj.desenhar(tela)
    
    def desenhar_barra_vida(self, tela):
        """Desenha a barra de vida do chefe"""
        barra_x = self.x
        barra_y = self.y - 20
        barra_largura = self.largura
        barra_altura = 10
        
        # Fundo
        fundo_rect = pygame.Rect(barra_x, barra_y, barra_largura, barra_altura)
        pygame.draw.rect(tela, (100, 100, 100), fundo_rect)
        
        # Vida atual
        vida_porcentagem = self.vida_atual / self.vida_maxima
        vida_largura = int(barra_largura * vida_porcentagem)
        vida_rect = pygame.Rect(barra_x, barra_y, vida_largura, barra_altura)
        
        # Cor baseada na vida
        if vida_porcentagem > 0.6:
            cor = (0, 255, 0)  # Verde
        elif vida_porcentagem > 0.3:
            cor = (255, 255, 0)  # Amarelo
        else:
            cor = (255, 0, 0)  # Vermelho
        
        pygame.draw.rect(tela, cor, vida_rect)
        pygame.draw.rect(tela, (255, 255, 255), fundo_rect, 2)
    
    def get_rect(self):
        """Retorna o retângulo de colisão do chefe"""
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

class BossProjetil:
    def __init__(self, x, y, velocidade, angulo):
        """Inicializa projétil do chefe"""
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.angulo = angulo
        self.raio = 8
        
        # Carrega sprite do projétil do boss
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite("projectile")
    
    def atualizar(self):
        """Move o projétil"""
        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade
    
    def desenhar(self, tela):
        """Desenha o projétil do chefe"""
        if self.sprite:
            tela.blit(self.sprite, (int(self.x - self.raio), int(self.y - self.raio)))
        else:
            # Fallback para círculo se sprite não carregar
            pygame.draw.circle(tela, (255, 0, 0), (int(self.x), int(self.y)), self.raio)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x - self.raio, self.y - self.raio, 
                          self.raio * 2, self.raio * 2) 