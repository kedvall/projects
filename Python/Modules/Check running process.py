import psutil

PROCNAME = "python.exe"
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        print('Already running! Info:')
        print(proc)