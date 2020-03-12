@echo off
REM ^ is the little-known BAT file line continuation...

REM Build Data Mapper
pyinstaller --noconfirm ^
			--log-level=WARN ^
			--onefile ^
			--windowed ^
			--name "Excel Data Mapper"^
			--icon="icons\Data Mapper.ico" ^
			"..\Excel Data Mapper\Excel Data Mapper.py"

echo.
echo ################################################
echo #               Data Mapper built              #
echo ################################################
echo.

REM Build Extractor
pyinstaller --noconfirm ^
			--log-level=WARN ^
			--onefile ^
			--windowed ^
			--name "Excel Extractor"^
			--icon="icons\Extractor.ico" ^
			"..\Excel Extractor\Excel Extractor.py"

echo.
echo ################################################
echo #               Extractor built                #
echo ################################################
echo.

REM Build Importer
pyinstaller --noconfirm ^
			--log-level=WARN ^
			--onefile ^
			--windowed ^
			--name "IFS Importer"^
			--icon="icons\Importer.ico" ^
			"..\IFS Importer\IFS Importer.py"

echo.
echo ################################################
echo #               Importer built                 #
echo ################################################
echo.

REM Done!
echo ------------------------------------------------
echo ^|                                              ^|
echo ^| - - -  Finished building all programs  - - - ^|
echo ^|                                              ^|
echo ------------------------------------------------
echo.
pause