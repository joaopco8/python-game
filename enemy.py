import pygame
import random
from sprite_loader import SpriteLoader

class Enemy:
    def __init__(self, x, y, largura, altura, velocidade, tipo="jellyfish"):
        """Inicializa um inimigo"""
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.tipo = tipo
        
        # Carrega sprite do inimigo
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite(f"enemy_{tipo}")
    
    def atualizar(self):
        """Move o inimigo para a esquerda"""
        self.x -= self.velocidade
    
    def desenhar(self, tela):
        """Desenha o inimigo"""
        if self.sprite:
            tela.blit(self.sprite, (self.x, self.y))
        else:
            # Fallback para retângulo se sprite não carregar
            peixe_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
            pygame.draw.rect(tela, (255, 100, 100), peixe_rect)  # Vermelho
    
    def get_rect(self):
        """Retorna o retângulo de colisão do inimigo"""
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
    
    def esta_fora_da_tela(self):
        """Verifica se o inimigo saiu da tela pela esquerda"""
        return self.x + self.largura < 0

class EnemyManager:
    def __init__(self, largura_tela, altura_tela, hud_altura):
        """Gerencia a criação e atualização dos inimigos"""
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.hud_altura = hud_altura
        self.inimigos = []
        self.tempo_ultimo_inimigo = 0
        self.intervalo_criacao = 2000  # 2 segundos entre inimigos
        self.velocidade_inimigo = 3
    
    def criar_inimigo(self):
        """Cria um novo inimigo no lado direito da tela"""
        x = self.largura_tela
        y = random.randint(self.hud_altura + 20, self.altura_tela - 40)
        
        # Escolhe tipo aleatório de inimigo
        tipos = ["jellyfish", "fish", "crab"]
        tipo = random.choice(tipos)
        
        # Tamanhos baseados no tipo
        tamanhos = {
            "jellyfish": (40, 40),
            "fish": (30, 20),
            "crab": (35, 25)
        }
        largura, altura = tamanhos.get(tipo, (30, 20))
        
        inimigo = Enemy(x, y, largura, altura, self.velocidade_inimigo, tipo)
        self.inimigos.append(inimigo)
    
    def atualizar(self, tempo_atual):
        """Atualiza todos os inimigos e cria novos se necessário"""
        # Cria novo inimigo se passou tempo suficiente
        if tempo_atual - self.tempo_ultimo_inimigo > self.intervalo_criacao:
            self.criar_inimigo()
            self.tempo_ultimo_inimigo = tempo_atual
        
        # Atualiza posição dos inimigos existentes
        for inimigo in self.inimigos[:]:
            inimigo.atualizar()
            if inimigo.esta_fora_da_tela():
                self.inimigos.remove(inimigo)
    
    def desenhar(self, tela):
        """Desenha todos os inimigos"""
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
    
    def verificar_colisoes(self, projeteis):
        """Verifica colisões entre projéteis e inimigos"""
        colisoes = []
        
        for inimigo in self.inimigos[:]:
            inimigo_rect = inimigo.get_rect()
            
            for proj in projeteis[:]:
                proj_rect = proj.get_rect()
                
                if inimigo_rect.colliderect(proj_rect):
                    # Colisão detectada
                    colisoes.append((inimigo, proj))
        
        return colisoes 