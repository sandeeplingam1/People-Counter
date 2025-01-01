import os
import threading
from gtts import gTTS
from pygame import mixer
import time

class AudioEngine:
    def __init__(self):
        self.mixer_initialized = False
        self._lock = threading.Lock()
        self.last_played_text = ""

    def _init_mixer(self):
        with self._lock:
            if not self.mixer_initialized:
                mixer.init()
                self.mixer_initialized = True

    def speak(self, text, block=False):
        """
        Announces the text using TTS.
        """
        if text == self.last_played_text:
            return

        def _announce():
            self._init_mixer()
            try:
                # Create a temporary file for the speech
                filename = f"speech_{int(time.time())}.mp3"
                tts = gTTS(text=text, slow=False)
                tts.save(filename)
                
                with self._lock:
                    mixer.music.load(filename)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(0.1)
                
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)
                self.last_played_text = text
            except Exception as e:
                print(f"Audio Error: {e}")

        t = threading.Thread(target=_announce)
        t.start()
        if block:
            t.join()
