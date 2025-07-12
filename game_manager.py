import pygame
import sys
from menu import Menu, TelaVitoria
from main import Jogo

class GameManager:
    def __init__(self):
        """Inicializa o gerenciador do jogo"""
        pygame.init()
        
        # Configurações da janela
        self.largura = 960
        self.altura = 540
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Aventura Submarina: O Resgate dos Corais")
        
        # Estados do jogo
        self.estado = "menu"  # menu, jogo, vitoria, sair
        
        # Cria as telas
        self.menu = Menu(self.largura, self.altura)
        self.tela_vitoria = TelaVitoria(self.largura, self.altura)
        self.jogo = None
        
        # Clock para framerate
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def executar(self):
        """Loop principal do gerenciador"""
        print("Iniciando Aventura Submarina: O Resgate dos Corais...")
        
        while self.estado != "sair":
            if self.estado == "menu":
                self.executar_menu()
            elif self.estado == "jogo":
                self.executar_jogo()
            elif self.estado == "vitoria":
                self.executar_tela_vitoria()
        
        pygame.quit()
        sys.exit()
    
    def executar_menu(self):
        """Executa o menu principal"""
        while self.estado == "menu":
            resultado = self.menu.processar_eventos()
            
            if resultado == "jogar":
                self.estado = "jogo"
                self.jogo = Jogo()
            elif resultado == "sair":
                self.estado = "sair"
            
            self.menu.desenhar(self.tela)
            self.clock.tick(self.fps)
    
    def executar_jogo(self):
        """Executa o jogo principal"""
        if not self.jogo:
            return
        
        # Loop do jogo
        while self.estado == "jogo" and self.jogo.rodando:
            # Atualiza e desenha o jogo
            self.jogo.processar_eventos()
            self.jogo.atualizar()
            self.jogo.desenhar()
            
            # Verifica se o boss foi derrotado
            if self.jogo.boss_ativo == False and self.jogo.boss:
                self.estado = "vitoria"
                return
            
            self.clock.tick(self.fps)
    
    def executar_tela_vitoria(self):
        """Executa a tela de vitória"""
        pontuacao = self.jogo.pontuacao if self.jogo else 0
        
        while self.estado == "vitoria":
            resultado = self.tela_vitoria.processar_eventos()
            
            if resultado == "menu":
                self.estado = "menu"
                self.jogo = None
            elif resultado == "sair":
                self.estado = "sair"
            
            self.tela_vitoria.desenhar(self.tela, pontuacao)
            self.clock.tick(self.fps)

def main():
    """Função principal"""
    game_manager = GameManager()
    game_manager.executar()

if __name__ == "__main__":
    main() 