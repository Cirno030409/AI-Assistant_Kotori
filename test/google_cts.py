import simpleaudio, tempfile, os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ai-assistant-415211-7350a956fc43.json"
client = texttospeech.TextToSpeechClient()
text = "田中さんこんにちは、今日も良い天気ですね。"
synthesis_input = texttospeech.SynthesisInput(text=text)

#声の設定
voice = texttospeech.VoiceSelectionParams(
    name="ja-JP-Wavenet-A",
    language_code="ja-JP",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

#生成する音声ファイルのエンコード方式
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

#音声ファイルを再生
with tempfile.TemporaryDirectory() as tmp:
    with open(f"{tmp}/output.wav", "wb") as f:
        f.write(response.audio_content)
        wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/output.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()