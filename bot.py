import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Oylar nomlari
MONTHS = {
    'uz': {
        1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel",
        5: "May", 6: "Iyun", 7: "Iyul", 8: "Avgust",
        9: "Sentabr", 10: "Oktabr", 11: "Noyabr", 12: "Dekabr"
    },
    'ru': {
        1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля",
        5: "Мая", 6: "Июня", 7: "Июля", 8: "Августа",
        9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"
    },
    'en': {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
}

# Til tarjimalari
TRANSLATIONS = {
    'uz': {
        'welcome': "Assalomu alaykum! Men sizning tug'ilgan kuningizni fokus orqali topib beraman!",
        'select_language': "Iltimos, tilni tanlang:",
        'step1': "1️⃣ Tug'ilgan kuningiz raqamini (1-31) 5 ga ko'paytiring",
        'step2': "2️⃣ Natijaga 6 qo'shing",
        'step3': "3️⃣ Natijani 4 ga ko'paytiring",
        'step4': "4️⃣ Natijaga 9 qo'shing",
        'step5': "5️⃣ Natijani 5 ga ko'paytiring",
        'step6': "6️⃣ Natijaga tug'ilgan oyingiz raqamini (1-12) qo'shing",
        'step7': "7️⃣ Natijadan 165 ni ayiring",
        'done': "✅ Bajardim!",
        'ask_result': "🟢 Endi chiqqan yakuniy sonni menga yuboring!",
        'result': "🎉 Ajoyib! Sizning tug'ilgan kuningiz {day}-{month}!",
        'error': "❌ Iltimos, faqat raqam kiriting!",
        'error_invalid': "❌ Noto'g'ri natija! Iltimos, qaytadan hisoblang.",
        'start_over': "Qayta boshlash uchun /start bosing"
    },
    'ru': {
        'welcome': "Здравствуйте! Я помогу найти вашу дату рождения с помощью фокуса!",
        'select_language': "Пожалуйста, выберите язык:",
        'step1': "1️⃣ Умножьте число рождения (1-31) на 5",
        'step2': "2️⃣ Прибавьте 6",
        'step3': "3️⃣ Умножьте на 4",
        'step4': "4️⃣ Прибавьте 9",
        'step5': "5️⃣ Умножьте на 5",
        'step6': "6️⃣ Прибавьте номер месяца рождения (1-12)",
        'step7': "7️⃣ Вычтите 165",
        'done': "✅ Готово!",
        'ask_result': "🟢 Теперь отправьте мне полученное число!",
        'result': "🎉 Отлично! Ваш день рождения {day} {month}!",
        'error': "❌ Пожалуйста, введите только число!",
        'error_invalid': "❌ Неверный результат! Пожалуйста, пересчитайте.",
        'start_over': "Для перезапуска нажмите /start"
    },
    'en': {
        'welcome': "Hello! I will find your birthday using a trick!",
        'select_language': "Please choose a language:",
        'step1': "1️⃣ Multiply your birth day (1-31) by 5",
        'step2': "2️⃣ Add 6",
        'step3': "3️⃣ Multiply by 4",
        'step4': "4️⃣ Add 9",
        'step5': "5️⃣ Multiply by 5",
        'step6': "6️⃣ Add your birth month (1-12)",
        'step7': "7️⃣ Subtract 165",
        'done': "✅ Done!",
        'ask_result': "🟢 Now send me the final number!",
        'result': "🎉 Great! Your birthday is {month} {day}!",
        'error': "❌ Please enter only numbers!",
        'error_invalid': "❌ Invalid result! Please recalculate.",
        'start_over': "Press /start to restart"
    }
}

# Foydalanuvchi holatlarini saqlash
user_states = {}

# "Bajardim" tugmasi
def get_done_button(lang):
    keyboard = [[KeyboardButton(TRANSLATIONS[lang]['done'])]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start komandasi - til tanlash"""
    keyboard = [
        [
            InlineKeyboardButton("O'zbek", callback_data='lang_uz'),
            InlineKeyboardButton("Русский", callback_data='lang_ru'),
            InlineKeyboardButton("English", callback_data='lang_en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Добро пожаловать! Пожалуйста, выберите язык:\n\n"
        "👋 Welcome! Please choose a language:\n\n"
        "👋 Assalomu alaykum! Iltimos, tilni tanlang:",
        reply_markup=reply_markup
    )

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Til tanlash"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    user_id = query.from_user.id
    
    # Holatni saqlash
    user_states[user_id] = {
        'lang': lang,
        'step': 1,  # 1 dan 7 gacha
        'day': None,
        'month': None
    }
    
    await query.edit_message_text(
        f"✅ {TRANSLATIONS[lang]['welcome']}\n\n"
        f"{TRANSLATIONS[lang]['step1']}\n\n"
        f"⬇️ Amalni bajargandan so'ng quyidagi tugmani bosing:"
    )
    
    # "Bajardim" tugmasini ko'rsatish
    await query.message.reply_text(
        "✅",
        reply_markup=get_done_button(lang)
    )

def calculate_birthday(final_result):
    """
    Formula: ((day * 5 + 6) * 4 + 9) * 5 + month - 165 = final_result
    
    final_result dan day va month ni topish:
    final_result = day * 100 + month
    
    Demak:
    day = final_result // 100
    month = final_result % 100
    """
    day = final_result // 100
    month = final_result % 100
    
    # Tekshirish: day 1-31 oralig'ida va month 1-12 oralig'ida bo'lishi kerak
    if 1 <= day <= 31 and 1 <= month <= 12:
        return day, month
    else:
        return None, None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi xabarlarini qayta ishlash"""
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_states:
        await start(update, context)
        return
    
    state = user_states[user_id]
    lang = state['lang']
    
    # Agar "Bajardim" tugmasi bosilgan bo'lsa
    if text == TRANSLATIONS[lang]['done']:
        step = state['step']
        
        if step == 1:
            await update.message.reply_text(TRANSLATIONS[lang]['step2'])
            state['step'] = 2
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 2:
            await update.message.reply_text(TRANSLATIONS[lang]['step3'])
            state['step'] = 3
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 3:
            await update.message.reply_text(TRANSLATIONS[lang]['step4'])
            state['step'] = 4
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 4:
            await update.message.reply_text(TRANSLATIONS[lang]['step5'])
            state['step'] = 5
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 5:
            await update.message.reply_text(TRANSLATIONS[lang]['step6'])
            state['step'] = 6
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 6:
            await update.message.reply_text(TRANSLATIONS[lang]['step7'])
            state['step'] = 7
            await update.message.reply_text("✅", reply_markup=get_done_button(lang))
            
        elif step == 7:
            # Foydalanuvchidan yakuniy natijani so'rash
            await update.message.reply_text(
                TRANSLATIONS[lang]['ask_result'],
                reply_markup=None  # Tugmani olib tashlash
            )
            state['step'] = 'final'
    
    # Yakuniy natija kiritilganda
    elif state['step'] == 'final':
        try:
            final_result = int(text)
            
            # Tug'ilgan kun va oyni hisoblash
            day, month = calculate_birthday(final_result)
            
            if day and month:
                # Oy nomini olish
                month_name = MONTHS[lang].get(month, month)
                
                # Natija xabari
                if lang == 'uz':
                    result_text = TRANSLATIONS[lang]['result'].format(day=day, month=month_name)
                elif lang == 'ru':
                    result_text = TRANSLATIONS[lang]['result'].format(day=day, month=month_name)
                else:  # en
                    result_text = TRANSLATIONS[lang]['result'].format(month=month_name, day=day)
                
                await update.message.reply_text(
                    f"{result_text}\n\n"
                    f"📊 Sizning natijangiz: {final_result}\n"
                    f"📅 {day:02d}.{month:02d}\n\n"
                    f"{TRANSLATIONS[lang]['start_over']}",
                    reply_markup=None
                )
                
                # Holatni tozalash
                del user_states[user_id]
            else:
                await update.message.reply_text(
                    f"{TRANSLATIONS[lang]['error_invalid']}\n\n"
                    f"{TRANSLATIONS[lang]['start_over']}",
                    reply_markup=None
                )
                del user_states[user_id]
            
        except ValueError:
            await update.message.reply_text(
                f"{TRANSLATIONS[lang]['error']}\n\n"
                f"{TRANSLATIONS[lang]['start_over']}",
                reply_markup=None
            )
    
    else:
        # Noto'g'ri xabar
        await update.message.reply_text(
            f"⚠️ Iltimos, 'Bajardim ✅' tugmasini bosing!\n\n"
            f"{TRANSLATIONS[lang]['start_over']}",
            reply_markup=None
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bekor qilish"""
    user_id = update.message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    await update.message.reply_text(
        "❌ Amaliyot bekor qilindi.\n"
        "❌ Операция отменена.\n"
        "❌ Operation cancelled.\n\n"
        "Qayta boshlash uchun /start bosing.",
        reply_markup=None
    )

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN topilmadi!")
        return
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()