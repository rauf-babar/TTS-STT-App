

# Desktop TTS & STT Application

## Overview

A native desktop application providing offline Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities. Built with Python, it utilizes local machine learning models and native system voices to ensure privacy and fast processing times without requiring an internet connection.

The application features a modern graphical user interface designed for intuitive interaction, complete with multi-threading to ensure the UI remains responsive during audio processing operations.

---

## Key Features

* **Offline Speech Recognition**: Utilizes the Vosk API for accurate, real-time voice transcription without sending audio data to the cloud.
* **Native Text-to-Speech**: Leverages `pyttsx3` to convert text to audio, with dynamic controls for speech rate, volume, and voice gender.
* **Asynchronous Processing**: Implements Python's `threading` library to handle continuous audio listening and speaking tasks without freezing the main event loop.
* **Modern Interface**: Built using `customtkinter` for a sleek, dark-mode native desktop experience.
* **File Processing**: Ability to read and synthesize speech directly from standard text files.

---

## Project Structure

```
Speakify-Voice-Assistant/
│
├── main.py          # Entry point of the application
├── gui.py           # UI logic and layout (TTS_STT_App class)
├── tts_engine.py    # Text-to-Speech logic
├── stt_engine.py    # Speech-to-Text processing using Vosk
├── requirements.txt
├── sample.txt
└── model/           # Directory for Vosk model (not included)
```

---

## Core Dependencies

* `vosk` – Offline speech recognition toolkit
* `pyttsx3` – Offline text-to-speech engine
* `customtkinter` – Modern UI framework for desktop apps
* `sounddevice` – Real-time microphone input handling

---

## Installation and Setup

### Prerequisites

* Python 3.8 or higher
* Working microphone and speakers

---

### 1. Clone the Repository

```bash
git clone https://github.com/rauf-babar/TTS-STT-App.git
cd TTS-STT-App
```

---

### 2. Install Dependencies

It is recommended to create a virtual environment first.

```bash
python -m venv venv
```

Activate the environment:

* **Windows**

```bash
venv\Scripts\activate
```

* **macOS / Linux**

```bash
source venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

### 3. Download the STT Model

Because machine learning models are large, the Vosk model is not included in this repository.

Steps:

1. Download the model: **vosk-model-small-en-us-0.15**
   [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
2. Extract the downloaded folder
3. Create a folder named `model` in the project root
4. Place the extracted model folder inside `model/`

Final structure:

```
model/vosk-model-small-en-us-0.15/
```

---

### 4. Run the Application

```bash
python main.py
```

---

