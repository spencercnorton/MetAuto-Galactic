@echo off
setlocal EnableDelayedExpansion

REM Define the file types to extract
set "video_ext=mp4 mkv avi mov wmv"

REM Define the root directory
set "root_dir=ENTER_DIRECTORY_HERE"

REM Change to the root directory
cd /d "%root_dir%"

REM Iterate through all folders and subfolders
for /r %%i in (*.rar) do (
    REM Extract files from the RAR archive
    "C:\Program Files\7-Zip\7z.exe" e "%%i" -o"%%~dpi\extracted" -y

    REM Move the extracted video files to the root of the extracted folder
    for %%j in (!video_ext!) do (
        for /r "%%~dpi\extracted" %%k in (*.%%j) do (
            move "%%k" "%%~dpi"
        )
    )

    REM Clean up extracted folder
    rmdir /s /q "%%~dpi\extracted"
)

echo Extraction and moving of video files completed!
pause
