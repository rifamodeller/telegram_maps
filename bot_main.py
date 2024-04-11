# Импортируем необходимые классы.
from geo import load_map, geocode
import logging
import os
import random

import task
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
timer_keyboard = [['30 сек', '60 сек', '5 мин'], ['Назад']]


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(t, update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)

    context.job_queue.run_once(task, int(t), chat_id=chat_id, name=str(chat_id), data=t)
    text = f'Засек {t} с.!'
    if job_removed:
        text += 'Старая задача удалена'
    await update.effective_message.reply_text(text, reply_markup=ReplyKeyboardMarkup(['/close']))


async def task(context):
    t = context.job.data
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {t}c. прошли!')


async def on_start(update: Update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['/dice', '/timer'], ['Назад']])
    await update.message.reply_text(text='Чем могу помочь?', reply_markup=keyboard)


async def on_dice(update: Update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([['6', '6x2', '20'], ['Назад']])
    await update.message.reply_text(text='Хотите кинуть кубик?', reply_markup=keyboard)


async def on_timer(update: Update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup(timer_keyboard)
    await update.message.reply_text(text='Сколько времени засечь?', reply_markup=keyboard)


async def on_close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров!'
    await update.message.reply_text(text, reply_markup=timer_keyboard)


dices = ['⚀', '⚁ ', '⚂ ', '⚃ ', '⚄ ', '⚅']


async def on_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '6':
        await update.message.reply_text(text=random.choice('⚀⚁⚂⚃⚄⚅'))
    elif text == '6x2':
        await update.message.reply_text(text=''.join(random.choices('⚀⚁⚂⚃⚄⚅', k=2)))
    elif text == '20':
        await update.message.reply_text(text=str(random.randint(1, 20)))
    elif text == 'Скрыть':
        await update.message.reply_text('Клавиатура скрыта', reply_markup=ReplyKeyboardMarkup())
    elif text == 'Назад':
        await on_start(update, context)
    elif text == '30 сек':
        await set_timer(30, update, context)
    elif text == '60 сек':
        await set_timer(60, update, context)
    elif text == '5 мин':
        await set_timer(300, update, context)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', on_start))
    application.add_handler(CommandHandler('dice', on_dice))
    application.add_handler(CommandHandler('timer', on_timer))
    application.add_handler(CommandHandler('close', on_close))
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=on_message))

    application.run_polling()


if __name__ == '__main__':
    main()
