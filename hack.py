import time
import PySimpleGUI as sg
import pyautogui

layout = [[sg.Text('My one-shot window.')], [sg.Button("Submit"), sg.Button("Cancel")]]      

# window = sg.Window('Window Title', layout)    
# layout = [[sg.Text('My one-shot window.')]]      

window = sg.Window('Bigger Window', layout, size=(400, 200), resizable=True, no_titlebar=False, alpha_channel=0.5)


while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == "Cancel":
        break 
    if event == "Submit": 
        left, top = window.CurrentLocation()
        width = window.size[0]
        height = window.size[1]
        # Take a screenshot of the selected area
        window.Hide()
        time.sleep(0.5) 
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save('/home/arseny/Hack/screenshot.png')
        window.UnHide()
window.close()

# sudo apt-get install tesseract-ocr-all
# import pytesseract
# import shutil
# import os
# import random
# try:
#  from PIL import Image
# except ImportError:
#  import Image

# image_path_in_colab="/content/Screenshot from 2023-01-27 16-53-39.png"
# extractedInformation = pytesseract.image_to_string(Image.open(image_path_in_colab), lang='kor')
# text = extractedInformation
# print(text)

# pip install -U deep-translator
# from deep_translator import GoogleTranslator
# translated = GoogleTranslator(source='auto', target='en').translate(text)  # output -> Weiter so, du bist großartig
# print(translated)
