import ctypes
import threading
import time

def worker(title,close_until_seconds):
    time.sleep(close_until_seconds)
    wd=ctypes.windll.user32.FindWindowW(0,title)
    ctypes.windll.user32.SendMessageW(wd,0x0010,0,0)
    return

def AutoCloseMessageBoxW(text, title, close_until_seconds,window_type):
    t = threading.Thread(target=worker,args=(title,close_until_seconds))
    t.start()
    ctypes.windll.user32.MessageBoxW(0, text, title, window_type)
