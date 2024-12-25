@echo off
setlocal

REM Assign arguments
set USER=%1
set IP=%2

REM Define the path to the SSH key
set SSH_KEY=%~dp0id_rsa

REM Check if the SSH key already exists
if exist "%SSH_KEY%" (
    echo SSH key already exists. Skipping key generation.
) else (
    echo Generating SSH key in the current directory...
    ssh-keygen -t rsa -b 4096 -f "%SSH_KEY%"

    echo Copying SSH key to %USER%@%IP%...
    scp "./id_rsa.pub" "%USER%@%IP%:~/.ssh/authorized_keys"

    echo Setup complete.
)

endlocal