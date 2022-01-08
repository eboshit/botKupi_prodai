from flask import Flask, request
import telebot
import time

bot = telebot.TeleBot('2016332955:AAHhOGR8ZqIP1xseAg6lp9YOe8XkB4Iu5s4')
bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://1ce8-109-252-87-170.ngrok.io")
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok", 200


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    #app.run()














