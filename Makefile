setup-no-virtuel:
	pip install -r requirements.txt
	mongod --config mongod.conf --fork --logpath ./log/mongodb.log
	
mongo:
	-docker stop mjaaango
	-docker run --name mjaaango -d mongo
	docker start mjaaango

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

populate:
	-docker stop mjaaabot
	-docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaango:mongo -td --name mjaaabot python:3 /bin/bash
	docker start mjaaabot
	docker exec -it mjaaabot bash -c "pip install -r requirements.txt; python ./src/populate_full.py ./keys/cv.txt"

local:
	-docker stop mjaaabot
	-docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaango:mongo -td --name mjaaabot python:3 /bin/bash
	docker start mjaaabot
	docker exec -it mjaaabot bash -c "pip install -r requirements.txt; python ./src/telegram.py ./keys/key.txt ./keys/cv.txt"

remote:
	-docker stop mjaaabot
	-docker rm mjaaabot
	docker run -w /home/comicbot/telegram -v $(ROOT_DIR):/home/comicbot/telegram \
	--link mjaaango:mongo -td --name mjaaabot python:3 /bin/bash -c \
	"pip install -r requirements.txt; python ./src/telegram.py ./keys/key.txt ./keys/cv.txt"

clean:
	-docker stop mjaaango
	-docker stop mjaaabot
	-docker rm mjaaango
	-docker rm mjaaabot
