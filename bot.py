import os
import random
import html
import urllib.parse
import urllib.request
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================================================
# الأسئلة
# =========================================================

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
    "شو أكتر موقف ندمتي عليه؟",
    "مين الشخص اللي مستحيل تنسيه؟",
    "هل بتسامحي بسهولة ولا لأ؟",
    "شو أكتر شي بيجذبك بالشخص؟",
]

DARES = [
    "ابعتي آخر صورة عندك بالمعرض 😂",
    "اكتبي أول 3 كلمات إجوا ببالك هلق.",
    "اعملي منشن لشخص وقولي له كلمة لطيفة ❤️",
    "ابعتي رسالة صوتية واحكي أول شي خطر ببالك 😂",
    "قولي مين أكتر شخص بالكروب بيضحكك.",
    "اكتبي جملة رومانسية لشخص من اختيارك 😏",
    "اعملي منشن لشخص وقلّيله اشتقتلك 😂",
    "اكتبي اسم الشخص اللي مستحيل ترفضي له طلب.",
    "قولي آخر شخص فتحتي معه محادثة.",
    "ابعتي إيموجي بيعبر عن حالتك العاطفية هلق.",
]

KAT_QUESTIONS = [
    "مين أول شخص خطر ببالك لما قلتي حب؟ ❤️",
    "شو أكتر شي ممكن يخلي قلبك يدق بسرعة؟",
    "هل بتقعي بالحب بسرعة ولا بدك وقت؟",
    "شو أكتر حركة رومانسية ممكن تذوبك؟",
    "هل بتحبي الغيرة بالعلاقة؟ 👀",
    "شو أكتر كلمة رومانسية بتحبي تسمعيها؟",
    "شو بالنسبة إلك معنى الحب الحقيقي؟",
    "هل ممكن تحبي شخص بعيد عنك؟",
    "شو أكتر شي ممكن يقتل الحب بالنسبة إلك؟",
    "شو أكتر شي بيخليكي تحسي بالأمان مع شخص؟",
]

GENERAL_QUESTIONS = [
    "لو فيكي تعيشي بأي بلد لمدة سنة، وين بتختاري؟ 🌍",
    "شو أكتر عادة يومية ما فيكي تتركيها؟",
    "لو ربحتي مبلغ كبير فجأة، شو أول شي بتعملي فيه؟ 💰",
    "شو أكتر أكلة ممكن تاكليها كل يوم؟ 😋",
    "شو الشي اللي نفسك تتعلميه؟",
    "شو أكتر مكان بتحبي تزوريه؟ ✈️",
    "بتفضلي الحياة الهادية ولا المغامرات؟",
    "شو أكتر صفة بتقدريها بالناس؟",
    "شو أكتر شي بيريّحك لما تكوني مضغوطة؟",
    "شو حلم نفسك تحققيه قريب؟ ✨",
]

JOKES = [
    "مرة واحد راح عالدكتور وقاله: دكتور كل ما أشرب شاي عيني بتوجعني… قاله الدكتور: جرّب شيل المعلقة من الكاسة 😂",
    "مرة واحد بخيل مات، كتبوا على قبره: ممنوع الدفن هون… الأرض إيجار 😂",
    "واحد سأل صاحبه: ليش الكمبيوتر بردان؟ قاله: لأنه فاتح الويندوز 😂",
    "مرة واحد كسلان كتير، لما حلم إنه عم يركض… صحى تعبان 😂",
    "مرة واحد نام متأخر… صحي لقى حاله بكرا 😂",
]

# =========================================================
# الردود
# =========================================================

LOVE_YES = [
    "إي طبعاً بحبك 😭❤️",
    "أكيد بحبك يا روحي 😌❤️",
    "إي بحبك، شو هالسؤال؟ 😂❤️",
    "بحبك بس لا تستغل الموضوع 😂",
]

LOVE_NO = [
    "لا 😭😂 اليوم لا، زعلتني.",
    "بصراحة؟ مو كتير اليوم 😂",
    "هلق لأ… بدك تراضيني أول 😤😂",
    "لا حالياً، بس ممكن تغيّر رأيي 😌",
]

HATE_YES = [
    "إي شوي 😂 بس لا تخاف، مو كره حقيقي.",
    "اليوم؟ إي، معصبّتني 😭😂",
    "ممكن شوي… حسب شو عملت 😤😂",
]

