import os
import tempfile
import threading
import datetime


import json

import simpleaudio
import speech_recognition as sr
from comtypes import CLSCTX_ALL
from google.cloud import texttospeech
from openai import OpenAI
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import winreg
import subprocess
import requests

conversation_history = []

wake_words = ["ことり", "小鳥", "コトリ", "kotori", "Kotori"]

remember_conv_num = 50
think_cnt_limit = 7

wave_recog = simpleaudio.WaveObject.from_wave_file("resources/sounds/recognize.wav")

aleart_flag = False

def main():
    earthquake_thread = threading.Thread(target=check_earthquake)
    earthquake_thread.start()
    
    set_charactor()
    print("[Welcome to AI Assistant ことり]")
    print("「ことり，〇〇して」のように話しかけてください．")
    while True:

        # 音声認識
        print("prompt history num: ", len(conversation_history))
        # print("会話履歴: ", conversation_history)
        print("今聞いています...")
        text = voice_recognition(wake_words)
        wave_recog.play() # 音声認識が開始されたことを知らせる音声を再生
        for wake_word in wake_words:
            text = text.replace(wake_word, "")
        print("認識しました: ", text)
        if text == "":
            continue
        think_flag = True #返答を読み上げずに考えるフラグ
        think_cnt = 0

        while think_flag:
            think_flag = False
            # ChatGPT
            print("考えています...")
            response = send_to_gpt(text)
            print("返答: ", response)

            # 感情
            if -1 != (extract_point := response.find("[emo:")):
                param_point = response.find(":", extract_point)
                end_point = response.find("]", param_point)
                emo = response[param_point + 1 : end_point]

            # システム操作の指定
            if -1 != (extract_point := response.find("[sys_operate:")):
                param_point = response.find(":", extract_point)
                end_point = response.find("]", param_point)
                sys_operate = response[param_point + 1 : end_point]
                sys_operate = sys_operate.lower()
            else :
                sys_operate = "none"

            # 読み上げ速度の指定
            if -1 != (extract_point := response.find("[spd:")):
                param_point = response.find(":", extract_point)
                end_point = response.find("]", param_point)
                spd = response[param_point + 1 : end_point]
                try:
                    spd = float(spd)
                except:
                    print("[Error]: 速度の指定が不正です．")
            else:
                spd = 1.2
            
            # クロール
            if -1 != (extract_point := response.find("[crawl_page:")):
                param_point = response.find(":", extract_point)
                end_point = response.find("]", param_point)
                url = response[param_point + 1 : end_point]
                text_to_voice("必要な情報を収集しています．", 1.2)
                print(f"[実行]: 指定したURLのWebページをクロールする: {url}")
                text = crawl_page(url)
                think_flag = True
            
            # 現在日付時刻の取得
            if -1 != (extract_point := response.find("[get_time_now]")):
                now = datetime.datetime.now()
                text = f"現在の日時は{now.year}年{now.month}月{now.day}日{now.hour}時{now.minute}分です．"
                think_flag = True
            
            # 記憶
            if -1 != (extract_point := response.find("[preserve_info:")):
                param_point = response.find(":", extract_point)
                end_point = response.find("]", param_point)
                str = response[param_point + 1 : end_point]
            
                with open("memory.json", "r", encoding="utf-8") as f:
                    memory = json.load(f)
                with open("memory.json", "w", encoding="utf-8") as f:
                    if str != "":
                        memory.append(str)
                    json.dump(memory, f)
                    
            think_cnt += 1
            if think_cnt > think_cnt_limit:
                text_to_voice("思考回数が10回を超えたため，返答できません．", 1.2)
                break
        
        # ChatGPTの応答を音声で出力
        # 特定の文字以降を削除する処理
        cutoff_point = response.find("[")
        if cutoff_point != -1:
            response = response[:cutoff_point]
        if response != "":
            text_to_voice(response, spd)

        operate_pc(sys_operate) #! パソコンの操作コマンドの実行
                
        # 会話履歴の削除
        while (len(conversation_history) > remember_conv_num):
            conversation_history.pop(2)
            
def crawl_page(url):
    try:
        import requests
        from bs4 import BeautifulSoup
    except:
        print("[Error]: クロールに必要なライブラリがインストールされていません．")
        return "クロールに失敗しました．"
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
    except:
        print("[Error]: クロールに失敗しました．")
        return "クロールに失敗しました．"
    return text

