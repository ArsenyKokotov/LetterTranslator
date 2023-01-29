import time
import PySimpleGUI as sg
import pyautogui
import pytesseract
try:
 from PIL import Image
except ImportError:
 import Image
from deep_translator import GoogleTranslator

LANG_ORG_pytesseract = ''
LANG_ORG_deep_translator = ''
LANG_DEST = ''

languages_origin = ['english', 'korean', 'chinese (simplified)', 'japanese']
languages_destination = ['english', 'korean', 'chinese (simplified)', 'japanese', 'russian']

translator = GoogleTranslator()

def format_lang(origin, dest):
    global LANG_ORG_pytesseract
    global LANG_ORG_deep_translator
    global LANG_DEST
    
    if origin == 'english':
        LANG_ORG_pytesseract = 'eng'
    elif origin == 'korean':
        LANG_ORG_pytesseract = 'kor'
    elif origin == 'chinese (simplified)':
        LANG_ORG_pytesseract ='chi_sim'
    elif origin == 'japanese':
        LANG_ORG_pytesseract = 'jpn'
    # find abbreviations in here https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    
    LANG_DEST = GoogleTranslator.get_supported_languages(translator, True)[dest]
    LANG_ORG_deep_translator = GoogleTranslator.get_supported_languages(translator, True)[origin]

def create_screenshot_window(old_window):
    old_window.close()
    layout = [[sg.Text('', size=(2,1)), sg.Text('Overlay the transparent blue area and take a screenshot', background_color='red')], 
              [[sg.Text('', size=(15,1)), sg.Text('and take a screenshot', background_color='red')]], 
              [sg.Text('', size=(1,5)), sg.Button("Submit"), sg.Text('', size=(25,1)), sg.Button("Cancel"),sg.Text('', size=(1,5))],
              [sg.Text('', size=(0,5))]]

    window = sg.Window('Screenshot', layout, size=(400, 200), resizable=True, no_titlebar=False, alpha_channel=0.5)


    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            create_menu(window)
            break
        if event == "Cancel":
            create_menu(window)
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
            translation()
            # window.UnHide()
            break
    window.close()

def create_menu(screenshot=1):
    if screenshot!=1:
        screenshot.close()
    layout = [[sg.Text('Pick a language and take a screenshot.')],
              [sg.Combo(values=languages_origin, key='lang_origin', readonly=True, default_value=languages_origin[0]), sg.Text('Language you want to translate')], 
              [sg.Combo(values=languages_destination, key='lang_dest', readonly=True, default_value=languages_origin[0]), sg.Text('Language you want to translate to')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Button("Screenshot"), sg.Text('', size=(25,1)), sg.Button("Cancel")]]           
    window = sg.Window('Main Menu', layout, size=(400, 200), resizable=True, no_titlebar=False)


    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == "Cancel":
            break 
        if event == "Screenshot": 
            if values['lang_origin']=='' or values['lang_dest']=='':
                continue
            format_lang(values['lang_origin'],values['lang_dest'])
            create_screenshot_window(window)
    window.close()

def translation():
    image_path_in_colab="screenshot.png"
    extractedInformation = pytesseract.image_to_string(Image.open(image_path_in_colab), lang=LANG_ORG_pytesseract)
    translated = GoogleTranslator(source=LANG_ORG_deep_translator, target=LANG_DEST).translate(extractedInformation)
    layout = [[sg.Text('Original Text:')],
              [sg.Multiline(extractedInformation, size=(100,3))],
              [sg.Text('Translation')],
              [sg.Multiline(translated, size=(100,3))],
              [sg.Button("Cancel")]]           
    window = sg.Window('Main Menu', layout, size=(400, 200), resizable=True, no_titlebar=False)


    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            create_screenshot_window(window)
            break
        if event == "Cancel":
            create_screenshot_window(window)
            break 
    window.close()

create_menu()



# print(GoogleTranslator.get_supported_languages(translator, True))
