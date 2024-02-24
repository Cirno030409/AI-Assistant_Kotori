from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def main( ):
    devices = AudioUtilities.GetSpeakers()  # スピーカーデバイスの取得
    
    interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)  # 動作中のIFを取得
    volume=interface.QueryInterface(IAudioEndpointVolume)
    print("MuteState %s",volume.GetMute())  # Mute 状態を取得
    volume.SetMute(0,None)                  # Mute解除  
    print("MasterVolume %s",volume.GetMasterVolumeLevel())  # 現在Vol 取得
    print("VolumeRange %s",volume.GetVolumeRange())         # Volのレンジを取得
    volume.SetMasterVolumeLevel(-40,None)                   # MasterVolの設定


if __name__ == '__main__':
    main()