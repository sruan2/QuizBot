import argparse
import base64
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

import subprocess as sp, os, traceback

# path to ffmpeg bin
FFMPEG_PATH = "ffmpeg"
#os.environ['FFMPEG_PATH']

DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')


def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)


def speech_to_text_google(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    speech_content = base64.b64encode(speech_file)

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                'languageCode': 'en-US',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    print(json.dumps(response))


def transcribe(audio_url):
    raw_audio = convert(audio_url)
    return speech_to_text_google(raw_audio)

def convert(file_path):
    try:
        command = [
            FFMPEG_PATH, '-i', file_path, '-y', '-loglevel', '16','-threads', '8',  '-c:v', 'mp4' , '-f', 'wav' , '-'
        ]
        # Get raw audio from stdout of ffmpeg shell command
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        raw_audio = pipe.stdout.read()
        return raw_audio
        
    except:
        print("[BUG] PID " + str(os.getpid())+": Transcription failed")
        return ""
