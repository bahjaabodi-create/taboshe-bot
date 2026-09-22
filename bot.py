import os
import random
import json
import urllib.parse
import urllib.request

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
    "هل في شخص لسا بتحبيه رغم كل شي؟",
    "مين أول شخص بتفكري فيه لما تزعلي؟",
    "شو أكتر صفة بتحبيها بحالك؟",
    "شو أكتر صفة بتكرهيها بحالك؟",
    "هل سبق وحبيتي شخص وما عرف؟",
    "شو أكتر موقف خلاكي تبكي بسبب شخص؟",
    "مين الشخص اللي مستحيل تنسيه؟",
    "هل بتسامحي بسهولة ولا لأ؟",
    "شو أكتر شي بيجذبك بالشخص؟",
    "هل سبق وكذبتي لتحمي شخص بتحبيه؟",
    "شو أكبر سر مخبيتيه عن أصحابك؟ 👀",
    "مين الشخص اللي بتشتاقيله وما بتقولي؟",
    "هل بتؤمني بالحب من أول نظرة؟",
    "شو أكتر كلمة ممكن تكسرك؟",
    "هل في شخص نفسك تحكي معه هلق؟",
    "شو أكتر موقف ندمتي عليه؟",
    "مين أكتر شخص بيعرف أسرارك؟",
    "لو فيكي ترجعي بالزمن، شو الشي اللي بتغيريه؟",
    "هل سبق وحبيتي شخص ما كان مناسب إلك؟",
    "شو أكتر شي بيخليكي تغاري؟",
    "هل بتفضلي الحب ولا الاستقرار؟",
    "شو أكتر رسالة نفسك توصلك هلق؟",
    "مين الشخص اللي وجوده بحياتك نعمة؟ ❤️",
]

DARES = [
    "ابعتي آخر صورة عندك بالمعرض 😂",
    "اكتبي أول 3 كلمات إجوا ببالك هلق.",
    "اعملي منشن لشخص وقولي له كلمة لطيفة 💕",
    "ابعتي رسالة صوتية واحكي أول شي خطر ببالك 😂",
    "قولي مين أكتر شخص بالكروب بيضحكك.",
    "اكتبي جملة رومانسية لشخص من اختيارك 😏",
    "اعملي منشن لشخص وقلّيله اشتقتلك 😂",
    "اكتبي اسم الشخص اللي مستحيل ترفضي له طلب.",
    "قولي آخر شخص فتحتي معه محادثة.",
    "ابعتي إيموجي بيعبر عن حالتك العاطفية هلق.",
    "اكتبي أول حرف من اسم الشخص اللي ببالك 👀",
    "قولي أكتر شخص بالكروب بتتوقعي يكون رومانسي.",
    "اكتبي جملة غزل بدون ما تذكري اسم الشخص.",
    "ابعتي 5 قلوب من اختيارك ❤️😂",
    "قولي شو أول شي بتعمليه لما تشتاقي لحدا.",
    "اعملي منشن لشخص وخليه يختارلك سؤال.",
    "اكتبي اعتراف صغير بدون أسماء 👀",
    "قولي مين أكتر شخص بتتخانقي معه.",
    "اكتبي كلمة بتحبي تسمعيها من شخص بتحبيه.",
    "اختاري شخص بالكروب وقولي شو أكتر صفة حلوة فيه.",
]

