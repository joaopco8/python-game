import pygame
import sys
import os
from player import Player
from enemy import EnemyManager
from coral import CoralManager
from boss import Boss
from powerup import PowerUpManager
from menu import Menu, TelaVitoria
from sound_manager import SoundManager
from background import Background

# Inicialização do Pygame
pygame.init()

# Configurações da janela
LARGURA = 960
ALTURA = 540
TITULO = "Aventura Submarina: O Resgate dos Corais"

# Cores
AZUL_OCEANO = (0, 100, 200)  # Azul para representar o oceano
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

# Configurações do jogador
JOGADOR_LARGURA = 60
JOGADOR_ALTURA = 30
JOGADOR_VELOCIDADE = 5  # Velocidade de movimento do submarino

# Configurações do HUD
FONTE_TAMANHO = 24
HUD_ALTURA = 40

# Configurações do jogo
PONTOS_POR_INIMIGO = 10
VIDA_MAXIMA = 100
PONTOS_POR_BOSS = 100
TEMPO_PARA_BOSS = 30000  # 30 segundos

class Jogo:
    def __init__(self):
        """Inicializa o jogo e suas configurações"""
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        
        # Clock para controlar o framerate
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Estado do jogo
        self.rodando = True
        
        # Dados do jogador
        self.vida = 100
        self.pontuacao = 0
        
        # Cria o jogador
        self.jogador = Player(50, ALTURA - 100, JOGADOR_LARGURA, JOGADOR_ALTURA, JOGADOR_VELOCIDADE)
        
        # Cria o gerenciador de inimigos
        self.enemy_manager = EnemyManager(LARGURA, ALTURA, HUD_ALTURA)
        
        # Cria o gerenciador de corais
        self.coral_manager = CoralManager(LARGURA, ALTURA, HUD_ALTURA, num_corais=8)
        
        # Cria o gerenciador de power-ups
        self.powerup_manager = PowerUpManager(LARGURA, ALTURA, HUD_ALTURA)
        
        # Sistema de som
        self.sound_manager = SoundManager()
        
        # Sistema de background
        self.background = Background(LARGURA, ALTURA)
        
        # Controle de tiro
        self.ultimo_tiro = 0
        self.intervalo_tiro = 300  # 300ms entre tiros
        
        # Sistema de boss
        self.boss = None
        self.boss_ativo = False
        self.tempo_inicio = pygame.time.get_ticks()
        
        # Fonte para o HUD
        self.fonte = pygame.font.Font(None, FONTE_TAMANHO)
    
    def processar_eventos(self):
        """Processa eventos do pygame (teclas, mouse, etc.)"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Volta ao menu em vez de fechar
                    self.rodando = False
                elif evento.key == pygame.K_SPACE:
                    # Tiro controlado por intervalo
                    tempo_atual = pygame.time.get_ticks()
                    if tempo_atual - self.ultimo_tiro > self.intervalo_tiro:
                        self.jogador.atirar()
                        self.sound_manager.tocar_tiro()
                        self.ultimo_tiro = tempo_atual
    
    def processar_movimento_jogador(self):
        """Processa o movimento do jogador baseado nas teclas pressionadas"""
        teclas = pygame.key.get_pressed()
        self.jogador.processar_movimento(teclas, LARGURA, ALTURA, HUD_ALTURA)
    
    def verificar_colisoes(self):
        """Verifica colisões entre projéteis e inimigos"""
        colisoes = self.enemy_manager.verificar_colisoes(self.jogador.projeteis)
        
        for inimigo, proj in colisoes:
            # Remove inimigo e projétil
            if inimigo in self.enemy_manager.inimigos:
                self.enemy_manager.inimigos.remove(inimigo)
            if proj in self.jogador.projeteis:
                self.jogador.projeteis.remove(proj)
            
            # Adiciona pontos
            self.pontuacao += PONTOS_POR_INIMIGO
    
    def verificar_colisao_corais(self):
        """Verifica colisão entre jogador e corais"""
        pontos_coral = self.coral_manager.verificar_colisao_jogador(self.jogador)
        if pontos_coral > 0:
            self.pontuacao += pontos_coral
            self.sound_manager.tocar_coral()
    
    def verificar_colisao_powerups(self):
        """Verifica colisão entre jogador e power-ups"""
        tempo_atual = pygame.time.get_ticks()
        powerup_coletado = self.powerup_manager.verificar_colisao_jogador(self.jogador, tempo_atual)
        if powerup_coletado:
            self.sound_manager.tocar_coral()  # Usa som de coral para power-up
            print(f"Power-up coletado: {powerup_coletado}")
    
    def verificar_colisao_boss(self):
        """Verifica colisões com o boss"""
        if not self.boss_ativo or not self.boss:
            return
        
        # Colisão projéteis do jogador com boss
        for proj in self.jogador.projeteis[:]:
            proj_rect = proj.get_rect()
            boss_rect = self.boss.get_rect()
            
            if proj_rect.colliderect(boss_rect):
                if proj in self.jogador.projeteis:
                    self.jogador.projeteis.remove(proj)
                
                if self.boss.receber_dano(20):  # 20 de dano por tiro
                    self.boss_ativo = False
                    self.pontuacao += PONTOS_POR_BOSS
                    self.sound_manager.tocar_vitoria()
                else:
                    self.sound_manager.tocar_boss_hit()
        
        # Colisão projéteis do boss com jogador
        for proj in self.boss.projeteis[:]:
            proj_rect = proj.get_rect()
            jogador_rect = pygame.Rect(self.jogador.x, self.jogador.y, 
                                     self.jogador.largura, self.jogador.altura)
            
            if proj_rect.colliderect(jogador_rect):
                if proj in self.boss.projeteis:
                    self.boss.projeteis.remove(proj)
                
                self.vida -= 10
                self.sound_manager.tocar_dano()
    
    def verificar_boss_spawn(self):
        """Verifica se deve spawnar o boss"""
        if not self.boss_ativo and not self.boss:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicio > TEMPO_PARA_BOSS:
                self.boss = Boss(LARGURA - 150, ALTURA // 2 - 40)
                self.boss_ativo = True
                print("BOSS APARECEU!")
    
    def verificar_colisao_inimigos_jogador(self):
        """Verifica colisão entre inimigos e jogador"""
        jogador_rect = pygame.Rect(self.jogador.x, self.jogador.y, 
                                 self.jogador.largura, self.jogador.altura)
        
        for inimigo in self.enemy_manager.inimigos[:]:
            inimigo_rect = inimigo.get_rect()
            if jogador_rect.colliderect(inimigo_rect):
                # Remove o inimigo
                self.enemy_manager.inimigos.remove(inimigo)
                # Causa dano ao jogador
                self.vida -= 15
                print(f"Jogador tomou dano! Vida: {self.vida}")
                self.sound_manager.tocar_dano()
                
                # Verifica se o jogador morreu
                if self.vida <= 0:
                    print("GAME OVER!")
                    self.rodando = False
    
    def atualizar(self):
        """Atualiza a lógica do jogo"""
        self.processar_movimento_jogador()
        
        # Atualiza projéteis do jogador
        self.jogador.atualizar_projeteis(LARGURA)
        
        # Atualiza inimigos, corais e power-ups
        tempo_atual = pygame.time.get_ticks()
        self.enemy_manager.atualizar(tempo_atual)
        self.coral_manager.atualizar(tempo_atual)
        self.powerup_manager.atualizar(tempo_atual)
        
        # Sistema de boss
        self.verificar_boss_spawn()
        if self.boss_ativo and self.boss:
            self.boss.atualizar(LARGURA, ALTURA, tempo_atual)
            self.verificar_colisao_boss()
        
        # Verifica colisões
        self.verificar_colisoes()
        self.verificar_colisao_corais()
        self.verificar_colisao_powerups()
        self.verificar_colisao_inimigos_jogador()
    
    def desenhar_hud(self):
        """Desenha o HUD (Heads-Up Display) na tela"""
        # Fundo do HUD
        hud_rect = pygame.Rect(0, 0, LARGURA, HUD_ALTURA)
        pygame.draw.rect(self.tela, (0, 0, 0, 128), hud_rect)
        
        # Barra de vida
        self.desenhar_barra_vida()
        
        # Texto da vida
        texto_vida = self.fonte.render(f"Vida: {self.vida}", True, VERMELHO)
        self.tela.blit(texto_vida, (10, 10))
        
        # Texto da pontuação
        texto_pontuacao = self.fonte.render(f"Pontuação: {self.pontuacao}", True, AMARELO)
        self.tela.blit(texto_pontuacao, (LARGURA - 200, 10))
        
        # Texto dos corais coletados
        texto_corais = self.fonte.render(f"Corais: {self.coral_manager.corais_coletados}", True, (0, 255, 0))
        self.tela.blit(texto_corais, (LARGURA // 2 - 50, 10))
    
    def desenhar_barra_vida(self):
        """Desenha a barra de vida do jogador"""
        barra_x = 120
        barra_y = 15
        barra_largura = 200
        barra_altura = 15
        
        # Fundo da barra (cinza)
        fundo_rect = pygame.Rect(barra_x, barra_y, barra_largura, barra_altura)
        pygame.draw.rect(self.tela, (100, 100, 100), fundo_rect)
        
        # Barra de vida (verde)
        vida_atual = (self.vida / VIDA_MAXIMA) * barra_largura
        vida_rect = pygame.Rect(barra_x, barra_y, vida_atual, barra_altura)
        
        # Cor baseada na vida
        if self.vida > 60:
            cor_vida = (0, 255, 0)  # Verde
        elif self.vida > 30:
            cor_vida = (255, 255, 0)  # Amarelo
        else:
            cor_vida = (255, 0, 0)  # Vermelho
        
        pygame.draw.rect(self.tela, cor_vida, vida_rect)
        
        # Borda da barra
        pygame.draw.rect(self.tela, (255, 255, 255), fundo_rect, 2)
    
    def desenhar_jogador(self):
        """Desenha o submarino do jogador"""
        self.jogador.desenhar(self.tela)
    
    def desenhar(self):
        """Desenha todos os elementos na tela"""
        # Desenha o background primeiro
        self.background.desenhar(self.tela)
        
        # Desenha os corais
        self.coral_manager.desenhar(self.tela)
        
        # Desenha os power-ups
        self.powerup_manager.desenhar(self.tela)
        
        # Desenha os inimigos
        self.enemy_manager.desenhar(self.tela)
        
        # Desenha o boss
        if self.boss_ativo and self.boss:
            self.boss.desenhar(self.tela)
        
        # Desenha o jogador
        self.desenhar_jogador()
        
        # Desenha o HUD
        self.desenhar_hud()
        
        # Atualiza a tela
        pygame.display.flip()
    
    def executar(self):
        """Loop principal do jogo"""
        print("Iniciando Aventura Submarina: O Resgate dos Corais...")
        print("Pressione ESC para sair")
        
        # Inicia música de fundo
        self.sound_manager.tocar_musica_fundo()
        
        while self.rodando:
            # Processa eventos
            self.processar_eventos()
            
            # Atualiza a lógica do jogo
            self.atualizar()
            
            # Desenha tudo na tela
            self.desenhar()
            
            # Controla o framerate
            self.clock.tick(self.fps)
        
        # Finaliza o pygame
        self.sound_manager.parar_musica()
        pygame.quit()
        sys.exit()

# Função main movida para game_manager.py 