import pyxel as px
import pygame as pg
# Defina uma classe para gerenciar os sons


class Sounds:
    def __init__(self):
        # Carregua os sons:
        px.sound(0).set(
            notes='g3f3d#3',
            tones='n',
            volumes='531',
            effects='',
            speed=4,
        )

        px.sound(1).set(
            notes='a#4g4g4e4d#4d#4d#4f3d#3c#3c#3c#3c#3',
            tones='nnnnnnnnnnnnn',
            volumes='6677775433322',
            effects='',
            speed=2,
        )
        px.sound(2).set(
            notes='g#4g4e4d#4c4g3e3',
            tones='n',
            volumes='7765342',
            effects='',
            speed=3
        )

    # Define as funções para tocar os sons:
    def play_hit_sound_mob(self):
        px.play(0, 0)

    def play_hit_sound_player(self):
        px.play(1, 1)

    def play_atack_sound_mob():
        px.play(2, 2)


class Sound_Track():
    def __init__(self, volume):
        # soud pygame
        pg.mixer.init()
        self.sound_track = pg.mixer.Sound(
            "Projeto em Python/soud_track.mp3")
        self.sound_track.set_volume(volume)

    # função para iniciar minha musica
    def sound_track(self):
        self.sound_track.play(0, 0)
    # função para pausar minha musica

    def pause(self):
        self.sound_track.stop()
    # função para retomar minha musica

    def resume(self):
        self.sound_track.play(0, 0)
