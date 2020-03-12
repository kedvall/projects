#SingleInstance, force
#Persistent

controlID = %clipboard%

ControlGetText, controlText, %controlID%, Inventory Part

clipboard = %controlText%

ExitApp