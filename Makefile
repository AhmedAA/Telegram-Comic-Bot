redis:
	-docker stop mjaaadis
	-docker rm mjaaadis
	docker run -th mjaaadis --name mjaaadis -d redis

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

start:
	-docker rm mjaaabot
	docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaadis:redis -it --name mjaaabot python:3 /bin/bash \
	-c "pip install -r requirements.txt; /bin/bash"

run:
	python ./src/main.py ./keys/key.txt ./keys/cv.txt

populate:
	python ./src/populate_redis.py ./src/hero_list.txt ./keys/cv.txt

clean:
	-docker stop mjaaadis
	-docker rm mjaaadis
	-docker rm mjaaabot
