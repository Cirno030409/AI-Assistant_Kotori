import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=0) as source:
    print('録音中: ')
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language='ja-JP')
    print(text)
except:
    print("録音されていません")