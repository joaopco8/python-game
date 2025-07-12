import pygame
import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, compatível com PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Background:
    def __init__(self, largura, altura):
        """Inicializa o sistema de fundo do jogo"""
        self.largura = largura
        self.altura = altura
        
        # Carrega a imagem de fundo
        self.carregar_background()
    
    def carregar_background(self):
        """Carrega e prepara a imagem de fundo"""
        try:
            # Caminho para a imagem de fundo
            caminho_background = resource_path(os.path.join("assets", "images", "background.png"))
            
            # Carrega a imagem
            self.imagem_original = pygame.image.load(caminho_background).convert_alpha()
            
            # Escala a imagem para o tamanho da janela
            self.imagem = pygame.transform.scale(self.imagem_original, (self.largura, self.altura))
            
            print("Background carregado com sucesso!")
            
        except pygame.error as e:
            print(f"Erro ao carregar background: {e}")
            # Cria um fundo azul padrão caso a imagem não carregue
            self.imagem = pygame.Surface((self.largura, self.altura))
            self.imagem.fill((0, 100, 200))  # Azul oceano
    
    def desenhar(self, tela):
        """Desenha o fundo na tela"""
        # Desenha o background na posição (0, 0)
        tela.blit(self.imagem, (0, 0)) 