import subprocess as sp, os, traceback
from urllib.request import urlopen
import time

# path to ffmpeg bin
FFMPEG_PATH = os.environ['FFMPEG_PATH'] 

def convert(file_path):
    command = [
        FFMPEG_PATH, '-i', file_path, '-y', '-loglevel', '16','-threads', '2', '-c:a', 'opus', '-f', 'ogg', '-'
        ##'wget', '-O', '-', file_path
    ]
    # Get raw audio from stdout of ffmpeg shell command
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
    raw_audio = pipe.stdout.read()
    return raw_audio

# [START import_libraries]
import base64
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
# [END import_libraries]


# [START authenticating]
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
# [END authenticating]


def speech_to_text_google(speech_file):
    """Transcribe the given audio file.
    Args:
        speech_file: the name of the audio file.
        Hung's modification: take in binary raw input
    """
    # [START construct_request]
    # Method 1. Take in file input
    # with open(speech_file, 'rb') as speech: # --> for file
        # Base64 encode the binary audio file for inclusion in the JSON
        # request.
        # speech_content = base64.b64encode(speech.read())

    # Method 2. Take in raw binary input
    # Base64 encode the binary audio file for inclusion in the JSON
    # request.
    speech_content = base64.b64encode(speech_file)

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'OGG_OPUS',
                'sampleRate': 48000,
                'maxAlternatives': 1,
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    # [END construct_request]
    # [START send_request]
    response = service_request.execute() # return a dict object
    # [END send_request]
    if 'results' in response:
      results =  sorted(response['results'], reverse=True)
      #print(results)
      final_result = results[0]['alternatives'][0]['transcript']
    else:
      #print(json.dumps(response))
      final_result = "Sorry I couldn't recognize that"
    return final_result


def transcribe(audio_url):
    time1 = time.time()
    #print("Start conversion: " + str(time.time()))
    raw_audio = convert(audio_url)
    time2 = time.time()
    print("conversion: " + str(time2 - time1))
    #print(len(raw_audio))
    time3 = time.time()
    #print("Send to Google: " + str(time.time()))
    final_result = speech_to_text_google(raw_audio)
    time4= time.time()
    print("Google: " + str(time4 - time3))
    #print("=============\n"+final_result)
    return final_result


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
    
