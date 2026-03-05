from pygame import mixer

from src.config.settings import Settings

class SoundPlayer:
    _current_music = None

    @staticmethod
    def play_music(music: str, volume: float = 1.0) -> None:
        if SoundPlayer._current_music == music:
            return
            
        path = Settings.SOUNDS_PATH / Settings.SOUNDS_MAP[music]
        try:
            mixer.music.load(str(path))
            mixer.music.set_volume(volume * Settings.MUSIC_VOLUME_PERCENT / 100)
            mixer.music.play(-1)
            SoundPlayer._current_music = music
        except Exception as e:
            print(f"No se pudo cargar la música: {e}")

    @staticmethod
    def play_sfx(key: str, volume: float = 0.5):
        sound = Settings.SOUNDS.get(key)
        if sound:
            sound.set_volume(volume * Settings.SFX_VOLUME_PERCENT / 100)
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