redis:
	docker run -th mjaaadis --name mjaaadis -d redis

start:
	docker run -w /home/comicbot/telegram -v ~/code/Telegram-Comic-Bot:/home/comicbot/telegram \
	--link mjaaadis:redis -it python:3 /bin/bash \
	-c "pip install -r requirements.txt; /bin/bash"

run:
	python ./src/main.py ./keys/key.txt ./keys/cv.txt

clean:
	docker stop mjaaadis
	docker rm mjaaadis
	docker rm $$(docker ps -aq -f="ancestor=python:3")
