import pygame

class Menu:
    def __init__(self, largura, altura):
        """Inicializa o menu principal"""
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_botao = pygame.font.Font(None, 48)
        self.fonte_info = pygame.font.Font(None, 24)
        
        # Cores
        self.cor_fundo = (0, 50, 100)
        self.cor_titulo = (255, 255, 255)
        self.cor_botao = (0, 150, 255)
        self.cor_botao_hover = (0, 200, 255)
        self.cor_texto_botao = (255, 255, 255)
        
        # Botão jogar
        self.botao_jogar = pygame.Rect(largura // 2 - 100, altura // 2 + 50, 200, 60)
        self.botao_hover = False
    
    def processar_eventos(self):
        """Processa eventos do menu"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo
                    if self.botao_jogar.collidepoint(evento.pos):
                        return "jogar"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "sair"
                elif evento.key == pygame.K_RETURN:
                    return "jogar"
        
        # Verifica hover do botão
        mouse_pos = pygame.mouse.get_pos()
        self.botao_hover = self.botao_jogar.collidepoint(mouse_pos)
        
        return None
    
    def desenhar(self, tela):
        """Desenha o menu"""
        # Fundo
        tela.fill(self.cor_fundo)
        
        # Título
        titulo = self.fonte_titulo.render("Aventura Submarina", True, self.cor_titulo)
        subtitulo = self.fonte_titulo.render("O Resgate dos Corais", True, self.cor_titulo)
        
        titulo_rect = titulo.get_rect(center=(self.largura // 2, self.altura // 3))
        subtitulo_rect = subtitulo.get_rect(center=(self.largura // 2, self.altura // 3 + 80))
        
        tela.blit(titulo, titulo_rect)
        tela.blit(subtitulo, subtitulo_rect)
        
        # Botão jogar
        cor_botao = self.cor_botao_hover if self.botao_hover else self.cor_botao
        pygame.draw.rect(tela, cor_botao, self.botao_jogar, border_radius=10)
        pygame.draw.rect(tela, (255, 255, 255), self.botao_jogar, 3, border_radius=10)
        
        texto_botao = self.fonte_botao.render("JOGAR", True, self.cor_texto_botao)
        texto_rect = texto_botao.get_rect(center=self.botao_jogar.center)
        tela.blit(texto_botao, texto_rect)
        
        # Instruções
        instrucoes = [
            "Controles:",
            "WASD ou Setas - Mover",
            "ESPAÇO - Atirar",
            "ESC - Sair"
        ]
        
        y_offset = self.altura - 150
        for i, instrucao in enumerate(instrucoes):
            texto = self.fonte_info.render(instrucao, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(self.largura // 2, y_offset + i * 25))
            tela.blit(texto, texto_rect)
        
        pygame.display.flip()

class TelaVitoria:
    def __init__(self, largura, altura):
        """Inicializa a tela de vitória"""
        self.largura = largura
        self.altura = altura
        self.fonte_titulo = pygame.font.Font(None, 64)
        self.fonte_texto = pygame.font.Font(None, 36)
        self.fonte_botao = pygame.font.Font(None, 48)
        
        # Botão voltar ao menu
        self.botao_menu = pygame.Rect(largura // 2 - 100, altura - 100, 200, 60)
    
    def processar_eventos(self):
        """Processa eventos da tela de vitória"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.botao_menu.collidepoint(evento.pos):
                        return "menu"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"
                elif evento.key == pygame.K_RETURN:
                    return "menu"
        
        return None
    
    def desenhar(self, tela, pontuacao):
        """Desenha a tela de vitória"""
        # Fundo
        tela.fill((0, 100, 50))  # Verde escuro
        
        # Título
        titulo = self.fonte_titulo.render("FASE CONCLUÍDA!", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.largura // 2, self.altura // 3))
        tela.blit(titulo, titulo_rect)
        
        # Mensagem
        mensagem = self.fonte_texto.render("Parabéns! Você salvou os corais!", True, (255, 255, 255))
        mensagem_rect = mensagem.get_rect(center=(self.largura // 2, self.altura // 2))
        tela.blit(mensagem, mensagem_rect)
        
        # Pontuação
        texto_pontos = self.fonte_texto.render(f"Pontuação Final: {pontuacao}", True, (255, 255, 0))
        pontos_rect = texto_pontos.get_rect(center=(self.largura // 2, self.altura // 2 + 50))
        tela.blit(texto_pontos, pontos_rect)
        
        # Botão voltar ao menu
        pygame.draw.rect(tela, (0, 150, 255), self.botao_menu, border_radius=10)
        pygame.draw.rect(tela, (255, 255, 255), self.botao_menu, 3, border_radius=10)
        
        texto_botao = self.fonte_botao.render("MENU", True, (255, 255, 255))
        texto_rect = texto_botao.get_rect(center=self.botao_menu.center)
        tela.blit(texto_botao, texto_rect)
        
        pygame.display.flip() 