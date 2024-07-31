from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui as pag


def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    cast(interface, POINTER(IAudioEndpointVolume)
         ).SetMasterVolumeLevelScalar(volume_level, None)


input_volume = float(float(input("Enter volume level (1-100): ")) / 100)
set_volume(input_volume - 0.02)

pag.press("volumeup")
