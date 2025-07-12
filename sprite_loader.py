import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SpriteLoader:
    """Utilitário para carregar e gerenciar sprites"""
    
    def __init__(self):
        """Inicializa o carregador de sprites"""
        self.sprites = {}
        self.assets_path = "assets/images"
        self.carregar_sprites()
    
    def carregar_sprites(self):
        """Carrega todos os sprites necessários"""
        sprites_config = {
            "player": {
                "file": "player_submarine.png",
                "size": (60, 30)
            },
            "enemy_jellyfish": {
                "file": "enemy_jellyfish.png", 
                "size": (40, 40)
            },
            "enemy_fish": {
                "file": "enemy_octopus.png",  # Usando octopus como placeholder
                "size": (30, 20)
            },
            "enemy_crab": {
                "file": "enemy_crab.png",
                "size": (35, 25)
            },
            "boss_octopus": {
                "file": "enemy_octopus.png",
                "size": (120, 80)
            },
            "projectile": {
                "file": "projectile_bubble.png",
                "size": (15, 15)
            },
            "coral": {
                "file": "coral_red.png",
                "size": (30, 30)
            },
            "powerup_shield": {
                "file": "powerup_shield.png",
                "size": (25, 25)
            },
            "powerup_speed": {
                "file": "powerup_damage.png",  # Usando damage como placeholder
                "size": (25, 25)
            },
            "powerup_torpedo": {
                "file": "powerup_damage.png",  # Usando damage como placeholder
                "size": (25, 25)
            }
        }
        
        for sprite_name, config in sprites_config.items():
            self.sprites[sprite_name] = self.carregar_sprite(
                config["file"], 
                config["size"]
            )
    
    def carregar_sprite(self, filename, size):
        """Carrega um sprite específico"""
        filepath = resource_path(os.path.join(self.assets_path, filename))
        
        try:
            if os.path.exists(filepath):
                # Carrega a imagem
                image = pygame.image.load(filepath)
                image = image.convert_alpha()
                
                # Redimensiona se necessário
                if size:
                    image = pygame.transform.scale(image, size)
                
                return image
            else:
                # Cria sprite placeholder se arquivo não existir
                return self.criar_sprite_placeholder(size, filename)
        except Exception as e:
            print(f"Erro ao carregar sprite {filename}: {e}")
            return self.criar_sprite_placeholder(size, filename)
    
    def criar_sprite_placeholder(self, size, filename):
        """Cria um sprite placeholder colorido"""
        if not size:
            size = (32, 32)
        
        # Cria superfície com transparência
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Cor baseada no nome do arquivo
        if "player" in filename:
            color = (0, 150, 255)  # Azul
        elif "enemy" in filename:
            color = (255, 100, 100)  # Vermelho
        elif "boss" in filename:
            color = (128, 0, 128)  # Roxo
        elif "projectile" in filename:
            color = (255, 255, 0)  # Amarelo
        elif "coral" in filename:
            color = (255, 100, 150)  # Rosa
        elif "powerup" in filename:
            color = (0, 255, 0)  # Verde
        else:
            color = (128, 128, 128)  # Cinza
        
        # Desenha retângulo colorido
        pygame.draw.rect(surface, color, (0, 0, size[0], size[1]))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, size[0], size[1]), 2)
        
        return surface
    
    def get_sprite(self, sprite_name):
        """Retorna um sprite específico"""
        return self.sprites.get(sprite_name, None)
    
    def get_sprite_rect(self, sprite_name, x, y):
        """Retorna o retângulo de um sprite na posição especificada"""
        sprite = self.get_sprite(sprite_name)
        if sprite:
            rect = sprite.get_rect()
            rect.x = x
            rect.y = y
            return rect
        return pygame.Rect(x, y, 32, 32)  # Retângulo padrão 