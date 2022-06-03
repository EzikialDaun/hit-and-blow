# hit-and-blow
Hit &amp; Blow(Bulls &amp; Cows) with the theme of playing cards based on Python

배포 시 아나콘다 프롬프트에서 cd를 통해 hit_and_blow.py와 같은 디렉토리로 이동
배포 명령어: pyinstaller --noconsole --onefile --add-data="resource/image/*;resource/image" --add-data="hit_and_blow.ui;." --hidden-import pygame.mixer -i=./icon.ico hit_and_blow.py

GUI 실행: ./dist/hit_and_blow.exe