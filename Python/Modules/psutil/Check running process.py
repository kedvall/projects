import psutil

PROCNAME = "python.exe"
for proc in psutil.process_iter():
	print(proc.pid)
	#print(proc)

	if proc.name() == PROCNAME:
		print('Already running! Info:')
