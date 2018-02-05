import subprocess as sp, os, traceback

# path to ffmpeg bin
FFMPEG_PATH = "/home/ubuntu/quizbot_dev/ffmpeg/"
#os.environ['FFMPEG_PATH']

# [START import_libraries]
# import base64
# import json

# from googleapiclient import discovery
# import httplib2
# from oauth2client.client import GoogleCredentials
# # [END import_libraries]


# # [START authenticating]
# DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
#                  'version={apiVersion}')


# # Application default credentials provided by env variable
# # GOOGLE_APPLICATION_CREDENTIALS
# def get_speech_service():
#     credentials = GoogleCredentials.get_application_default().create_scoped(
#         ['https://www.googleapis.com/auth/cloud-platform'])
#     http = httplib2.Http()
#     credentials.authorize(http)

#     return discovery.build(
#         'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
# # [END authenticating]


# def speech_to_text_google(speech_file):
#     """Transcribe the given audio file.
#     Args:
#         speech_file: the name of the audio file.
#         Hung's modification: take in binary raw input
#     """
#     # [START construct_request]
#     # Method 1. Take in file input
#     with open(speech_file, 'rb') as speech: # --> for file
#         #Base64 encode the binary audio file for inclusion in the JSON request.
#         speech_content = base64.b64encode(speech.read())

#     # Method 2. Take in raw binary input
#     # Base64 encode the binary audio file for inclusion in the JSON
#     # request.
    
#     #speech_content = base64.b64encode(speech_file)

#     service = get_speech_service()
#     service_request = service.speech().syncrecognize(
#         body={
#             'config': {
#                 'encoding': 'LINEAR16',
#                 'sampleRate': 8000,
#                 'maxAlternatives': 1,
#             },
#             'audio': {
#                 'content': speech_content.decode('UTF-8')
#                 }
#             })
#     # [END construct_request]
#     # [START send_request]
#     response = service_request.execute() # return a dict object
#     # [END send_request]
#     if 'results' in response:
#         results =  sorted(response['results'], reverse=True)
#         print(results)
#         final_result = results[0]['alternatives'][0]['transcript']
#     else:
#         print(json.dumps(response))
#         final_result = "Sorry I couldn't recognize that"
#     return final_result


def transcribe(audio_url):
    raw_audio = convert(audio_url)
    return speech_to_text_google(raw_audio)

def convert(audio_url):
    command = [
        FFMPEG_PATH, '-i', audio_url, '-y', '-loglevel', '16','-threads', '8',  '-c:v', 'mp4' , '-f', 'wav' , '-'
    ]
    # Get raw audio from stdout of ffmpeg shell command
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8, shell=True)
    raw_audio = pipe.stdout.read()
    return raw_audio
  


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
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]
      

### testing ###
if __name__ == "__main__":
    run_quickstart("gcloud_speech/quit.raw")
    
