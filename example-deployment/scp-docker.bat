@echo off
set "REMOTE_USER=<username>"
set "REMOTE_HOST=<ip>"
set "REMOTE_PATH=/home/ubuntu"
set "REMOTE_NGINX_PATH=nginx"
set "REMOTE_TLSA_PATH=server/tlsa_server"

call id-setup.bat %REMOTE_USER% %REMOTE_HOST%

REM Use SCP to copy the file
scp -i id_rsa -r docker-compose.yml Dockerfile.server ../server ../requirements.txt %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%
scp -i id_rsa nginx.conf %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/%REMOTE_NGINX_PATH%
scp -i id_rsa postgres_settings.py %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/%REMOTE_TLSA_PATH%
scp -i id_rsa settings.py %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%/%REMOTE_TLSA_PATH%