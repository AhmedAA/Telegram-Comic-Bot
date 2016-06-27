bot:
	docker build -t mjaaa/telebot .
	docker run -v /src -it mjaaa/telebot python main.py ../keys/key.txt ../keys/cv.txt "172.17.0.2"

redis:
	docker-compose up -d

clean:
	docker exec -it telegramcomicbot_redis_1 /bin/bash -c 'redis-cli select 0; redis-cli flushdb'
