import json
import ollama
import vosk
import sounddevice as sd
import numpy as np
import pyttsx3

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
            'content' : 'You are a personal assistant named Jarvis. You are to be as helpful as possible specifically inthe manner of technical problems. Keep your answers clear and concice unless specified otherwise.'
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

            #reduced_data = noisereduce.reduce_noise(y=data, sr=16000)

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
        response = ollama.chat(model=Agent_model, messages=[{'role': 'user', 'content' : user_input}], stream=False)
        print("Jarvis: ", response['message']['content'])

        speak(response['message']['content'])
