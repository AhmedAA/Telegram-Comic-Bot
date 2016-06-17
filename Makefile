build:
	docker build -t telebot .

run:
	docker run -i -t telebot python /home/docker-py/telegram-comic-bot/main.py /home/docker-py/keys/key.txt