@echo off
REM ^ is the little-known BAT file line continuation...

pyinstaller --noconfirm ^
			--log-level=WARN ^
			--onefile ^
			--windowed ^
			--name "Excel Extractor"^
			--icon="Excel Extractor.ico" ^
			ExcelDataScraper.py
pause