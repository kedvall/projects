@echo off
REM ^ is the little-known BAT file line continuation...

pyinstaller --noconfirm ^
			--log-level=WARN ^
			--onefile ^
			--windowed ^
			--name "Excel Data Mapper"^
			--icon="Swapper.ico" ^
			"Excel Data Mapper.py"

pause