KAT_QUESTIONS = [
    "مين أول شخص خطر ببالك لما قلتي حب؟ ❤️",
    "شو أكتر شي ممكن يخلي قلبك يدق بسرعة؟",
    "هل بتقعي بالحب بسرعة ولا بدك وقت؟",
    "شو أكتر حركة رومانسية ممكن تذوبك؟",
    "هل بتحبي الغيرة بالعلاقة؟ 👀",
    "شو أكتر كلمة رومانسية بتحبي تسمعيها؟",
    "لو الشخص اللي بتحبيه قدامك هلق، شو أول شي بتقولي له؟",
    "شو بالنسبة إلك معنى الحب الحقيقي؟",
    "هل بتفضلي الحضن ولا الكلام الحلو؟",
    "شو أكتر تفصيل صغير ممكن يخليكي تتعلقي بشخص؟",
    "هل ممكن تحبي شخص بعيد عنك؟",
    "شو أكتر شي ممكن يقتل الحب بالنسبة إلك؟",
    "بتفضلي شخص رومانسي ولا شخص بيضحكك؟",
    "شو أجمل ذكرى رومانسية عندك؟",
    "هل ممكن ترجعي لشخص قديم بتحبيه؟",
    "شو أكتر شي بيخليكي تحسي بالأمان مع شخص؟",
    "لو عندك يوم كامل مع الشخص اللي بتحبيه، كيف بتقضوه؟",
    "شو أكتر نوع رسائل بتحبي توصلك؟",
    "هل بتفضلي الحب السري ولا العلاقة المعلنة؟",
    "شو أكتر شي ممكن يخليكي تشتاقي لشخص؟",
    "مين الشخص اللي بتتمني يكون جنبك هلق؟ 👀",
    "هل ممكن تسامحي خيانة عاطفية؟",
    "شو أكتر صفة لازم تكون موجودة بالشخص اللي بتحبيه؟",
    "هل بتؤمني إن شخص واحد ممكن يضل بقلبك طول العمر؟",
    "لو الحب كان أغنية، شو بتكون أغنيتك؟ 🎵",
]

GREETING_REPLIES = [
    "مراحب 😌❤️",
    "يا مرحبااا 🌷",
    "أهلااا وسهلااا 😍",
    "يا هلا ويا غلا 😂❤️",
    "صباح الخيرات 🌞❤️",
    "مساء الخيرات 🌙✨",
    "أهلا بالناس الحلوة 😌",
    "هلا هلااا 😭❤️",
    "منورين يا جماعة 🌷",
    "أهلاً وسهلاً بالزين كله 😂",
    "يا صباح الورد 🌹",
    "مساء الورد والياسمين 🌙🌹",
    "هلا باللي جانا 😌",
]

LOVE_REPLIES = [
    "وأنا كمان بحبك يا روحي 😂❤️",
    "بعرف 😌 بس لا تتعلق فيني كتير 😂",
    "طبوشة كمان بتحبك 😭❤️",
    "وأنا شو بدي ساوي بهالحب هاد؟ 😭😂",
    "خلص فضحتني قدام الكروب 😂❤️",
    "يا لطيف! هيك دغري؟ 😭😂",
    "وأنا كنت ناطرة منك هالكلمة 👀❤️",
    "حبيتك من هالكلمة 😂❤️",
    "تعال هون خليني صدقك أول 😂",
]

HATE_REPLIES = [
    "وأنا شو عملتلك؟ 😭😂",
    "لااااا طبوشة حساسة 😭",
    "خلص زعلت منك 😤😂",
    "بكرا بترجع بتحبني، بعرفك 😌😂",
    "مرفوضة هاي الكلمة 😂",
    "روح راجع حالك وبعدين تعال 😭😂",
    "معقول بعد كل هالحب؟ 😭",
    "طيب زعلت… بس شوي 😂",
    "حاضر يا عدو طبوشة الرسمي 😂",
]

RELATIONSHIP_REPLIES = [
    "موافقة 😌💍 بس الشبكة على حسابك 😂",
    "يلا موافقة… بس لا تقول بعدين ما حذرتك 😭😂",
    "تمت الموافقة رسميًا 💍😂 وين بدنا نحتفل؟",
    "موافقة، بس عندي شروط… أولها ما تزعلني 😏",
    "خلص ارتبطنا، مبروك إلك ولي 😂❤️",
    "طلبك قيد الدراسة من لجنة طبوشة 😂",
    "ممكن… بس بدك تثبت إنك بتستاهل 😌",
    "ارتباط؟ بهالسرعة؟ 😭😂",
    "حط طلبك بالدور، في ناس قبلك 😂",
    "موافقة مبدئية… والباقي حسب التصرفات 👀😂",
    "لا تستعجل، خلينا نتعرف أول 😂❤️",
    "تم قبول الطلب… مؤقتاً 😌💍",
]

