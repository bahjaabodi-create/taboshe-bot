import os
import random
from urllib.parse import quote_plus

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
    "Nassif Zeytoun - Kazdou",
    "Amr Diab - Khaleek Maaya",
    "Nancy Ajram - El Hob Zay El Watar",
    "Akhras - Harb",
]

LOVE_REPLIES = [
    "وأنا كمان بحبك يا روحي 😂💕",
    "طبوشة كمان بتحبك 😭💕",
    "بعرف 😌💕 بس لا تتعلق فيني كتير 😂",
    "وأنا شو بدي ساوي بهالحب هاد؟ 😭😂",
]

HATE_REPLIES = [
    "وأنا شو عملتلك؟ 😭😂",
    "لااااا طبوشة حساسة 😭💔",
    "خلص زعلت منك 😤😂",
    "بكرا بترجع بتحبني، بعرفك 😌😂",
]

RELATIONSHIP_ACCEPT = [
    "موافقة 😌💍 بس الشبكة على حسابك 😂",
    "يلا موافقة… بس لا تقول بعدين ما حذرتك 😭😂",
    "تمت الموافقة رسميًا 💍😂 وين بدنا نحتفل؟",
    "موافقة، بس عندي شروط… أولها ما تزعلني 😏😂",
    "خلص ارتبطنا، مبروك إلك ولي 😂❤️",
]

RELATIONSHIP_REJECT = [
    "مرفوض الطلب… حاول مرة ثانية بعد 3-5 أيام عمل 😂",
    "آسفة، قلبي حاليًا خارج نطاق التغطية 📵😂",
    "لااا، خلينا أصدقاء… أصدقاء بعيدين كمان أحسن 😂",
    "رفضت طلب الارتباط، السبب: طبوشة بدها تضل سنغل 😂💔",
    "لا حبيبي/حبيبتي، طبوشة مرتبطة بالنوم حاليًا 😭😂",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 أهلااا! أنا طبوشة 💕\n\n"
        "جربي:\n"
        "• صراحة\n"
        "• جرأة\n"
        "• نرد\n"
        "• أغنية\n"
        "• أغنية + اسم الأغنية\n"
        "• نرتبط\n"
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
        "🎵 أغنية + اسم — البحث عن أغنية\n"
        "💕 بحبك — جربي شو رح جاوبك\n"
        "😂 بكرهك — جربي كمان\n"
        "💍 نرتبط — شو رح يكون جواب طبوشة؟ 😂"
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
    song_name = random.choice(SONGS)
    link = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(song_name)
    )

    await update.message.reply_text(
        f"🎵 طبوشة اختارتلك:\n\n"
        f"🎶 {song_name}\n\n"
        f"{link}"
    )


async def search_song(update: Update, song_name: str):
    link = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(song_name)
    )

    await update.message.reply_text(
        f"🎵 طبوشة عم تدورلك على:\n\n"
        f"🎶 {song_name}\n\n"
        f"{link}"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    # بحبك
    if "بحبك" in text:
        await update.message.reply_text(
            random.choice(LOVE_REPLIES)
        )
        return

    # بكرهك
    if "بكرهك" in text:
        await update.message.reply_text(
            random.choice(HATE_REPLIES)
        )
        return

    # نرتبط
    if "نرتبط" in text:
        if random.choice([True, False]):
            await update.message.reply_text(
                "💍 " + random.choice(RELATIONSHIP_ACCEPT)
            )
        else:
            await update.message.reply_text(
                "💔 " + random.choice(RELATIONSHIP_REJECT)
            )
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

    # إزالة / من بداية الرسالة
    clean = text[1:].strip() if text.startswith("/") else text

    # صراحة
    if clean == "صراحة":
        await truth(update, context)
        return

    # جرأة
    if clean == "جرأة":
        await dare(update, context)
        return

    # نرد
    if clean == "نرد":
        await dice(update, context)
        return

    # أغنية + اسم أغنية
    if clean.startswith("أغنية "):
        song_name = clean.replace("أغنية ", "", 1).strip()

        if song_name:
            await search_song(update, song_name)
            return

    # أغنية فقط
    if clean in ["أغنية", "اغنية", "أغاني", "اغاني"]:
        await song(update, context)
        return

    # مساعدة
    if clean == "مساعدة":
        await help_ar(update, context)
        return


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # كل الرسائل العادية
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    # الأوامر التي تبدأ بـ /
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.COMMAND,
            chat
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