HATE_NO = [
    "لااا، مستحيل أكرهك 😭❤️",
    "لا يا روحي، طبوشة ما بتكرهك 😌",
    "حتى لو زعلت منك ما بكرهك 😂❤️",
]

RELATIONSHIP_REPLIES = [
    "موافقة 😌💍 بس الشبكة على حسابك 😂",
    "يلا موافقة 😭😂",
    "تمت الموافقة رسميًا 💍😂",
    "موافقة مبدئية… والباقي حسب التصرفات 👀😂",
    "ارتباط؟ بهالسرعة؟ 😭😂",
]

MARRIAGE_REPLIES = [
    "موافقة 😭💍 بس وين الشبكة؟ 😂❤️",
    "إي موافقة… خلص احجز الموعد 😂💍",
    "موافقة مبدئية، بدي مهر شوكولا 😂❤️",
    "لاااا 😭😂 خلينا أصحاب أحسن.",
    "مرفوض الطلب 😂💔",
]

KISS_REPLIES = [
    "😘😘😘😘😘",
    "مـــــوااااااااح 💋😂",
    "بوسة على راسك 😘",
    "😘💋😘💋😘",
]

GREETING_REPLIES = [
    "مراحب 😌❤️",
    "يا مرحبااا 🌷",
    "أهلااا وسهلااا 😍",
    "يا هلا ويا غلا 😂❤️",
    "منورين يا جماعة 🌷",
]

BYE_REPLIES = [
    "مع السلامة… لا تطول الغيبة 😌😂",
    "يلا باي 😂",
    "روح روح، الله معك 😂",
    "باي… واعتبرها إجازة إجبارية 😂",
]

INSULT_REPLIES = [
    "عيببب 😂",
    "بلا تربية 😭😂",
    "وين التربية والأخلاق؟ 😂",
    "احترم حالك يا قليل الأدب 😭",
    "الله يهديك بس 😂",
]

# =========================================================
# الدين
# =========================================================

DEEN_QUESTIONS = [
    {
        "q": "كم عدد الصلوات المفروضة في اليوم والليلة؟",
        "answers": ["5", "خمسة", "خمس"],
        "correct": "٥ صلوات: الفجر والظهر والعصر والمغرب والعشاء."
    },
    {
        "q": "كم عدد أركان الإسلام؟",
        "answers": ["5", "خمسة", "خمس"],
        "correct": "أركان الإسلام خمسة."
    },
    {
        "q": "كم عدد أركان الإيمان؟",
        "answers": ["6", "ستة", "ست"],
        "correct": "أركان الإيمان ستة."
    },
    {
        "q": "ما اسم الشهر الذي يصوم فيه المسلمون؟",
        "answers": ["رمضان"],
        "correct": "الشهر هو رمضان."
    },
    {
        "q": "ما هي قبلة المسلمين؟",
        "answers": ["الكعبة", "الكعبة المشرفة", "مكة", "مكة المكرمة"],
        "correct": "قبلة المسلمين هي الكعبة المشرفة في مكة المكرمة."
    },
    {
        "q": "ما اسم أول سورة في القرآن الكريم؟",
        "answers": ["الفاتحة", "سورة الفاتحة"],
        "correct": "أول سورة في ترتيب المصحف هي سورة الفاتحة."
    },
    {
        "q": "ما هي أطول سورة في القرآن الكريم؟",
        "answers": ["البقرة", "سورة البقرة"],
        "correct": "أطول سورة في القرآن الكريم هي سورة البقرة."
    },
    {
        "q": "ما اسم ليلة خير من ألف شهر؟",
        "answers": ["ليلة القدر", "القدر"],
        "correct": "هي ليلة القدر."
    },
    {
        "q": "من هو خاتم الأنبياء والمرسلين؟",
        "answers": ["محمد", "النبي محمد", "محمد صلى الله عليه وسلم"],
        "correct": "هو النبي محمد ﷺ."
    },
]

def normalize_arabic(text):
    text = text.lower().strip()

    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    for mark in [
        "َ", "ً", "ُ", "ٌ",
        "ِ", "ٍ", "ْ", "ّ", "ـ"
    ]:
        text = text.replace(mark, "")

    return " ".join(text.split())