KISS_REPLIES = [
    "😘😘😘😘😘",
    "مـــــوااااااااح 💋😂",
    "بوسة على راسك 😘",
    "موووووواححححححح 😭💋",
    "😘💋😘💋😘",
    "تعال خد هالبوسة 😘",
    "بوسة محترمة وبس 😂💋",
    "موااااااح من هون لبكرا 💋😂",
    "بوسة + حضن كمان 😭❤️",
    "💋💋💋💋💋💋",
]

INSULT_REPLIES = [
    "عيببب 😂",
    "بلا تربية 😭😂",
    "وين التربية والأخلاق؟ 😂",
    "احترم حالك يا قليل الأدب 😭",
    "طبوشة سمعت كل شي 👀😂",
    "استغفر ربك وروق 😂",
    "شو هالحكي؟ عيب 😭",
    "الله يهديك بس 😂",
    "هيك قدام العالم؟ 😭",
]

WHERE_REPLIES = [
    "بقلبك ❤️",
    "هون… بس مخبية 👀",
    "جنبك بس إنت ما بتشوفني 😂",
    "ببالك يا حلو 😌",
    "موجودة، وين بدي روح؟ 😂",
    "بقلبك… فتش منيح ❤️",
]

BYE_REPLIES = [
    "بالناقص وارتحنا 😂",
    "مع السلامة… لا تطول الغيبة 😌😂",
    "يلا باي، الكروب رح يرتاح شوي 😂",
    "باي؟ أخيراً 😂",
    "روح روح، الله معك 😂",
    "بالناقص يا عيوني 😭😂",
    "مع السلامة، الباب وراك 😂",
    "خلص خلص، لا ترجع بسرعة 😂",
    "باي… واعتبرها إجازة إجبارية 😂",
]

ISTAGHFAR_REPLIES = [
    "هي اصطخفر الله 😭😂",
    "اصطخفر الله العظيم 😂",
    "طبوشة استغفرت معك 😭",
    "الله يغفرلنا جميعاً 😂❤️",
    "استغفر الله يا جماعة 😭😂",
]

SONGS = [
    "piano",
    "romantic music",
    "love music",
    "happy music",
    "sad music",
    "lofi",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 أهلااا! أنا طبوشة 💕\n\n"
        "جربي:\n"
        "• صراحة\n"
        "• جرأة\n"
        "• كت\n"
        "• نرد\n"
        "• أغنية\n"
        "• أغنية + اسم\n"
        "• نرتبط\n"
        "• بوسيني\n"
        "• مساعدة"
    )


async def help_ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😈 أوامر طبوشة:\n\n"
        "🫣 صراحة\n"
        "🔥 جرأة\n"
        "💕 كت\n"
        "🎲 نرد\n"
        "🎵 أغنية\n"
        "🎵 أغنية + اسم\n"
        "💍 نرتبط\n"
        "💋 بوسيني\n"
        "❤️ بحبك\n"
        "😂 بكرهك\n\n"
        "وكمان احكي مع طبوشة عادي 😂❤️"
    )


async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🫣 صراحة:\n\n" + random.choice(TRUTHS)
    )


async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 جرأة:\n\n" + random.choice(DARES)
    )


async def kat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💕 كت:\n\n" + random.choice(KAT_QUESTIONS)
    )


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)
    await update.message.reply_text(
        f"🎲 طبوشة رمت النرد...\n\nوطلع الرقم: {number} 😂"
    )


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        await update.message.reply_text(
            f"أهلا وسهلا {member.first_name} نورتينا 🌷❤️\n\n"
            "عرفينا عن حالك 😌\n"
            "شو اسمك؟ كم عمرك؟ من وين؟ وشو حالتك الاجتماعية؟ 👀😂"
        )


