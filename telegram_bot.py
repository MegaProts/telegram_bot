from telegram.ext import Updater, CommandHandler
import random
from datetime import datetime
import os
import praw
import requests
from dotenv import load_dotenv
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()

# відкрили порт щоб бот не спав
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')

    def do_HEAD(self):  # 👈 Додай цю частину
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server).start()


# Список передбачень
predictions = [
    "Та їбати його в сраку, буде як буде.",
    "Шось мені нюх каже — буде піздєц, але красивий.",
    "Сиди дома, не позорься, бо знову як тоді буде.",
    "Думаєш все так просто? Нє, братішка.",
    "Та канєшно, тільки без фанатізма.",
    "Єбаш, поки пруха, а там видно буде!",
    "Не сси в труси, всьо буде нормас.",
    "Ну, попробуй, якшо життя надоїло.",
    "Валяй, тільки шоб без істерік потім!",
    "З того щось буде канєшно, але не те, шо ти ждеш.",
    "Да, якшо не спалишся і мєнти не приїдуть.",
    "Хуйова ідея. Але я за.",
    "Йди пий, бо тверезим таке не рішають.",
    "Тобі шо, жити надоїло, чи просто тупо весело?",
    "Є шанс, но малий, як твоя зарплата.",
    "Та пофіг, головне шоб бухло було.",
    "Буде весело. Тобі — не факт.",
    "Тут або пан, або срака!"
]

# Функція-обробник команди /predict
def predict(update, context):
    question = ' '.join(context.args)
    if question:
        answer = random.choice(predictions)
        update.message.reply_text(answer)
    else:
        update.message.reply_text("Напиши питання після команди /predict")

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT")
)

# Функція витягування мемів
def send_reddit_meme(update, context):
    subreddit = reddit.subreddit("memes")
    posts = list(subreddit.hot(limit=50))
    random.shuffle(posts)

    for post in posts:
        if not post.stickied and post.url.endswith(('.jpg', '.jpeg', '.png')):
            update.message.reply_photo(post.url, caption=post.title)
            return

    update.message.reply_text("Не знайшов мемів 😢")

# Функція факт з вікі
def today_event(update, context):
    today = datetime.now()
    url = f"https://uk.wikipedia.org/api/rest_v1/feed/onthisday/events/{today.month}/{today.day}"

    try:
        response = requests.get(url)
        data = response.json()

        if "events" in data and data["events"]:
            event = random.choice(data["events"])
            text = event.get("text", "Сьогодні нічого особливого не сталося.")
            update.message.reply_text(f"📅 {text}")
        else:
            update.message.reply_text("Немає доступних подій на сьогодні.")
    except Exception as e:
        update.message.reply_text("Не вдалося отримати дані з Вікіпедії.")

    

# Основна функція запуску бота
def main():
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("pred", predict))
    dp.add_handler(CommandHandler("meme", send_reddit_meme))
    dp.add_handler(CommandHandler("today", today_event))

    updater.start_polling()
    print("Бот працює...")
    updater.idle()

if __name__ == '__main__':
    main()
