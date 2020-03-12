import subprocess

try:
	subprocess.call(['python.exe'])
except FileNotFoundError:
	print('File not found')
