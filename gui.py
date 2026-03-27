import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import tts_engine
import stt_engine

class TTS_STT_App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === Window Settings ===
        self.title("🎙 Speakify - TTS & STT APP")
        self.geometry("800x650")
        self.resizable(False, False) 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State
        self.listening_thread = None
        self.is_listening = False

        # === TTS Section ===
        tts_frame = ctk.CTkFrame(self, corner_radius=15)
        tts_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(tts_frame, text="Enter text to speak:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.text_input = ctk.CTkTextbox(tts_frame, height=120)
        self.text_input.pack(fill="x", padx=10, pady=(0, 10))

        controls_frame = ctk.CTkFrame(tts_frame)
        controls_frame.pack(fill="x", padx=10, pady=(5, 10))

        # Volume
        ctk.CTkLabel(controls_frame, text="Volume").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.volume_var = ctk.DoubleVar(value=tts_engine.current_volume)
        ctk.CTkSlider(controls_frame, from_=0.0, to=1.0, variable=self.volume_var, command=self.on_volume_change).grid(row=0, column=1, sticky="ew", padx=5)

        # Rate
        ctk.CTkLabel(controls_frame, text="Rate").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.rate_var = ctk.IntVar(value=tts_engine.current_rate)
        ctk.CTkSlider(controls_frame, from_=100, to=300, variable=self.rate_var, command=self.on_rate_change).grid(row=1, column=1, sticky="ew", padx=5)

        # Gender
        gender_frame = ctk.CTkFrame(controls_frame, corner_radius=10)
        gender_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="ns")
        self.gender_var = ctk.StringVar(value=tts_engine.current_gender)
        ctk.CTkLabel(gender_frame, text="Voice Gender", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=5)
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male", command=self.on_gender_change).pack(anchor="w", padx=10, pady=2)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female", command=self.on_gender_change).pack(anchor="w", padx=10, pady=2)

        controls_frame.grid_columnconfigure(1, weight=1)

        # TTS Buttons
        btn_frame = ctk.CTkFrame(tts_frame)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(btn_frame, text="▶ Speak Text", command=self.speak_text).pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="⏹ Stop", command=self.stop_speaking, fg_color="red", hover_color="#A13434").pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="📂  Speak From File", command=self.speak_from_file).pack(side="left", expand=True, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="🔄  Reset", command=self.reset_tts_box).pack(side="left", padx=5, pady=5)

        # === STT Section ===
        stt_frame = ctk.CTkFrame(self, corner_radius=15)
        stt_frame.pack(fill="both", expand=True, padx=20, pady=15)

        mic_reset_frame = ctk.CTkFrame(stt_frame, fg_color="transparent")
        mic_reset_frame.pack(fill="x", padx=10, pady=10)

        self.mic_btn = ctk.CTkButton(
            mic_reset_frame, 
            text="🎤 Start Listening", 
            command=self.toggle_listening, 
            height=40, 
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="green",
            hover_color="#3a663a"
        )
        self.mic_btn.pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            mic_reset_frame, 
            text="🔄 Reset", 
            command=self.reset_transcription, 
            height=40
        ).pack(side="right")

        self.transcription_box = ctk.CTkTextbox(stt_frame, wrap="word", height=200)
        self.transcription_box.pack(fill="both", expand=True, padx=10, pady=10)

    # ==== TTS Handlers ====
    def on_volume_change(self, event=None):
        tts_engine.changeVoiceSettings(volume=self.volume_var.get())

    def on_rate_change(self, event=None):
        tts_engine.changeVoiceSettings(rate=int(self.rate_var.get()))

    def on_gender_change(self):
        tts_engine.changeVoiceSettings(gender=self.gender_var.get())

    def speak_text(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Input needed", "Please enter some text to speak.")
            return
        threading.Thread(target=tts_engine.speakText, args=(text,), daemon=True).start()

    def stop_speaking(self):
        threading.Thread(target=tts_engine.stopSpeaking, daemon=True).start()

    def speak_from_file(self):
        file_path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
        if file_path:
            threading.Thread(target=tts_engine.speakFromFile, args=(file_path,), daemon=True).start()

    def reset_tts_box(self):
        self.text_input.delete("1.0", "end")

    # ==== STT Handlers ====
    def show_partial(self, partial_text):
        self.transcription_box.delete("end-2l", "end")
        self.transcription_box.insert("end", partial_text + "\n")
        self.transcription_box.see("end")

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.animate_mic(True)

            def on_result_threadsafe(text):
                self.after(0, self.update_transcription, text + " ")

            def on_partial_threadsafe(text):
                self.after(0, self.show_partial, text)

            def on_stop_threadsafe():
                self.after(0, self.on_stt_stop)

            self.listening_thread = threading.Thread(
                target=stt_engine.start_listening,
                args=(on_result_threadsafe, on_stop_threadsafe, on_partial_threadsafe),
                daemon=True
            )
            self.listening_thread.start()
        else:
            stt_engine.stop_listening()

    def on_stt_stop(self):
        self.is_listening = False
        self.animate_mic(False)

    def update_transcription(self, text):
        self.transcription_box.insert("end", text)
        self.transcription_box.see("end")

    def reset_transcription(self):
        self.transcription_box.delete("1.0", "end")

    # ==== Mic Animation ====
    def animate_mic(self, listening):
        if listening:
            self.mic_btn.configure(fg_color="red", hover_color="#A13434", text="⏹ Stop Listening")
        else:
            self.mic_btn.configure(fg_color="green", hover_color="#3a663a", text="🎤 Start Listening")
