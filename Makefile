redis:
	-docker stop mjaaadis
	-docker run --name mjaaadis -d redis
	docker start mjaaadis

mongo:
	-docker stop mjaaango
	-docker run --name mjaaango -d mongo
	docker start mjaaango

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

start:
	-docker stop mjaaabot
	-docker rm mjaaabot
	docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaadis:redis -it --name mjaaabot python:3 /bin/bash \
	-c "pip install -r requirements.txt; /bin/bash"

run:
	python ./src/main.py ./keys/key.txt ./keys/cv.txt

local:
	-docker stop mjaaabot
	-docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaango:mongo -td --name mjaaabot python:3 /bin/bash
	docker start mjaaabot
	docker exec -it mjaaabot bash -c "pip install -r requirements.txt; python ./src/main.py ./keys/key.txt ./keys/cv.txt"

remote:
	-docker stop mjaaabot
	-docker rm mjaaabot
	docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaango:mongo -td --name mjaaabot python:3 /bin/bash -c \
	"pip install -r requirements.txt; python ./src/main.py ./keys/key.txt ./keys/cv.txt"

populate:
	python ./src/populate_redis.py ./src/hero_list.txt ./keys/cv.txt

populate-full:
	python ./src/populate_full.py ./keys/cv.txt

clean:
	-docker stop mjaaango
	-docker stop mjaaadis
	-docker stop mjaaabot
	-docker rm mjaaango
	-docker rm mjaaadis
	-docker rm mjaaabot
