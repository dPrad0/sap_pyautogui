import time
import pyautogui as pyauto
from dev_functions.functions import wait_window
from dev_functions.search import find_png
import pyperclip

def open_transaction(sap_transaccion, sap_nombre_ventana):
# ---------- Entrar a la transaccion
    print('Abriendo transaccion')
    time.sleep(0.5)
    pyauto.hotkey('ctrl', '/')
    pyauto.typewrite('/n ' + sap_transaccion)
    time.sleep(0.5)
    pyauto.hotkey('enter')

    # Esperar a que abra la transaccion
    wait_window(sap_nombre_ventana)
    time.sleep(1)

def call_variante_window():
    time.sleep(1)
    pyauto.hotkey('shift', 'f5')

def sap_wait_window(window):
    wait_window(window)

def call_varainte_shift_f5(sap_variante):
    print(f"Selecting: {sap_variante}")

    time.sleep(1)
    pyauto.hotkey('shift', 'f5')
    wait_window('Buscar variante')
    time.sleep(0.5)

    pyperclip.copy(sap_variante)
    pyauto.hotkey('ctrl', 'v')
    
    pyauto.press('tab', presses=4)
    time.sleep(0.5)
    pyauto.press('delete')
    time.sleep(0.5)
    pyauto.hotkey('f8')
    time.sleep(0.5)
    print(f"Selected: {sap_variante}")

def run_report_f8():
    pyauto.press('f8')

def save_txt_shortcut_alt_l_g_f():
    pyauto.hotkey('alt', 'l', 'g', 'f', interval=0.1)

def save_txt_process():
    wait_window('Grabar lista fichero')
    pyauto.hotkey('enter')
    # Searches for buton crear
    img = 'crear.png'
    find_png(img)

def save_txt_path_file(dirPath, file_name):
    pyperclip.copy(dirPath)
    pyauto.hotkey('shift', 'tab')
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyperclip.copy(file_name)
    pyauto.hotkey('tab')
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 's')

    img = 'sap_green_check.png'
    find_png(img)

    pyauto.click(x=950, y=20)
    pyauto.hotkey('f3')

def save_txt_F9(dirPath, file_name):
    time.sleep(1)
    pyauto.hotkey('f9')
    time.sleep(0.5)
    wait_window('Grabar lista fichero')
    pyauto.hotkey('enter')

    # # Searches for the image
    img = 'crear.png'  
    find_png(img)
    time.sleep(0.5)

    pyauto.hotkey('shift', 'tab')
    pyperclip.copy(dirPath)
    pyauto.hotkey('ctrl', 'v')
    pyauto.hotkey('tab')
    pyperclip.copy(file_name)
    pyauto.hotkey('ctrl', 'v')
    pyauto.hotkey('ctrl', 's')

    img = 'sap_green_check.png'
    find_png(img)
    pyauto.click()
    pyauto.hotkey('F3')

def wait_green_check_and_return():
    img = 'sap_green_check.png'
    find_png(img)
    pyauto.click(x=950, Y=20)
    pyauto.hotkey('f3')

def return_main_sap():
    pyauto.hotkey('ctrl', '/')
    pyauto.write('/n')
    pyauto.hotkey('enter')

def save_txt_ctrl_shift_F9(dirPath, file_name):
    pyauto.hotkey('ctrl','shift','f9')
    time.sleep(0.5)
    wait_window('Grabar lista fichero')
    pyauto.hotkey('enter')

    # # Searches for the image
    img = 'crear.png'
    find_png(img)
    
    time.sleep(0.5)
    pyauto.hotkey('shift', 'tab')
    pyperclip.copy(dirPath)
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyauto.hotkey('tab')
    time.sleep(0.5)
    pyperclip.copy(file_name)
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyauto.hotkey('ctrl', 's')

    # img = 'sap_green_check.png'
    # find_png(img)

    pyauto.click()

    pyauto.hotkey('f3')