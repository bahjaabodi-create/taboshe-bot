import os
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


TRUTHS = [
    "مين أكتر شخص بالكروب بتثقي فيه؟ 👀",
    "شو أكتر موقف محرج صار معك؟ 😂",
    "مين آخر شخص اشتقتيله؟",
    "شو سر صغير ما بيعرفه عنك أغلب رفقاتك؟ 😉",
    "مين الشخص اللي وجوده بيغير مزاجك فوراً؟",
    "شو أكتر شي بتخافي حدا يعرفه عنك؟ 👀",
]

DARES = [
    "ابعتي آخر صورة عندك بالمعرض 😂",
    "اكتبي أول 3 كلمات إجت ببالك هلق",
    "اعملي منشن لشخص وقولي له كلمة لطيفة 💕",
    "ابعتي رسالة صوتية واحكي أول شي خطر ببالك 😂",
    "قولي مين أكتر شخص بالكروب بيضحكك",
    "اكتبي جملة رومانسية لشخص من اختيارك 😏",
]

SONGS = [
    "🎵 Nassif Zeytoun & Abu Ward - Kazdou\nhttps://www.youtube.com/results?search_query=Nassif+Zeytoun+Kazdou",
    "🎵 Amr Diab - Khaleek Maaya\nhttps://www.youtube.com/results?search_query=Amr+Diab+Khaleek+Maaya",
    "🎵 Nancy Ajram - El Hob Zay El Watar\nhttps://www.youtube.com/results?search_query=Nancy+Ajram+El+Hob+Zay+El+Watar",
    "🎵 Akhras - Harb\nhttps://www.youtube.com/results?search_query=Akhras+Harb",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 أهلااا! أنا طبوشة 💕\n\n"
        "أنا عضوة جديدة بالكروب ومالي دخل بشي 👀😂\n\n"
        "جربي:\n"
        "• صراحة\n"
        "• جرأة\n"
        "• نرد\n"
        "• أغنية\n"
        "• مساعدة\n\n"
        "وكمان فيكي تحكي معي عادي 😈"
    )


async def help_ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😈 أوامر طبوشة:\n\n"
        "🫣 صراحة — سؤال صراحة\n"
        "🔥 جرأة — تحدي جرأة\n"
        "🎲 نرد — رمية نرد\n"
        "🎵 أغنية — أغنية عشوائية\n"
        "💕 بحبك — جربي شو رح جاوبك\n"
        "😂 بكرهك — جربي كمان\n\n"
        "وفيكي تكتبي الأوامر مع أو بدون /"
    )


async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🫣 صراحة:\n\n" + random.choice(TRUTHS)
    )


async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 جرأة:\n\n" + random.choice(DARES)
    )


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)
    await update.message.reply_text(
        f"🎲 طبوشة رمت النرد...\n\n"
        f"وطلع الرقم: {number} 😂"
    )


async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 طبوشة اختارتلك هاي الأغنية:\n\n"
        + random.choice(SONGS)
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    # بحبك
    if "بحبك" in text:
        replies = [
            "وأنا كمان بحبك يا روحي 😂💕",
            "طبوشة كمان بتحبك 😭💕",
            "بعرف 😌💕 بس لا تتعلق فيني كتير 😂",
            "وأنا شو بدي ساوي بهالحب هاد؟ 😭😂",
        ]
        await update.message.reply_text(random.choice(replies))
        return

    # بكرهك
    if "بكرهك" in text:
        replies = [
            "وأنا شو عملتلك؟ 😭😂",
            "لااااا طبوشة حساسة 😭💔",
            "خلص زعلت منك 😤😂",
            "بكرا بترجع بتحبني، بعرفك 😌😂",
        ]
        await update.message.reply_text(random.choice(replies))
        return

    # طبوشة
    if "طبوشة" in text:
        replies = [
            "نعممم؟ 👀😂",
            "عيوني لطبوشة 😌",
            "مين ناداني؟ 😈",
            "سمعت حدا عم يحكي عني؟ 👀😂",
        ]
        await update.message.reply_text(random.choice(replies))
        return

    # الأوامر العربية مع أو بدون /
    clean = text.replace("/", "", 1).strip()

    if clean == "صراحة":
        await truth(update, context)

    elif clean == "جرأة":
        await dare(update, context)

    elif clean == "نرد":
        await dice(update, context)

    elif clean == "أغنية":
        await song(update, context)

    elif clean == "مساعدة":
        await help_ar(update, context)


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    # الأمر الأساسي
    app.add_handler(CommandHandler("start", start))

    # التقاط الكلام العربي
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    # حتى /صراحة و /جرأة وغيرها تشتغل
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^/(صراحة|جرأة|نرد|أغنية|مساعدة)$"
            ),
            chat
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
