import subprocess
import speech_recognition as sr
import os.path

def play(command):
    if type(command) is list:
        command = ' '.join(command)
    command = ['mpv', command]
    subprocess.Popen(command, cwd=os.path.expanduser('~/Music'))

if __name__ == '__main__':
# obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

# recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    print('Processing "' + speech + '"...')

# Split speech into segments by space
    speech = speech.split(' ')

    if speech[0] == 'play':
        play(speech[1:])
    else:
        print('Couldn\'t work out what you wanted. Sorry!')
