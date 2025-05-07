import json
import ollama
import vosk
import sounddevice as sd
import numpy as np
import pyttsx3
import webbrowser
import os
import ast

COMMANDS = {
    "open_browser": lambda: webbrowser.open("https://www.google.com"),
    "shutdown": lambda: os.system("shutdown /s /t 1"),
    "greet": lambda: speak("Hello, how can I assist you?")
}

#model file locations/names
Agent_model = "jarvis-model:mk1"
VoiceRec_Model = r"C:\Users\Mystic\Desktop\Models\vosk-model-en-us-0.22"

#speech recognition model initialisation
vosk_model = vosk.Model(VoiceRec_Model)
speech_recogniser = vosk.KaldiRecognizer(vosk_model, 16000)

#initialise TTS engine
TTS_engine = pyttsx3.init()
TTS_engine.setProperty('rate', 150) #rate of speech
TTS_engine.setProperty('volume', 1.0) # range of 0.0 - 1.0

audio_device_name = "Speakers (HyperX Quadcast)"

def speak(msg):
    TTS_engine.say(msg)
    TTS_engine.runAndWait()
    TTS_engine.stop()


history = []
def init_History():
    global history
    history = [
        {
            'role' : 'system',
            'content' : "You are a voice assistant named Jarvis. When the user gives a voice command, "
                "you must interpret the command and respond with a JSON object formatted as:\n"
                '{"command": "<command_name>", "text": "<response to speak>"}\n'
                "If it's not a command, just respond normally as a helpful assistant. "
                "Do not explain the JSON format in your answer."
        }
    ]

def append_history(msg):
    history.append(msg)

#gets the pre defined audio device
def GetAudioDevice(deviceName):
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev["name"] == deviceName and dev["max_input_channels"] > 0:
            return i


#listenting function for speech rec.
def listen():
    print("Listening...  (Wake word is 'Hey Jarvis')")

    global speech_text
    speech_text = ""

    with sd.InputStream(samplerate = 16000, channels = 1, dtype = np.int16, device = GetAudioDevice(audio_device_name)) as stream:
        while True:

            data = stream.read(4000)[0]

            if speech_recogniser.AcceptWaveform(data.tobytes()):  # accepts the waveform from the stream into the speech_recogniser

                full_text = speech_recogniser.Result()
                text_data = json.loads(full_text)
                speech_text = text_data.get("text", "")

            else:
                if "hey jarvis" in speech_text.lower():
                    print("You: ", speech_text)

                    return speech_text

while True:

    user_input = listen()
    if user_input.lower() in ["exit", "quit"]:
        break
    if user_input:
        append_history({'role':'user', 'content': user_input})
        response = ollama.chat(model=Agent_model, messages=history, stream=False)
        message = response['message']['content']
        print("Jarvis: ", response['message']['content'])
        print("Jarvis(Raw): ", response)
        # command input parsing, will be moved to a function later
        try:

            #try parsing the command input
            command_data = json.loads(message)
            command = command_data.get("command")
            text = command_data.get("text", "")

            if command in COMMANDS:
                COMMANDS[command]() # execute command function
                speak(text)
            else:
                speak("Sorry sir, it appears I don't have that command active in my database.")
        except json.JSONDecodeError:
            # not a command
            speak(message)

        append_history({'role':'assistant', 'content': message})




        #speak(response['message']['content'])

