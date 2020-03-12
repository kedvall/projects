import time

import win32gui

while True:
  window = win32gui.GetForegroundWindow()
  title = win32gui.GetWindowText(window)
  if title == 'Errors occurred':
    control = win32gui.FindWindowEx(window, 0, "static", None)
    print('text: ', win32gui.GetWindowText(control))
  time.sleep(1)