import pyautogui, time

time.sleep(5)
pyautogui.click() # Click to put the program into focus
distance = 300
while distance > 0:
	pyautogui.dragRel(distance, 0, duration=0) # Move right
	distance = distance - 5
	pyautogui.dragRel(0, distance, duration=0) # Move down
	pyautogui.dragRel(-distance, 0, duration=0) # Move left
	distance = distance - 5
	pyautogui.dragRel(0, -distance, duration=0) # Move up