def answer_matches(answer, accepted_answers):
    answer = normalize_arabic(answer)

    for expected in accepted_answers:
        if answer == normalize_arabic(expected):
            return True

    return False


async def start_deen(update, context):
    question = random.choice(DEEN_QUESTIONS)

    context.chat_data["deen_quiz"] = {
        "user_id": update.effective_user.id,
        "question": question,
    }

    await update.message.reply_text(
        "🕌 يلا نشوف معلوماتك الدينية 😌\n\n"
        f"❓ {question['q']}\n\n"
        "جاوبي وطبوشة رح تقولك إذا صح أو غلط ❤️"
    )


async def check_deen(update, context):
    quiz = context.chat_data.get("deen_quiz")

    if not quiz:
        return False

    user = update.effective_user

    if user.id != quiz["user_id"]:
        return False

    question = quiz["question"]

    if answer_matches(
        update.message.text,
        question["answers"]
    ):
        await update.message.reply_text(
            "✅ صحححح! برافو عليك 👏❤️\n\n"
            f"📚 {question['correct']}\n\n"
            "طبوشة فخورة فيك 😌🕌"
        )
    else:
        await update.message.reply_text(
            "❌ مو صحيح هالمرة 😅\n\n"
            f"الإجابة الصحيحة هي:\n"
            f"📚 {question['correct']}\n\n"
            "ولا يهمك، المهم نتعلم ❤️🕌"
        )

    context.chat_data.pop("deen_quiz", None)

    return True


# =========================================================
# YouTube Search
# =========================================================

async def youtube_search(update, song_name):

    query = urllib.parse.quote(song_name)

    url = (
        "https://www.youtube.com/results?"
        f"search_query={query}"
    )

    await update.message.reply_text(
        f"🔎 عم دور على:\n🎵 {song_name}\n\n"
        "👇 هاي نتيجة البحث على YouTube:\n"
        f"https://www.youtube.com/results?search_query={query}"
    )


# =========================================================
# الألعاب
# =========================================================

async def truth(update, context):
    await update.message.reply_text(
        "🫣 صراحة:\n\n"
        + random.choice(TRUTHS)
    )


async def dare(update, context):
    await update.message.reply_text(
        "🔥 جرأة:\n\n"
        + random.choice(DARES)
    )


async def kat(update, context):
    await update.message.reply_text(
        "💕 كت:\n\n"
        + random.choice(KAT_QUESTIONS)
    )


async def questions(update, context):
    await update.message.reply_text(
        "❓ سؤال طبوشة:\n\n"
        + random.choice(GENERAL_QUESTIONS)
    )


async def joke(update, context):
    await update.message.reply_text(
        "😂 نكتة طبوشة:\n\n"
        + random.choice(JOKES)
    )


async def dice(update, context):
    number = random.randint(1, 6)

    await update.message.reply_text(
        f"🎲 طبوشة رمت النرد...\n\n"
        f"وطلع الرقم: {number} 😂"
    )


# =========================================================
# الأعضاء ونسبة الحب
# =========================================================

async def love_percentage(update, context):

    members = context.chat_data.get(
        "members",
        {}
    )

    current_user = update.effective_user

    candidates = [
        (user_id, data)
        for user_id, data in members.items()
        if user_id != current_user.id
    ]

    if not candidates:
        await update.message.reply_text(
            "❤️ لسا ما بعرف حدا غيرك بالكروب 😂"
        )
        return

    chosen_id, chosen = random.choice(candidates)

    name = html.escape(
        chosen.get("name", "الشخص")
    )

    percent = random.randint(0, 100)

    mention = (
        f'<a href="tg://user?id={chosen_id}">'
        f'{name}'
        f'</a>'
    )

    await update.message.reply_text(
        f"💘 نسبة الحب بينك وبين {mention}: "
        f"<b>{percent}%</b> 😂❤️",
        parse_mode="HTML"
    )


async def welcome(update, context):

    if not update.message:
        return

    if not update.message.new_chat_members:
        return

    for member in update.message.new_chat_members:

        if member.is_bot:
            continue

        members = context.chat_data.setdefault(
            "members",
            {}
        )

        members[member.id] = {
            "name": member.first_name or "عضو",
            "username": member.username,
        }

        await update.message.reply_text(
            f"أهلا وسهلا {member.first_name} "
            f"نورتينا 🌷❤️\n\n"
            "عرفينا عن حالك 😌\n"
            "شو اسمك؟ كم عمرك؟ من وين؟ "
            "وشو حالتك الاجتماعية؟ 👀😂"
        )


