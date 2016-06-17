build:
	docker build -t mjaaa/telebot .

run:
	docker run -v /src -ti mjaaa/telebot python telegram-comic-bot/main.py keys/key.txt