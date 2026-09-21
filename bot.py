import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TRUTHS = [
    "مين أكتر شخص بالكروب بتثقي فيه؟ 👀",
    "شو أكتر موقف محرج صار معك؟ 😂",
    "مين آخر شخص اشتقتيله؟",
    "شو سر صغير ما بيعرفه عنك أغلب رفقاتك؟ 😏",
]

DARES = [
    "ابعتي آخر صورة عندك بالمعرض 😂",
    "اكتبي أول 3 كلمات إجت ببالك هلق.",
    "اعملي منشن لشخص وقولي له كلمة لطيفة ❤️",
    "ابعتي رسالة صوتية وقولي أول جملة بتختارها طبوشة 😂",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلااا 😂 أنا طبوشة!\n"
        "أنا عضوة جديدة بالكروب 😈\n\n"
        "جربي /truth أو /dare أو /dice"
    )

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎤 صراحة:\n" + random.choice(TRUTHS)
    )

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 تحدي:\n" + random.choice(DARES)
    )

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎲 طلع الرقم: {random.randint(1, 6)}"
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "طبوشة" in text or "@taboshebot" in text:
        replies = [
            "شو بدكن مني؟ 😂",
            "أنا هون 👀",
            "مين ناداني؟ 😈",
            "كمّلوا الحكي، أنا عم اسمع 🍿😂",
            "طبوشة وصلت 😌",
        ]
        await update.message.reply_text(random.choice(replies))

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("truth", truth))
    app.add_handler(CommandHandler("dare", dare))
    app.add_handler(CommandHandler("dice", dice))

    from telegram.ext import MessageHandler, filters
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
