import queue
import sounddevice as sd
import json
import time
from vosk import Model, KaldiRecognizer

# ====== SETTINGS ======
MODEL_PATH = "model/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
SILENCE_TIMEOUT = 10

# ====== GLOBALS ======
_model = None
_recognizer = None
audio_queue = queue.Queue()
recording = False
_on_result = None
_on_partial = None
_on_stop = None


# ----- LOAD MODEL ----
# Ensure Vosk model and recognizer are ready
def _ensure_model():
    global _model, _recognizer
    if _model is None:
        _model = Model(MODEL_PATH)
        _recognizer = KaldiRecognizer(_model, SAMPLE_RATE)

# ----- CALLBACK FOR AUDIO ----
# Receive audio chunks and put them in a queue
def _callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


# ----- START LISTENING ----
# Start recording audio and transcribing in real-time.
# Accepts optional callbacks (on_result(text), on_stop()).
def start_listening(on_result=None, on_stop=None, on_partial=None):
    global recording, _on_result, _on_partial, _on_stop
    if recording:
        return

    _ensure_model()
    _on_result = on_result
    _on_partial = on_partial
    _on_stop = on_stop

    while not audio_queue.empty():
        audio_queue.get_nowait()

    recording = True
    last_speech_time = time.time()  
    last_text = ""  

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                               dtype="int16", channels=1, callback=_callback):
            while recording:
                try:
                    data = audio_queue.get(timeout=0.5)
                except queue.Empty:
                    if time.time() - last_speech_time > SILENCE_TIMEOUT:
                        break
                    continue

                try:
                    if _recognizer.AcceptWaveform(data):
                        res = json.loads(_recognizer.Result())
                        text = res.get("text", "").strip()
                        if text and text != last_text:
                            last_text = text
                            last_speech_time = time.time()
                            if _on_result:
                                _on_result(text)
                    
                except Exception as e:
                    print("Recognition chunk error:", e)
                    continue

                if time.time() - last_speech_time > SILENCE_TIMEOUT:
                    break
    finally:
        try:
            final = json.loads(_recognizer.FinalResult()).get("text", "").strip()
            if final and final != last_text and _on_result:
                _on_result(final)
        except Exception:
            pass

        recording = False
        if _on_stop:
            _on_stop()


# ----- STOP LISTENING ----
# Stop the STT recording loop immediately.
def stop_listening():
    global recording
    recording = False
    try:
        audio_queue.put(b"")
    except Exception:
        pass