import pygame
import random
from sprite_loader import SpriteLoader

class PowerUp:
    def __init__(self, x, y, tipo="shield"):
        """Inicializa um power-up"""
        self.x = x
        self.y = y
        self.tipo = tipo
        self.largura = 25
        self.altura = 25
        self.coletado = False
        self.tempo_coleta = 0
        self.tempo_reaparecimento = 10000  # 10 segundos
        
        # Carrega sprite do power-up
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite(f"powerup_{tipo}")
        
        # Efeitos baseados no tipo
        self.efeitos = {
            "shield": {"duracao": 5000, "descricao": "Escudo"},
            "speed": {"duracao": 3000, "descricao": "Velocidade"},
            "torpedo": {"duracao": 4000, "descricao": "Super Tiro"}
        }
    
    def coletar(self, tempo_atual):
        """Marca o power-up como coletado"""
        if not self.coletado:
            self.coletado = True
            self.tempo_coleta = tempo_atual
            return True
        return False
    
    def verificar_reaparecimento(self, tempo_atual, largura_tela, altura_tela, hud_altura):
        """Verifica se o power-up deve reaparecer"""
        if self.coletado and tempo_atual - self.tempo_coleta > self.tempo_reaparecimento:
            # Reposiciona o power-up
            self.x = random.randint(50, largura_tela - 50)
            self.y = random.randint(hud_altura + 50, altura_tela - 50)
            self.coletado = False
            return True
        return False
    
    def desenhar(self, tela):
        """Desenha o power-up"""
        if not self.coletado:
            if self.sprite:
                tela.blit(self.sprite, (self.x, self.y))
            else:
                # Fallback para retângulo colorido
                cor = (0, 255, 0) if self.tipo == "shield" else (255, 255, 0) if self.tipo == "speed" else (255, 0, 255)
                powerup_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
                pygame.draw.rect(tela, cor, powerup_rect)
                pygame.draw.rect(tela, (255, 255, 255), powerup_rect, 2)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return pygame.Rect(self.x, self.y, self.largura, self.altura)
    
    def get_efeito(self):
        """Retorna o efeito do power-up"""
        return self.efeitos.get(self.tipo, {"duracao": 3000, "descricao": "Desconhecido"})

class PowerUpManager:
    def __init__(self, largura_tela, altura_tela, hud_altura):
        """Gerencia os power-ups do jogo"""
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.hud_altura = hud_altura
        self.powerups = []
        self.powerups_ativos = {}  # {tipo: tempo_fim}
        
        # Cria power-ups iniciais
        self.criar_powerups_iniciais()
    
    def criar_powerups_iniciais(self):
        """Cria power-ups iniciais"""
        tipos = ["shield", "speed", "torpedo"]
        
        for i in range(3):
            x = random.randint(100, self.largura_tela - 100)
            y = random.randint(self.hud_altura + 50, self.altura_tela - 100)
            tipo = tipos[i]
            
            powerup = PowerUp(x, y, tipo)
            self.powerups.append(powerup)
    
    def atualizar(self, tempo_atual):
        """Atualiza todos os power-ups"""
        for powerup in self.powerups:
            powerup.verificar_reaparecimento(tempo_atual, self.largura_tela, 
                                          self.altura_tela, self.hud_altura)
        
        # Remove power-ups ativos expirados
        for tipo in list(self.powerups_ativos.keys()):
            if tempo_atual > self.powerups_ativos[tipo]:
                del self.powerups_ativos[tipo]
    
    def desenhar(self, tela):
        """Desenha todos os power-ups"""
        for powerup in self.powerups:
            powerup.desenhar(tela)
    
    def verificar_colisao_jogador(self, jogador, tempo_atual):
        """Verifica colisão entre jogador e power-ups"""
        jogador_rect = pygame.Rect(jogador.x, jogador.y, jogador.largura, jogador.altura)
        
        for powerup in self.powerups:
            if not powerup.coletado:
                powerup_rect = powerup.get_rect()
                if jogador_rect.colliderect(powerup_rect):
                    if powerup.coletar(tempo_atual):
                        # Ativa o power-up
                        efeito = powerup.get_efeito()
                        self.powerups_ativos[powerup.tipo] = tempo_atual + efeito["duracao"]
                        return powerup.tipo
        return None
    
    def is_powerup_ativo(self, tipo):
        """Verifica se um power-up está ativo"""
        return tipo in self.powerups_ativos 