bot:
	docker build -t mjaaa/telebot .
	docker run -v /src -it mjaaa/telebot python main.py ../keys/key.txt ../keys/cv.txt "172.17.0.2"

redis:
	docker-compose up -d