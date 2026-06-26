import os
import pygame
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / 'music'

class SoundManager:
    _instance = None

    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self.current_music = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.enabled = True
        except Exception:
            self.enabled = False
        if self.enabled:
            self._load_sounds()

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_one(self, name):
        path = MUSIC_DIR / f'{name}.wav'
        if path.exists():
            try:
                self.sounds[name] = pygame.mixer.Sound(str(path))
            except Exception:
                pass

    def _load_sounds(self):
        for name in [
            'menu','u1_space','u2_uni','u3_delivery','u4_office','victory','gameover',
            'shoot','hit','powerup','portal','boss','jump'
        ]:
            self._load_one(name)
        # Lower some SFX a bit.
        for name, vol in {'shoot':0.25,'hit':0.35,'powerup':0.35,'portal':0.4,'boss':0.45,'jump':0.28}.items():
            if name in self.sounds:
                self.sounds[name].set_volume(vol)

    def play_music(self, name, loops=-1):
        if not self.enabled:
            return
        if self.current_music == name:
            return
        snd = self.sounds.get(name)
        if snd is None:
            return
        try:
            pygame.mixer.stop()
        except Exception:
            pass
        try:
            snd.play(loops=loops)
            self.current_music = name
        except Exception:
            pass

    def stop_music(self):
        if not self.enabled:
            return
        try:
            pygame.mixer.stop()
            self.current_music = None
        except Exception:
            pass

    def play_sfx(self, name):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd is None:
            return
        try:
            snd.play()
        except Exception:
            pass
