import os
from os import path
import shutil
import subprocess

main_file_path = path.join(os.getcwd(), "main.py")

if not path.exists("build"):
    os.makedirs("build")

os.chdir(path.join(os.getcwd(), "build"))

# Projektordner erstellen / übeschreiben
if path.exists("WhatsAnalyzer"):
    while True:
        answer = input(
            "Ordner existiert bereits, willst du ihn überschreiben? y/n?: ")
        if answer.lower().strip() == "y":
            shutil.rmtree("WhatsAnalyzer")
            break
        elif answer.lower().strip() == "n":
            exit()
        else:
            print("Eingabe nicht erkannt")

os.makedirs("WhatsAnalyzer")
os.makedirs("WhatsAnalyzer/chats")


with open("WhatsAnalyzer/README.txt", "w") as f:
    f.write("Zum Benutzen musst du einfach deinen exportierten WhatsApp Chat in den 'chats' Ordner einfügen. Dann führst du '_run.bat' aus (meistens mit Doppelklick auf die Datei).")

bat_str = '''
@echo off

set pwd=%~dp0

echo Wie heisst die die Chatdatei, die du analysieren moechtest? Tippe es ein und druecke ENTER.
set /p chatname=:

main.exe %chatname% --project_dir "%pwd%


if exist report.html (
	report.html
)

pause
'''

with open("WhatsAnalyzer/_run.bat", "w") as f:
    f.write(bat_str)

subprocess.call(f'pyinstaller --onefile "{main_file_path}"')
shutil.move("dist/main.exe", "WhatsAnalyzer/main.exe")

shutil.rmtree("dist")
shutil.rmtree("build")
os.remove("main.spec")

if path.exists("WhatsAnalyzer.zip"):
    os.remove("WhatsAnalyzer.zip")

shutil.make_archive("WhatsAnalyzer", "zip", "WhatsAnalyzer")