async def search_freesound(update: Update, query_text: str):
    api_key = os.environ.get("FREESOUND_API_KEY")

    if not api_key:
        await update.message.reply_text(
            "😢 مفتاح الأصوات مو موجود عند طبوشة."
        )
        return

    query = urllib.parse.quote_plus(query_text)

    url = (
        "https://freesound.org/apiv2/search/text/"
        f"?query={query}"
        "&fields=name,previews,username,license,url"
        "&page_size=1"
        f"&token={api_key}"
    )

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "TabosheBot/1.0"}
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = data.get("results", [])

        if not results:
            await update.message.reply_text(
                f"😢 ما لقيت صوت مناسب لـ:\n🎵 {query_text}"
            )
            return

        sound = results[0]
        previews = sound.get("previews", {})

        audio_url = (
            previews.get("preview-hq-mp3")
            or previews.get("preview-lq-mp3")
        )

        if not audio_url:
            await update.message.reply_text(
                "😢 لقيت النتيجة بس ما فيها معاينة صوتية."
            )
            return

        name = sound.get("name", query_text)
        username = sound.get("username", "Unknown")
        license_name = sound.get("license", "Unknown")
        sound_page = sound.get("url", "")

        caption = (
            f"🎵 {name}\n"
            f"👤 {username}\n"
            f"📜 {license_name}\n"
            f"🔗 {sound_page}"
        )

        await update.message.reply_audio(
            audio=audio_url,
            title=name[:64],
            performer=username[:64],
            caption=caption[:1024],
        )

    except Exception:
        await update.message.reply_text(
            "😢 صار خطأ وأنا عم دور على الصوت، جربي مرة تانية."
        )


async def random_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await search_freesound(update, random.choice(SONGS))


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    if "بحبك" in text:
        await update.message.reply_text(random.choice(LOVE_REPLIES))
        return

    if "بكرهك" in text:
        await update.message.reply_text(random.choice(HATE_REPLIES))
        return

    if "نرتبط" in text:
        await update.message.reply_text(
            "💍 " + random.choice(RELATIONSHIP_REPLIES)
        )
        return

    if "بوسيني" in text or "بوسة" in text:
        await update.message.reply_text(random.choice(KISS_REPLIES))
        return

    if "وينك" in text:
        await update.message.reply_text(random.choice(WHERE_REPLIES))
        return

    if "استغفر الله" in text or "استغفرالله" in text:
        await update.message.reply_text(
            random.choice(ISTAGHFAR_REPLIES)
        )
        return

    bad_words = [
        "خرا",
        "طيزي",
        "كس",
        "زب",
        "شرموط",
        "قحبة",
        "نيك",
    ]

    if any(word in text for word in bad_words):
        await update.message.reply_text(
            random.choice(INSULT_REPLIES)
        )
        return

    greetings = [
        "صباح الخير",
        "صباحو",
        "مساء الخير",
        "مرحبا",
        "مراحب",
        "هاي",
        "هلا",
        "السلام عليكم",
        "سلام عليكم",
    ]

    if text in greetings:
        await update.message.reply_text(
            random.choice(GREETING_REPLIES)
        )
        return

    if text in ["باي", "bye", "باي باي", "مع السلامة"]:
        await update.message.reply_text(
            random.choice(BYE_REPLIES)
        )
        return

    if "طبوشة" in text:
        await update.message.reply_text(
            random.choice([
                "نعممم؟ 👀😂",
                "عيوني لطبوشة 😌",
                "مين ناداني؟ 😈",
                "سمعت حدا عم يحكي عني؟ 👀😂",
                "هاااا؟ شو بدكن مني؟ 😂",
            ])
        )
        return

    clean = text[1:].strip() if text.startswith("/") else text

    if clean == "صراحة":
        await truth(update, context)
        return

    if clean in ["جرأة", "جراءة", "جرائه"]:
        await dare(update, context)
        return

    if clean == "كت":
        await kat(update, context)
        return

    if clean == "نرد":
        await dice(update, context)
        return

    if clean.startswith("أغنية "):
        song_name = clean.replace("أغنية ", "", 1).strip()

        if song_name:
            await search_freesound(update, song_name)
            return

    if clean in ["أغنية", "اغنية", "أغاني", "اغاني"]:
        await random_song(update, context)
        return

    if clean == "مساعدة":
        await help_ar(update, context)
        return


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.COMMAND,
            chat
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
