from telegram.ext import Updater, Handler
from config import TG_TOKEN
import data


def send_event(bot, update):
    while len(data.events_stack):
        bot.send_message(chat_id="@instantflats", message=data.events_stack.pop(0))


def main():
    updater = Updater(TG_TOKEN)
    job_queue = updater.job_queue
    job_queue.run_repeating(send_event, interval=60, first=0)
    job_queue.start()


if __name__ == '__main__':
    main()