# =========================================================
# START
# =========================================================

async def start(update, context):

    await update.message.reply_text(
        "😂 أهلااا! أنا طبوشة 💕\n\n"

        "جربي:\n"
        "• صراحة\n"
        "• جرأة\n"
        "• كت\n"
        "• أسئلة\n"
        "• نكتة\n"
        "• نسبة\n"
        "• نرد\n"
        "• دين\n"
        "• أغنية + اسم\n"
        "• نرتبط\n"
        "• تتزوجيني\n"
        "• بوسيني\n"
        "• مساعدة"
    )


async def help_ar(update, context):

    await update.message.reply_text(
        "😈 أوامر طبوشة:\n\n"

        "🫣 صراحة\n"
        "🔥 جرأة\n"
        "💕 كت\n"
        "❓ أسئلة\n"
        "😂 نكتة\n"
        "💘 نسبة\n"
        "🎲 نرد\n"
        "🕌 دين\n"
        "🎵 أغنية + اسم الأغنية\n"
        "💍 نرتبط\n"
        "💒 تتزوجيني\n"
        "💋 بوسيني\n\n"

        "وكمان احكي مع طبوشة عادي 😂❤️"
    )


# =========================================================
# المحادثة الرئيسية
# =========================================================

async def chat(update, context):

    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text.strip()

    lower = text.lower()

    # -----------------------------
    # لعبة الدين
    # -----------------------------

    if await check_deen(update, context):
        return

    # -----------------------------
    # تسجيل الأعضاء
    # -----------------------------

    if (
        update.effective_chat
        and update.effective_chat.type
        in ["group", "supergroup"]
    ):

        members = context.chat_data.setdefault(
            "members",
            {}
        )

        user = update.effective_user

        if user:

            members[user.id] = {
                "name": user.first_name or "عضو",
                "username": user.username,
            }

    # -----------------------------
    # أوامر
    # -----------------------------

    clean = lower

    if clean.startswith("/"):
        clean = clean[1:].strip()

    # دين

    if clean in [
        "دين",
        "ديني"
    ]:

        await start_deen(update, context)

        return

    # -----------------------------
    # بتحبيني؟
    # -----------------------------

    if (
        "بتحبيني" in lower
        or "تحبيني" in lower
    ):

        if random.choice([True, False]):

            await update.message.reply_text(
                random.choice(LOVE_YES)
            )

        else:

            await update.message.reply_text(
                random.choice(LOVE_NO)
            )

        return

    # -----------------------------
    # بتكرهيني؟
    # -----------------------------

    if (
        "بتكرهيني" in lower
        or "تكرهيني" in lower
    ):

        if random.choice([True, False]):

            await update.message.reply_text(
                random.choice(HATE_YES)
            )

        else:

            await update.message.reply_text(
                random.choice(HATE_NO)
            )

        return

    # -----------------------------
    # بحبك
    # -----------------------------

    if "بحبك" in lower:

        await update.message.reply_text(
            random.choice([
                "وأنا كمان بحبك يا روحي 😂❤️",
                "بعرف 😌 بس لا تتعلق فيني كتير 😂",
                "طبوشة كمان بتحبك 😭❤️",
                "خلص فضحتني قدام الكروب 😂❤️",
                "يا لطيف! هيك دغري؟ 😭😂",
                "وأنا كنت ناطرة منك هالكلمة 👀❤️",
            ])
        )

        return

    # -----------------------------
    # بكرهك
    # -----------------------------

    if "بكرهك" in lower:

        await update.message.reply_text(
            random.choice([
                "وأنا شو عملتلك؟ 😭😂",
                "لااااا طبوشة حساسة 😭",
                "خلص زعلت منك 😤😂",
                "بكرا بترجع بتحبني 😂",
                "مرفوضة هاي الكلمة 😂",
            ])
        )

        return

    # -----------------------------
    # نرتبط
    # -----------------------------

    if "نرتبط" in lower:

        await update.message.reply_text(
            "💍 "
            + random.choice(
                RELATIONSHIP_REPLIES
            )
        )

        return

    # -----------------------------
    # زواج
    # -----------------------------

    if (
        "تتزوجيني" in lower
        or "تتجوزيني" in lower
        or "تتزوجني" in lower
    ):

        await update.message.reply_text(
            "💒 "
            + random.choice(
                MARRIAGE_REPLIES
            )
        )

        return

    # -----------------------------
    # بوسة
    # -----------------------------

    if (
        "بوسيني" in lower
        or "بوسة" in lower
    ):

        await update.message.reply_text(
            random.choice(KISS_REPLIES)
        )

        return

    # -----------------------------
    # نكتة
    # -----------------------------

    if clean in [
        "نكتة",
        "نكت"
    ]:

        await joke(update, context)

        return

    # -----------------------------
    # أسئلة
    # -----------------------------

    if clean in [
        "اسئلة",
        "أسئلة",
        "اسئله",
        "أسئله"
    ]:

        await questions(update, context)

        return

    # -----------------------------
    # نسبة
    # -----------------------------

    if clean == "نسبة":

        await love_percentage(
            update,
            context
        )

        return

    # -----------------------------
    # نرد
    # -----------------------------

    if clean == "نرد":

        await dice(
            update,
            context
        )

        return

    # -----------------------------
    # صراحة
    # -----------------------------

    if clean == "صراحة":

        await truth(
            update,
            context
        )

        return

    # -----------------------------
    # جرأة
    # -----------------------------

    if clean in [
        "جرأة",
        "جراءة",
        "جرائه"
    ]:

        await dare(
            update,
            context
        )

        return

    # -----------------------------
    # كت
    # -----------------------------

    if clean == "كت":

        await kat(
            update,
            context
        )

        return

    # -----------------------------
    # أغنية
    # -----------------------------

    if (
        clean.startswith("أغنية ")
        or clean.startswith("اغنية ")
    ):

        if clean.startswith("أغنية "):

            song_name = clean[
                len("أغنية "):
            ].strip()

        else:

            song_name = clean[
                len("اغنية "):
            ].strip()

        if song_name:

            await youtube_search(
                update,
                song_name
            )

        return

    # -----------------------------
    # أغنية بدون اسم
    # -----------------------------

    if clean in [
        "أغنية",
        "اغنية",
        "أغاني",
        "اغاني"
    ]:

        await update.message.reply_text(
            "🎵 اكتبي مثلاً:\n\n"
            "أغنية قولوا لها"
        )

        return

    # -----------------------------
    # طبوشة
    # -----------------------------

    if "طبوشة" in lower:

        await update.message.reply_text(
            random.choice([
                "يا عيون طبوشة وقلبها وروحها 😭❤️",
                "يا روحي إنت، طبوشة هون 😌❤️",
                "عيون طبوشة إلك، شو بدك؟ 🥹❤️",
                "يا قلب طبوشة إنت 😭❤️",
                "نعم يا عيوني، ناديتني؟ 😌",
                "طبوشة كلها سمعتك وجاية لعندك 😂❤️",
            ])
        )

        return

    # -----------------------------
    # تحيات
    # -----------------------------

    greetings = [
        "صباح الخير",
        "صباحو",
        "مساء الخير",
        "مرحبا",
        "مراحب",
        "هاي",
        "هلا",
        "السلام عليكم",
        "سلام عليكم"
    ]

    if clean in greetings:

        await update.message.reply_text(
            random.choice(
                GREETING_REPLIES
            )
        )

        return

    # -----------------------------
    # باي
    # -----------------------------

    if clean in [
        "باي",
        "bye",
        "باي باي",
        "مع السلامة"
    ]:

        await update.message.reply_text(
            random.choice(
                BYE_REPLIES
            )
        )

        return

    # -----------------------------
    # شتائم
    # -----------------------------

    bad_words = [
        "خرا",
        "طيزي",
        "كس",
        "زب",
        "شرموط",
        "قحبة",
        "نيك"
    ]

    if any(
        word in lower
        for word in bad_words
    ):

        await update.message.reply_text(
            random.choice(
                INSULT_REPLIES
            )
        )

        return

    # -----------------------------
    # مساعدة
    # -----------------------------

    if clean == "مساعدة":

        await help_ar(
            update,
            context
        )

        return


# =========================================================
# تشغيل البوت
# =========================================================

def main():

    token = os.environ[
        "TELEGRAM_BOT_TOKEN"
    ]

    app = (
        Application
        .builder()
        .token(token)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome
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
