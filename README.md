# hit-and-blow
Hit &amp; Blow(Bulls &amp; Cows) with the theme of playing cards based on Python

배포: pyinstaller --noconsole --onefile --add-data="resource/image/*;resource/image" --add-data="hit_and_blow.ui;." --hidden-import pygame.mixer -i=./icon.ico hit_and_blow.py

GUI 실행: ./dist/hit_and_blow.exe