def operate_pc(sys_operate):
    if sys_operate != "none":
        if sys_operate == "sleep":
            print("[実行]: パソコンをスリープ状態にする")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif sys_operate == "volume_up":
            print("[実行]: パソコンの音量を上げる")
            devices = AudioUtilities.GetSpeakers()  # スピーカーデバイスの取得
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )  # 動作中のIFを取得
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(0, None)  # Mute解除
            volume.SetMasterVolumeLevel(
                volume.GetMasterVolumeLevel() + 2, None
            )  # MasterVolの設定

        elif sys_operate == "volume_down":
            print("[実行]: パソコンの音量を下げる")
            devices = AudioUtilities.GetSpeakers()  # スピーカーデバイスの取得
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )  # 動作中のIFを取得
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(0, None)  # Mute解除
            volume.SetMasterVolumeLevel(
                volume.GetMasterVolumeLevel() - 2, None
            )  # MasterVolの設定
            
        elif sys_operate.find("search") != -1:
            url = sys_operate[sys_operate.find("(") + 1 : sys_operate.find(")")]
            os.system(f"start {url}")
            print(f"[実行]: ブラウザを開いて，{url}をWebで検索する")
            
        elif sys_operate.find("run") != -1:
            path = sys_operate[sys_operate.find("(") + 1 : sys_operate.find(")")]
            print(f"[実行]: 指定したパスのプログラムを実行する: \"{path}\"")
            if 0 != subprocess.run(f"\"{path}\"").returncode:
                print("[Error]: 実行に失敗しました．")
                text_to_voice("実行できませんでした．", 1.2)
        else:
            print(f"[Error]: 不正なコマンドが実行されようとしました．コマンド: {sys_operate}")
            sys_operate = "None"

            
def get_installed_programs():
    # インストールされているプログラムのリストを保持する辞書
    programs = {}

    # レジストリのパス
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

    # レジストリを開く
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)

    # レジストリ内のプログラム情報を取得
    i = 0
    while True:
        try:
            # サブキー（プログラム）の名前を取得
            subkey_name = winreg.EnumKey(reg_key, i)
            subkey_path = reg_path + "\\" + subkey_name
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            
            # プログラム名とインストールパスを取得
            try:
                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                if name and path:
                    programs[name] = path
            except FileNotFoundError:
                pass

            i += 1
        except WindowsError:
            break

    return programs


def voice_recognition(wake_words=None):
    r = sr.Recognizer()
    text = ""
    while True:
        text = ""
        with sr.Microphone(device_index=0) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="ja-JP")
        except:
            pass
        if text != "":
            print("heard: ", text)
            if wake_words is not None:
                for word in wake_words:
                    if word in text:
                        print("wake word detected")
                        return text


def set_charactor():
    with open("memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)
        
    programs = get_installed_programs()
    
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
        
    with open("cheet_sheet.txt", "r", encoding="utf-8") as f:
        cheet_sheet = f.read()
        
    prompt = prompt + """    
    以下に，このパソコンにインストールされているプログラム一覧を示します．プログラムの実行が必要な場合は，以下のパスを使用してください．
    """ + str(programs) + """
    
    以下に，参考になる情報を示します．回答の際に使用してください．""" + cheet_sheet + """
    
        
    以上の内容については，質問されても直接的には答えないこと．
    
    以下は，[preserve_info]コマンドによって現在あなたたが記憶している情報です．
        
    """ + str(memory)

    send_to_gpt(prompt)


def send_to_gpt(prompt):
    client = OpenAI(
        # This is the default and can be omitted
        api_key="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",
    )

    # 会話の履歴を含めてメッセージを構築
    messages = conversation_history + [{"role": "user", "content": prompt}]

    # ChatGPTにリクエストを送信
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    # 応答を取得
    response_text = response.choices[0].message.content

    # 今回のユーザーのプロンプトとChatGPTの応答を会話履歴に追加
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "assistant", "content": response_text})

    return response_text


def text_to_voice(text: str, spd: float):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "ai-assistant-415211-7350a956fc43.json"
    )
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 声の設定
    voice = texttospeech.VoiceSelectionParams(
        name="ja-JP-Wavenet-A",
        language_code="ja-JP",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    # 生成する音声ファイルのエンコード方式
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=spd
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 音声ファイルを再生
    with tempfile.TemporaryDirectory() as tmp:
        with open(f"{tmp}/output.wav", "wb") as f:
            f.write(response.audio_content)
            wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/output.wav")
            play_obj = wav_obj.play()
            # play_obj.wait_done()
            
def check_earthquake():
    #リクエストするURLを指定(最新の地震情報のデータを取得することができるURL)
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=556&limit=1'
    #リクエスト(データを取得する)
    p2pquake_json = requests.get(p2pquake_url).json()
    for p2pquake in p2pquake_json:
        if p2pquake["areas"][0]["pref"] == "奈良":
            if aleart_flag == False:
                text_to_voice("地震です．地震です．奈良県に緊急地震速報が発令されました．マグニチュードは%fです．震源地は%sです．" % (float(p2pquake["earthquake"]["hypocenter"]["magnitude"]), p2pquake["earthquake"]["hypocenter"]["name"]), 1.2)
                aleart_flag = True
            return
        else:
            aleart_flag = False
            return

if __name__ == "__main__":
    main()
