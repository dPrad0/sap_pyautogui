import win32gui                                                                 
import re
import os
import pyautogui
from configparser import ConfigParser
import time
import win32process
import psutil
import win32con

MAIN_HWND = 0 

# PARAMETROS
SAP_title = 'SAP Graphics'
inactive_SAP_window = 'SAP GUI for Windows 760' 
configFilePath = "./config.txt"

# Funcion para listar las ventanas de windows
def find_main_window(starttxt):
    global MAIN_HWND
    win32gui.EnumChildWindows(0, is_win_ok, starttxt) # list the Windows until function 'is_win_ok' is met
    return MAIN_HWND

# Funcion para revisar el titulo de las ventanas de windows
def is_win_ok(hwnd, starttext):
    s = win32gui.GetWindowText(hwnd)
    if s.startswith(starttext):         # if window title starts with "SAP Graphics" end function       
            global MAIN_HWND            # return the window handle hwnd
            MAIN_HWND = hwnd
            return MAIN_HWND
    return 1

# Funcion para buscar ventana de windows por el nombre
def find_window_wildcard(wildcard):
    hwnd = win32gui.EnumWindows(window_enum_callback, wildcard)
    return hwnd

# Funcion para comparar nombre buscado con el nombre de la ventana
def window_enum_callback(hwnd, wildcard):
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        return hwnd

# Funcion para leer el archivo de config.txt
def config_parser():
    config = ConfigParser()
    config.read(configFilePath)
    return config

# Funcion para ejecutar CMD para abrir SAP
def executeSAP():

    # Se debe configurar el archivo config.txt con los parametros de SAP
    config = config_parser()

    # Leer las configuraciones del archivo config.txt
    SAPGuiPath = config.get('connection', 'sapgui')
    system = config.get('connection', 'system')
    language = config.get('connection', 'language')
    client = config.get('connection', 'client')
    
    # Ejecutar CMD para abrir SAP
    os.system('cmd /c "cd "' + SAPGuiPath +
              '" & sapshcut.exe -command="'
              '" -system="' + system +
              '" -wsz=Maximized -language="' + language +
              '" -client="' + client)
    
    print('Opening SAP')

    # Esperar hasta que la ventana de SAP abra para continuar
    sapmainwindowtitle = 'SAP Easy Access'
    listofwindows = pyautogui.getAllTitles()

    while sapmainwindowtitle not in listofwindows:
        listofwindows = pyautogui.getAllTitles()
        time.sleep(1)
        if sapmainwindowtitle in listofwindows:
            print('SAP main window ready')
            break

# Function to list all windows associated with a specific process name
def list_windows_by_process_name(process_name):
    windows = []

    # Enumerate all top-level windows
    def enum_windows_callback(hwnd, lParam):
        # Check if the window is visible and has a title
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)

            # Use win32process.GetWindowThreadProcessId to get the process ID (PID)
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            # Check if the process name of the window matches the specified process name
            if window_title and psutil.Process(pid).name() == process_name:
                windows.append({'hwnd': hwnd, 'title': window_title})

        return True

    win32gui.EnumWindows(enum_windows_callback, None)

    if windows:
        print(f"Windows associated with '{process_name}':")
        for window in windows:
            print(f"HWND: {window['hwnd']} - Title: {window['title']}")
    else:
        print(f"No windows associated with '{process_name}' found.")

    return windows



# Function to maximize and set a window with a specific HWND to the foreground
def maximize_and_set_foreground(hwnd):
    if win32gui.IsWindow(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # Maximize the window
        win32gui.SetForegroundWindow(hwnd)  # Set the window to the foreground
        return True  # Window maximized and set to the foreground
    return False  # Window not found or couldn't be maximized

# Function to restore and set a minimized window with a specific HWND to the foreground
def restore_and_set_foreground(hwnd):
    if win32gui.IsIconic(hwnd):  # Check if the window is minimized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore the window
    win32gui.SetForegroundWindow(hwnd)  # Set the window to the foreground

    return True  # Window restored and set to the foreground




def opensap():
    # Buscar si la ventana 'SAP Graphics' existe
    MAIN_HWND = find_main_window(SAP_title)
    
    # Si la ventana 'SAP Graphics' existe,
    # revisar si la ventana inactiva 'SAP GUI for Windows 760' existe
    if MAIN_HWND:
    
        # Listar todas las ventanas abiertas
        w = pyautogui.getAllTitles()

        # Si la ventana inactiva de 'SAP GUI for Windows 760' existe,
        # cerrarla y volver a abrir SAP
        if inactive_SAP_window in w:
            print('SAP disconnected. Opening SAP again')
            closed_window = find_main_window(inactive_SAP_window)
            win32gui.SetForegroundWindow(closed_window)
            pyautogui.hotkey('right')
            pyautogui.hotkey('enter')

            executeSAP()


    # enfocar la ventana 'SAP Graphics' y alistar el cursor para ingresar transacción
        else:
            # The process name you want to search for (e.g., "saplogon.exe")
            process_name = "saplogon.exe"
            windows_list = list_windows_by_process_name(process_name)

            # Check for "(1)" in the window title and get the hwnd value
            window_found_with_1 = next((window for window in windows_list if "(1)" in window['title']), None)

            if window_found_with_1:
                hwnd_with_1 = window_found_with_1['hwnd']
                print(f"Window with '(1)' in the title found. HWND: {hwnd_with_1}")
                maximize_and_set_foreground(hwnd_with_1)
                
            else:
                print("Window with '(1)' in the title not found. Performing alternative actions.")
                # Your alternative actions when "(1)" is not found
                # Example actions:
                MAIN_HWND = windows_list[0]['hwnd']  # Assuming you want to focus the main window
                win32gui.SetForegroundWindow(MAIN_HWND)
                time.sleep(0.5)
                x, y = pyautogui.size()
                pyautogui.click(x/2, y/2)
                t = chr(47)
                pyautogui.hotkey('ctrl', t)
                print('SAP window is focused')

    # Si la ventana 'SAP Graphics' no existe,
    # abrir SAP
    if MAIN_HWND < 1:
        executeSAP()


opensap()