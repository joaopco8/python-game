import pygame
from sprite_loader import SpriteLoader

class Player:
    def __init__(self, x, y, largura, altura, velocidade):
        """Inicializa o jogador"""
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.projeteis = []  # Lista de projéteis ativos
        
        # Carrega sprite do jogador
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite("player")
    
    def processar_movimento(self, teclas, largura_tela, altura_tela, hud_altura):
        """Processa o movimento do jogador baseado nas teclas pressionadas"""
        # Movimento horizontal (A/D ou setas esquerda/direita)
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
        
        # Movimento vertical (W/S ou setas cima/baixo)
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.y -= self.velocidade
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.y += self.velocidade
        
        # Limita o movimento para manter o jogador na tela
        self.x = max(0, min(self.x, largura_tela - self.largura))
        self.y = max(hud_altura, min(self.y, altura_tela - self.altura))
    
    def atirar(self):
        """Cria um novo projétil"""
        # Posição inicial do projétil (centro do submarino)
        proj_x = self.x + self.largura
        proj_y = self.y + self.altura // 2
        proj = Projetil(proj_x, proj_y)
        self.projeteis.append(proj)
    
    def atualizar_projeteis(self, largura_tela):
        """Atualiza a posição dos projéteis e remove os que saíram da tela"""
        for proj in self.projeteis[:]:
            proj.atualizar()
            if proj.x > largura_tela:
                self.projeteis.remove(proj)
    
    def desenhar(self, tela):
        """Desenha o submarino do jogador"""
        # Desenha sprite do jogador
        if self.sprite:
            tela.blit(self.sprite, (self.x, self.y))
        else:
            # Fallback para retângulo se sprite não carregar
            jogador_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.rect(tela, (255, 255, 255), jogador_rect)
        
        # Desenha os projéteis
        for proj in self.projeteis:
            proj.desenhar(tela)

class Projetil:
    def __init__(self, x, y):
        """Inicializa um projétil"""
        self.x = x
        self.y = y
        self.largura = 15
        self.altura = 15
        self.velocidade = 8
        
        # Carrega sprite do projétil
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite("projectile")
    
    def atualizar(self):
        """Move o projétil para a direita"""
        self.x += self.velocidade
    
    def desenhar(self, tela):
        """Desenha o projétil"""
        if self.sprite:
            tela.blit(self.sprite, (self.x, self.y))
        else:
            # Fallback para retângulo se sprite não carregar
            proj_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.rect(tela, (255, 255, 0), proj_rect)  # Amarelo
    
    def get_rect(self):
        """Retorna o retângulo de colisão do projétil"""
        return pygame.Rect(self.x, self.y, self.largura, self.altura) 