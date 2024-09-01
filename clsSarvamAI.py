###############################################################
####                                                       ####
#### Written By: Satyaki De                                ####
#### Written Date:  25-Aug-2024                            ####
#### Modified Date: 31-Aug-2024                            ####
####                                                       ####
#### Objective: This script will read the audio inputs     ####
#### in the native Indic languages & then provides the     ####
#### response as part of the Sarvam AI LLM response.       ####
####                                                       ####
###############################################################

import clsTemplate as ct
import speech_recognition as sr

import datetime
import logging
import time
import os
import asyncio
import speech_recognition as sr
from clsConfigClient import clsConfigClient as cf
from pydub import AudioSegment

import requests
import sounddevice as sd
import numpy as np
import io
import wave
import json
import base64
import re
import soundfile as sf

from queue import Queue
from threading import Thread

audio_base64 = []

# Disabling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

var1 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print('*' *60)
DInd = cf.conf['DEBUG_IND']

templateVal_1 = ct.templateVal_1

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

########################################################
################  End Of Global Area   #################
########################################################
class BreakOuterLoop(Exception):
    pass

class clsSarvamAI:
    def __init__(self):
        self.audioPath = str(cf.conf['AUDIO_PATH'])
        self.audioFile = str(cf.conf['AUDIO_FILE'])
        self.function1 = str(cf.conf['FUNC_1'])
        self.function2 = str(cf.conf['FUNC_2'])
        self.function3 = str(cf.conf['FUNC_3'])
        self.url = str(cf.conf['BASE_URL'])
        self.model_1 = str(cf.conf['MODEL_1'])
        self.model_2 = str(cf.conf['MODEL_2'])
        self.model_3 = str(cf.conf['MODEL_3'])
        self.sarvamAPIKey = str(cf.conf['SARVAM_AI_KEY'])
        self.url_1 = self.url + self.function1
        self.url_2 = self.url + self.function2
        self.url_3 = self.url + self.function3
        self.WavFile = self.audioPath + self.audioFile
        self.langCode_1 = str(cf.conf['BENGALI_CD'])
        self.langCode_2 = str(cf.conf['ENGLISH_CD'])
        self.speakerName = str(cf.conf['SPKR_NAME'])
        self.speakerGender = str(cf.conf['SPKR_GNDR'])

    def createWavFile(self, audio, output_filename="output.wav", target_sample_rate=16000):
        try:
            # Get the raw audio data as bytes
            audio_data = audio.get_raw_data()

            # Get the original sample rate
            original_sample_rate = audio.sample_rate

            # Open the output file in write mode
            with wave.open(output_filename, 'wb') as wf:
                # Set parameters: nchannels, sampwidth, framerate, nframes, comptype, compname
                wf.setnchannels(1)  # Assuming mono audio
                wf.setsampwidth(2)  # 16-bit audio (int16)
                wf.setframerate(original_sample_rate)

                # Write audio data in chunks
                chunk_size = 1024 * 10  # Chunk size (adjust based on memory constraints)
                for i in range(0, len(audio_data), chunk_size):
                    wf.writeframes(audio_data[i:i+chunk_size])

            # Log the current timestamp
            var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print('Audio Time: ', str(var))

            return 0

        except Exception as e:
            print('Error: <Wav File Creation>: ', str(e))
            return 1

    def chunkBengaliResponse(self, text, max_length=500):
        try:
            chunks = []
            current_chunk = ""

            # Use regex to split on sentence-ending punctuation
            sentences = re.split(r'(।|\?|!)', text)

            for i in range(0, len(sentences), 2):
                sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')

                if len(current_chunk) + len(sentence) <= max_length:
                    current_chunk += sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence

            if current_chunk:
                chunks.append(current_chunk.strip())

            return chunks
        except Exception as e:
            x = str(e)
            print('Error: <<Chunking Bengali Response>>: ', x)

            return ''

    def playWav(self, audio_data):
        try:
            # Create a wav file object from the audio data
            WavFile = wave.open(io.BytesIO(audio_data), 'rb')

            # Extract audio parameters
            channels = WavFile.getnchannels()
            sample_width = WavFile.getsampwidth()
            framerate = WavFile.getframerate()
            n_frames = WavFile.getnframes()

            # Read the audio data
            audio = WavFile.readframes(n_frames)
            WavFile.close()

            # Convert audio data to numpy array
            dtype_map = {1: np.int8, 2: np.int16, 3: np.int32, 4: np.int32}
            audio_np = np.frombuffer(audio, dtype=dtype_map[sample_width])

            # Reshape audio if stereo
            if channels == 2:
                audio_np = audio_np.reshape(-1, 2)

            # Play the audio
            sd.play(audio_np, framerate)
            sd.wait()

            return 0
        except Exception as e:
            x = str(e)
            print('Error: <<Playing the Wav>>: ', x)

            return 1

    def audioPlayerWorker(self, queue):
        try:
            while True:
                var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                print('Response Audio Time: ', str(var))
                audio_bytes = queue.get()
                if audio_bytes is None:
                    break
                self.playWav(audio_bytes)
                queue.task_done()

            return 0
        except Exception as e:
            x = str(e)
            print('Error: <<Audio Player Worker>>: ', x)

            return 1

    async def processChunk(self, chText, url_3, headers):
        try:
            sarvamAPIKey = self.sarvamAPIKey
            model_1 = self.model_1
            langCode_1 = self.langCode_1
            speakerName = self.speakerName

            print()
            print('Chunk Response: ')
            vText = chText.replace('*','').replace(':',' , ')
            print(vText)

            payload_3 = {
                "inputs": [vText],
                "target_language_code": langCode_1,
                "speaker": speakerName,
                "pitch": 0.15,
                "pace": 0.95,
                "loudness": 2.1,
                "speech_sample_rate": 16000,
                "enable_preprocessing": True,
                "model": model_1
            }
            response_3 = requests.request("POST", url_3, json=payload_3, headers=headers)
            audio_data = response_3.text
            data = json.loads(audio_data)
            byte_data = data['audios'][0]
            audio_bytes = base64.b64decode(byte_data)

            return audio_bytes
        except Exception as e:
            x = str(e)
            print('Error: <<Process Chunk>>: ', x)
            audio_bytes = base64.b64decode('')

            return audio_bytes

    async def processAudio(self, audio):
        try:
            model_2 = self.model_2
            model_3 = self.model_3
            url_1 = self.url_1
            url_2 = self.url_2
            url_3 = self.url_3
            sarvamAPIKey = self.sarvamAPIKey
            audioFile = self.audioFile
            WavFile = self.WavFile
            langCode_1 = self.langCode_1
            langCode_2 = self.langCode_2
            speakerGender = self.speakerGender

            headers = {
                "api-subscription-key": sarvamAPIKey
            }

            audio_queue = Queue()
            data = {
                "model": model_2,
                "prompt": templateVal_1
            }
            files = {
                "file": (audioFile, open(WavFile, "rb"), "audio/wav")
            }

            response_1 = requests.post(url_1, headers=headers, data=data, files=files)
            tempDert = json.loads(response_1.text)
            regionalT = tempDert['transcript']
            langCd = tempDert['language_code']
            statusCd = response_1.status_code
            payload_2 = {
                "input": regionalT,
                "source_language_code": langCode_2,
                "target_language_code": langCode_1,
                "speaker_gender": speakerGender,
                "mode": "formal",
                "model": model_3,
                "enable_preprocessing": True
            }

            response_2 = requests.request("POST", url_2, json=payload_2, headers=headers)
            regionalT_2 = response_2.text
            data_ = json.loads(regionalT_2)
            regionalText = data_['translated_text']
            chunked_response = self.chunkBengaliResponse(regionalText)

            audio_thread = Thread(target=self.audioPlayerWorker, args=(audio_queue,))
            audio_thread.start()

            for chText in chunked_response:
                audio_bytes = await self.processChunk(chText, url_3, headers)
                audio_queue.put(audio_bytes)

            audio_queue.join()
            audio_queue.put(None)
            audio_thread.join()

            var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print('Retrieval Time: ', str(var))

            return 0

        except Exception as e:
            x = str(e)
            print('Error: <<Processing Audio>>: ', x)

            return 1

    def initializeMicrophone(self):
        try:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found (device_index={index})")
            return sr.Microphone()
        except Exception as e:
            x = str(e)
            print('Error: <<Initiating Microphone>>: ', x)

            return ''

    def realTimeTranslation(self):
        try:
            WavFile = self.WavFile
            recognizer = sr.Recognizer()
            try:
                microphone = self.initializeMicrophone()
            except Exception as e:
                print(f"Error initializing microphone: {e}")
                return

            with microphone as source:
                print("Adjusting for ambient noise. Please wait...")
                recognizer.adjust_for_ambient_noise(source, duration=5)
                print("Microphone initialized. Start speaking...")

                try:
                    while True:
                        try:
                            print("Listening...")
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                            print("Audio captured. Recognizing...")

                            #var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            #print('Before Audio Time: ', str(var))

                            self.createWavFile(audio, WavFile)

                            try:
                                text = recognizer.recognize_google(audio, language="bn-BD")  # Bengali language code
                                sentences = text.split('।')  # Bengali full stop

                                print('Sentences: ')
                                print(sentences)
                                print('*'*120)

                                if not text:
                                    print("No speech detected. Please try again.")
                                    continue

                                if str(text).lower() == 'টাটা':
                                    raise BreakOuterLoop("Based on User Choice!")

                                asyncio.run(self.processAudio(audio))

                            except sr.UnknownValueError:
                                print("Google Speech Recognition could not understand audio")
                            except sr.RequestError as e:
                                print(f"Could not request results from Google Speech Recognition service; {e}")

                        except sr.WaitTimeoutError:
                            print("No speech detected within the timeout period. Listening again...")
                        except BreakOuterLoop:
                            raise
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

                        time.sleep(1)  # Short pause before next iteration

                except BreakOuterLoop as e:
                    print(f"Exited : {e}")

            # Removing the temporary audio file that was generated at the begining
            os.remove(WavFile)

            return 0
        except Exception as e:
            x = str(e)
            print('Error: <<Real-time Translation>>: ', x)

            return 1
