from telegram.ext import Updater, CommandHandler
import random
import os

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
        update.message.reply_text("Напиши питання після команди /pred")

# Основна функція запуску бота
def main():
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("pred", predict))

    updater.start_polling()
    print("Бот працює...")
    updater.idle()

if __name__ == '__main__':
    main()
