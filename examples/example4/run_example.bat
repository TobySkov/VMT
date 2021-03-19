@echo off
echo "+++++ Launching main.exe +++++"
..\..\main.exe %~dp0\input.json
echo "+++++ main.exe complete +++++"
timeout 100