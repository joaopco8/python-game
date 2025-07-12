import pygame
import os

class SoundManager:
    def __init__(self):
        """Inicializa o gerenciador de sons"""
        self.sounds = {}
        self.music_playing = False
        self.volume_sfx = 0.7
        self.volume_music = 0.5
        
        # Inicializa o mixer
        pygame.mixer.init()
        
        # Carrega sons (se existirem)
        self.carregar_sons()
    
    def carregar_sons(self):
        """Carrega os arquivos de som"""
        sounds_dir = "assets/sounds"
        
        # Lista de sons para carregar
        sound_files = {
            "tiro": "tiro.wav",
            "coral": "coral.wav", 
            "bolhas": "bolhas.wav",
            "dano": "dano.wav",
            "boss_hit": "boss_hit.wav",
            "vitoria": "vitoria.wav"
        }
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sounds_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(self.volume_sfx)
                except:
                    print(f"Erro ao carregar som: {filepath}")
            else:
                # Cria som placeholder se arquivo não existir
                self.criar_som_placeholder(sound_name)
    
    def criar_som_placeholder(self, sound_name):
        """Cria um som placeholder simples"""
        # Cria um som simples baseado no tipo
        if sound_name == "tiro":
            # Som de tiro (frequência alta)
            self.sounds[sound_name] = self.criar_som_simples(800, 100)
        elif sound_name == "coral":
            # Som de coleta (frequência média)
            self.sounds[sound_name] = self.criar_som_simples(400, 200)
        elif sound_name == "bolhas":
            # Som de bolhas (frequência baixa)
            self.sounds[sound_name] = self.criar_som_simples(200, 300)
        elif sound_name == "dano":
            # Som de dano (frequência baixa)
            self.sounds[sound_name] = self.criar_som_simples(150, 150)
        elif sound_name == "boss_hit":
            # Som de hit no boss (frequência média)
            self.sounds[sound_name] = self.criar_som_simples(600, 100)
        elif sound_name == "vitoria":
            # Som de vitória (frequência alta)
            self.sounds[sound_name] = self.criar_som_simples(1000, 500)
    
    def criar_som_simples(self, frequencia, duracao):
        """Cria um som simples usando pygame"""
        # Cria um som simples baseado em frequência e duração
        sample_rate = 22050
        samples = int(duracao * sample_rate / 1000)
        
        # Gera onda senoidal simples
        import math
        wave = []
        for i in range(samples):
            value = int(32767 * math.sin(2 * math.pi * frequencia * i / sample_rate))
            wave.append(value)
        
        # Converte para bytes
        import array
        sound_array = array.array('h', wave)
        sound_bytes = sound_array.tobytes()
        
        # Cria o som
        sound = pygame.mixer.Sound(buffer=sound_bytes)
        sound.set_volume(self.volume_sfx)
        return sound
    
    def tocar_musica_fundo(self):
        """Toca música de fundo"""
        music_file = "assets/sounds/musica_fundo.ogg"
        
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.volume_music)
                pygame.mixer.music.play(-1)  # -1 para loop infinito
                self.music_playing = True
            except:
                print(f"Erro ao carregar música: {music_file}")
        else:
            # Cria música placeholder
            self.criar_musica_placeholder()
    
    def criar_musica_placeholder(self):
        """Cria uma música de fundo simples"""
        # Cria uma melodia simples usando pygame
        sample_rate = 22050
        samples = int(5 * sample_rate)  # 5 segundos
        
        import math
        wave = []
        for i in range(samples):
            # Melodia simples com diferentes frequências
            t = i / sample_rate
            freq = 220 + 110 * math.sin(2 * math.pi * 0.1 * t)  # Frequência variável
            value = int(16383 * math.sin(2 * math.pi * freq * t))
            wave.append(value)
        
        import array
        sound_array = array.array('h', wave)
        sound_bytes = sound_array.tobytes()
        
        # Salva temporariamente e carrega
        temp_file = "temp_music.ogg"
        with open(temp_file, "wb") as f:
            f.write(sound_bytes)
        
        try:
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.set_volume(self.volume_music)
            pygame.mixer.music.play(-1)
            self.music_playing = True
        except:
            print("Erro ao criar música placeholder")
    
    def parar_musica(self):
        """Para a música de fundo"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def tocar_som(self, sound_name):
        """Toca um efeito sonoro"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def tocar_tiro(self):
        """Toca som de tiro"""
        self.tocar_som("tiro")
    
    def tocar_coral(self):
        """Toca som de coral coletado"""
        self.tocar_som("coral")
    
    def tocar_bolhas(self):
        """Toca som de bolhas"""
        self.tocar_som("bolhas")
    
    def tocar_dano(self):
        """Toca som de dano"""
        self.tocar_som("dano")
    
    def tocar_boss_hit(self):
        """Toca som de hit no boss"""
        self.tocar_som("boss_hit")
    
    def tocar_vitoria(self):
        """Toca som de vitória"""
        self.tocar_som("vitoria")
    
    def set_volume_sfx(self, volume):
        """Define o volume dos efeitos sonoros"""
        self.volume_sfx = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume_sfx)
    
    def set_volume_music(self, volume):
        """Define o volume da música"""
        self.volume_music = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume_music) 