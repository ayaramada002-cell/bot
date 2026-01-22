from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. بياناتك
TOKEN = "8595623208:AAFtezYjfTOlpR9eazJIcvSWlwyRcTuilzc"
YOUR_CHAT_ID = 6263200922

async def send_with_menu(update: Update, text: str):
    keyboard = [['/start', 'أرغب في التواصل']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التعديل هنا
    await send_with_menu(update, "البوت شغّال")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # نظام الرد (Reply)
    if update.message.chat_id == YOUR_CHAT_ID and update.message.reply_to_message:
        try:
            original_msg = update.message.reply_to_message.text
            target_user_id = original_msg.split("ID: ")[1].split("\n")[0]
            await context.bot.send_message(chat_id=int(target_user_id), text=user_text)
            await update.message.reply_text("تم إرسال الرد بنجاح ✅")
        except:
            await update.message.reply_text("حدث خطأ في الوصول للمستخدم")
        return

    # الأوامر
    if user_text == "/start":
        # التعديل هنا أيضاً لضمان التطابق
        await send_with_menu(update, "البوت شغّال")
    elif user_text == "أرغب في التواصل":
        await update.message.reply_text("بلغني رسالتك، سِر من إنسان لبوت 🤫")
    else:
        await update.message.reply_text(f"• أهلًا بكَ عزيزي {user_name}، رسالتك وصلت 🚀")
        report = f"رسالة من: {user_name}\nID: {user_id}\n\nالنص: {user_text}"
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=report)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("البوت جاهز للعمل")
    app.run_polling()
