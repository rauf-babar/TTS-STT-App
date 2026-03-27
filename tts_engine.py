import pyttsx3
import os

# ====== GLOBAL SETTINGS ======
current_rate = 200
current_volume = 1.0
current_gender = "Male"

# Holds the engine that's currently speaking (None if idle)
current_engine = None


# ====== ENGINE CREATOR ======
# Create and configure a fresh pyttsx3 engine with current settings
def create_engine():
    e = pyttsx3.init()
    e.setProperty("rate", current_rate)
    e.setProperty("volume", current_volume)

    voices = e.getProperty("voices")
    index = 0 if current_gender.lower() == "male" else 1
    if index < len(voices):
        e.setProperty("voice", voices[index].id)

    return e


# ====== SPEAK TEXT ======
# Speak a given string using current settings
def speakText(text):
    global current_engine
    try:
        e = create_engine()
        current_engine = e
        e.say(text)
        e.runAndWait()
    except Exception as ex:
        speakError(str(ex))
    finally:
        current_engine = None


# ====== SPEAK FROM FILE ======
# Read and speak text from file
def speakFromFile(file_path):
    if not os.path.isfile(file_path):
        return speakError("File not found.")
    if not file_path.lower().endswith(".txt"):
        return speakError("Invalid file format. Only text files allowed.")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return speakError("File is empty.")
            speakText(content)
    except Exception as ex:
        speakError(str(ex))


# ====== CHANGE VOICE SETTINGS ======
# Update global TTS settings for future calls
def changeVoiceSettings(rate=None, volume=None, gender=None):
    global current_rate, current_volume, current_gender
    if rate is not None:
        current_rate = rate
    if volume is not None:
        current_volume = volume
    if gender is not None:
        current_gender = gender


# ====== STOP SPEAKING ======
# Stop the currently speaking engine (if any)
def stopSpeaking():
    global current_engine
    if current_engine:
        try:
            current_engine.stop()
        except Exception as ex:
            speakError(str(ex))
    else:
        speakError("No speech in progress.")


# ====== ERROR HANDLER ======
# Print and speak error messages
def speakError(message):
    try:
        e = create_engine()
        e.say(f"Error: {message}")
        e.runAndWait()
    except:
        pass
