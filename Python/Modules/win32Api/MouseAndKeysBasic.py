import win32api
import win32con
win32api.keybd_event(win32con.VK_F3, 0) # this will press F3 key

win32api.GetFocus() # this will return you the handle of the window which has focus

win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0) # this will press mouse left button
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTTUP, 0, 0) # this will raise mouse left button
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0) # this will press mouse right button
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0) # this will raise mouse right button