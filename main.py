import tts_engine
from gui import TTS_STT_App

if __name__ == "__main__":
    # Set default TTS settings
    tts_engine.changeVoiceSettings(rate=200, volume=1.0, gender="Male")
    
    # Create and run the GUI
    app = TTS_STT_App()
    app.mainloop()
