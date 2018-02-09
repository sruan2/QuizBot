import subprocess as sp, os, traceback
from urllib.request import urlopen

# path to ffmpeg bin
FFMPEG_PATH = os.environ['FFMPEG_PATH'] 

def convert(file_path):
    command = [
        FFMPEG_PATH, '-i', file_path, '-y', '-loglevel', '16','-threads', '8',  '-c:v', 'mp4' , '-f', 'wav' , '-'
    ]
    # Get raw audio from stdout of ffmpeg shell command
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
    raw_audio = pipe.stdout.read()
    return raw_audio

def transcribe(audio_url):
    raw_audio = convert(audio_url)
    print(len(raw_audio))


    # #print(audio_url)
    # name = audio_url[-8:]
    # aacfile = urlopen(audio_url)
    # with open('gcloud_speech/'+name+'.aac', "wb") as handle:
    #     handle.write(aacfile.read())
    
    # cmdline = ['avconv', '-i', 'gcloud_speech/'+name+'.aac', '-y', '-ar', '48000', '-ac', '1', 'gcloud_speech/'+name+'.flac']
    # sp.call(cmdline)

    # return run_quickstart('gcloud_speech/'+name+'.flac')


def run_quickstart(file_name):
    # [START speech_quickstart]
    import io
    import os

    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END migration_import]

    # Instantiates a client
    # [START migration_client]
    client = speech.SpeechClient()
    # [END migration_client]


    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    final_result = ""

    for result in response.results:
        final_result += result.alternatives[0].transcript
    # [END speech_quickstart]

    return final_result

### testing ###
if __name__ == "__main__":
    run_quickstart("gcloud_speech/test.wav")
    
