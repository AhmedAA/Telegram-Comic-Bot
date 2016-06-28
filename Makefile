containers := `docker ps -aq`

bot:
	docker build -t mjaaa/telebot .
	docker run -v /src --link mjaaadis -it mjaaa/telebot python main.py ../keys/key.txt ../keys/cv.txt "mjaaadis"

redis:
	docker run -th mjaaadis --name mjaaadis -d redis

clean:
	docker exec -it mjaaadis /bin/bash -c 'redis-cli select 0; redis-cli flushdb'

docker-clean:
	docker stop $(containers)
	docker rm $(containers)
