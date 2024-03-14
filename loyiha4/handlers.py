from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

#bot token manzili
bot = AsyncTeleBot("6976819286:AAHThjYAocmGAE8p7tMH1vOFz6ajO4Qqv-4", parse_mode=None)

#start uchun command
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message,'\n'
                 + 'Assalomu alaykum hurmatli, '
                 + message.from_user.full_name
                 + " \n Siz menga o'zbekcha matn yuboring men uni sizga inglizcha tarjima qilib qaytaraman \n Yoki xohlagan tilingizda matn yuboring uni o'zbekchaga tarjima qilib sizga yuboraman "
                 +'\n')

#help uchun command
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message,' ↓ ↓ ↓\n'
                 + 'Menga text yuboring\n'
                 + "Siz yuborgan text qaysi tilda ekanligi aniqlayman va o'zbekchaga tarjima qilib sizga yuboraman\n"
                 + "Yoki o'zbekcha matn yuborsangiz uni inglizcha qilib sizga tarjima qilib beraman\n"
                 +'\n')

#tilni aniqlash va uni tarjima qilish
@bot.message_handler()
async def user_text(message):
    translator = Translator()

    #matn tilini aniqlash
    lang = translator.detect(message.text)
    lang = lang.lang

    # boshqa tillarni ham qo'shib yozsa bo'ladi dest='kerakli til'
    if lang == 'uz':
        send = translator.translate(message.text)
        await bot.reply_to(message, '\n'+ send.text +'\n ')

    else:
        send = translator.translate(message.text, dest='uz')
        await bot.reply_to(message, '\n'+ send.text +'\n')

#inline so'rovlar uchun command
@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    # Agar bo'sh matn kelsa, tarjima qilinmaydi ↓
    if not text:
        return f"Siz bo'sh matn yubordingiz"

    #Tilni aniqlash uchun ↓
    lang = translator.detect(text)
    lang = lang.lang

    if lang == 'uz':
        send = translator.translate(text)
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))
    else:
        send = translator.translate(text, dest='uz')
        results.append(types.InlineQueryResultArticle(
            id='1', title=send.text, input_message_content=types.InputTextMessageContent(
                message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Обработка картинок с подписями
# @bot.message_handler(content_types=['photo'])
# async def handle_image(message):
#     translator = Translator()
#     #Обработчик сообщений с изображениями
#     chat_id = message.chat.id
#     photo = message.photo[-1].file_id
#     caption = message.caption

#     # Определение языка ввода.
#     lang = translator.detect(caption)
#     lang = lang.lang

#     # Если подпись по русски, то перевести на английский по умолчанию.
#     if lang == 'uz':
#         send = translator.translate(caption)

#     # Иначе другой язык перевести на русский {dest='ru'}.
#     else:
#         send = translator.translate(caption, dest='uz')
#     await bot.send_photo(chat_id, photo, caption=send.text)

asyncio.run(bot.infinity_polling())