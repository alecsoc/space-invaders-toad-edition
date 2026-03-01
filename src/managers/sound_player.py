from pygame import mixer

from src.config.settings import Settings

class SoundPlayer:
    _current_music = None

    @staticmethod
    def play_music(music):
        if SoundPlayer._current_music == music:
            return
            
        path = Settings.SOUNDS_PATH / Settings.SOUNDS_MAP[music]
        try:
            mixer.music.load(str(path))
            mixer.music.play(-1)
            SoundPlayer._current_music = music
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")

    @staticmethod
    def play_sfx(key, volume=0.5):
        sound = Settings.SOUNDS.get(key)
        if sound:
            sound.set_volume(volume)
            sound.play()

    @staticmethod
    def stop_music():
        mixer.music.stop()
        SoundPlayer._current_music = None

    @staticmethod
    def stop_all():
        mixer.music.stop()
        mixer.stop()
        SoundPlayer._current_music = None