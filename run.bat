@echo off
title Smart Fast Runner
cls

:: 1. venv check aur activate
if not exist "venv\" (
    echo [1/4] venv bana raha hoon...
    python -m venv venv
)
call venv\Scripts\activate

:: 2. Check if libraries are already installed
:: Hum check karenge ki kya 'requirements.txt' exist karti hai
if exist "requirements.txt" (
    echo [2/4] Requirements pehle se hain. Seedha run kar raha hoon...
    goto :run_project
)

:: 3. Agar requirements nahi hai, toh hi install karega
echo [2/4] Pehli baar setup ho raha hai. Libraries install kar raha hoon...
pip install pipreqs
pipreqs . --force --ignore venv
pip install -r requirements.txt
pip install "numpy<2" mediapipe==0.10.14 --force-reinstall

:run_project
echo [3/4] Project shuru ho raha hai...
echo ----------------------------------------------------
for %%f in (*.py) do (
    if not "%%f"=="mediapipe.py" (
        python "%%f"
        goto :after_run
    )
)

:after_run
echo ----------------------------------------------------
echo [4/4] Project band ho gaya.
call deactivate
pause