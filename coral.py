import pygame
import random
from sprite_loader import SpriteLoader

class Coral:
    def __init__(self, x, y, tipo="normal"):
        """Inicializa um coral coletável"""
        self.x = x
        self.y = y
        self.tipo = tipo
        self.raio = 15
        self.coletado = False
        self.tempo_coleta = 0
        self.tempo_reaparecimento = 5000  # 5 segundos
        
        # Carrega sprite do coral
        self.sprite_loader = SpriteLoader()
        self.sprite = self.sprite_loader.get_sprite("coral")
        
        # Cores baseadas no tipo (fallback)
        self.cores = {
            "normal": (255, 100, 150),    # Rosa
            "especial": (255, 215, 0),    # Dourado
            "raro": (138, 43, 226)        # Roxo
        }
        self.cor = self.cores.get(tipo, self.cores["normal"])
    
    def desenhar(self, tela):
        """Desenha o coral"""
        if not self.coletado:
            if self.sprite:
                tela.blit(self.sprite, (self.x - self.raio, self.y - self.raio))
            else:
                # Fallback para círculo se sprite não carregar
                pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio)
                
                # Detalhes do coral (pequenos círculos)
                detalhes = [
                    (self.x - 8, self.y - 8, 4),
                    (self.x + 8, self.y - 5, 3),
                    (self.x - 5, self.y + 8, 3),
                    (self.x + 5, self.y + 5, 2)
                ]
                
                for dx, dy, r in detalhes:
                    pygame.draw.circle(tela, (255, 255, 255), (dx, dy), r)
    
    def coletar(self, tempo_atual):
        """Marca o coral como coletado"""
        if not self.coletado:
            self.coletado = True
            self.tempo_coleta = tempo_atual
            return True
        return False
    
    def verificar_reaparecimento(self, tempo_atual, largura_tela, altura_tela, hud_altura):
        """Verifica se o coral deve reaparecer em nova posição"""
        if self.coletado and tempo_atual - self.tempo_coleta > self.tempo_reaparecimento:
            # Reposiciona o coral em local aleatório
            self.x = random.randint(50, largura_tela - 50)
            self.y = random.randint(hud_altura + 50, altura_tela - 50)
            self.coletado = False
            return True
        return False
    
    def get_rect(self):
        """Retorna o retângulo de colisão do coral"""
        return pygame.Rect(self.x - self.raio, self.y - self.raio, 
                          self.raio * 2, self.raio * 2)

class CoralManager:
    def __init__(self, largura_tela, altura_tela, hud_altura, num_corais=8):
        """Gerencia todos os corais do jogo"""
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.hud_altura = hud_altura
        self.corais = []
        self.corais_coletados = 0
        
        # Cria corais iniciais
        self.criar_corais_iniciais(num_corais)
    
    def criar_corais_iniciais(self, num_corais):
        """Cria os corais iniciais espalhados pelo cenário"""
        for i in range(num_corais):
            x = random.randint(100, self.largura_tela - 100)
            y = random.randint(self.hud_altura + 50, self.altura_tela - 100)
            
            # 70% normais, 20% especiais, 10% raros
            rand = random.random()
            if rand < 0.7:
                tipo = "normal"
            elif rand < 0.9:
                tipo = "especial"
            else:
                tipo = "raro"
            
            coral = Coral(x, y, tipo)
            self.corais.append(coral)
    
    def atualizar(self, tempo_atual):
        """Atualiza todos os corais"""
        for coral in self.corais:
            coral.verificar_reaparecimento(tempo_atual, self.largura_tela, 
                                        self.altura_tela, self.hud_altura)
    
    def desenhar(self, tela):
        """Desenha todos os corais"""
        for coral in self.corais:
            coral.desenhar(tela)
    
    def verificar_colisao_jogador(self, jogador):
        """Verifica colisão entre jogador e corais"""
        jogador_rect = pygame.Rect(jogador.x, jogador.y, jogador.largura, jogador.altura)
        tempo_atual = pygame.time.get_ticks()
        
        for coral in self.corais:
            if not coral.coletado:
                coral_rect = coral.get_rect()
                if jogador_rect.colliderect(coral_rect):
                    if coral.coletar(tempo_atual):
                        self.corais_coletados += 1
                        return self.get_pontos_coral(coral.tipo)
        return 0
    
    def get_pontos_coral(self, tipo):
        """Retorna pontos baseados no tipo do coral"""
        pontos = {
            "normal": 5,
            "especial": 15,
            "raro": 30
        }
        return pontos.get(tipo, 5) 