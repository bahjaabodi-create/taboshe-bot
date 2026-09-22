import os
import random
import json
import html
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


# =========================
# الألعاب والأسئلة
# =========================

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
    "مين أكتر شخص ممكن يسرق قلبك من أول كلمة؟ ❤️",
    "شو أول شي بتلاحظيه بالشخص اللي بيعجبك؟ 👀",
    "لو حبيبك طلب منك أمنية، شو بتتمني منه؟",
    "هل بتفضلي الاعتراف بالحب بشكل مباشر ولا بالتلميحات؟",
    "شو أكتر موقف رومانسي ممكن يخليكي ما تنسي الشخص؟",
    "هل الغيرة بالنسبة إلك دليل حب ولا ممكن تكون مزعجة؟",
    "لو لازم تختاري بين الحب والمال، شو بتختاري؟",
    "شو أكتر اسم دلع بتحبي تسمعيه؟ 😌",
    "هل ممكن تحبي شخص ما بيبادلك نفس الشعور؟",
    "مين أول شخص بتحكي معه لما يصير معك شي حلو؟",
    "شو أكتر شي ممكن يخليكي تتعلقي بشخص بسرعة؟",
    "لو الشخص اللي بتحبيه طلب منك تسافري معه، بتوافقي؟ ✈️❤️",
    "شو الرسالة اللي بتتمني توصلك من شخص معين؟",
    "هل بتفضلي علاقة مليانة كلام وحكي ولا أفعال أكتر؟",
    "شو أكتر تفصيل صغير بتحبيه بالعلاقات؟",
]

GENERAL_QUESTIONS = [
    "لو فيكي تعيشي بأي بلد لمدة سنة، وين بتختاري؟ 🌍",
    "شو أكتر عادة يومية ما فيكي تتركيها؟",
    "لو ربحتي مبلغ كبير فجأة، شو أول شي بتعملي فيه؟ 💰",
    "شو أكتر أكلة ممكن تاكليها كل يوم وما تملّي منها؟ 😋",
    "مين أكتر شخص بتعتبريه قدوة بحياتك؟",
    "شو الشي اللي نفسك تتعلميه وما تعلمتيه لسا؟",
    "لو فيكي ترجعي لعمر معين، أي عمر بتختاري وليش؟",
    "شو أكتر مكان بتحبي تزوريه؟ ✈️",
    "بتفضلي الحياة الهادية ولا المليانة مغامرات؟",
    "شو أكتر صفة بتقدريها بالناس؟",
    "لو فيكي تغيري شي واحد بالعالم، شو بتغيري؟ 🌍",
    "شو أكتر موقف خلاكي تضحكي من قلبك؟ 😂",
    "بتفضلي البحر ولا الجبل؟ 🌊⛰️",
    "شو أكتر شي بيريّحك لما تكوني مضغوطة؟",
    "لو لازم تختاري أكلة واحدة لباقي حياتك، شو بتختاري؟",
    "شو أكتر تطبيق بتستخدميه يومياً؟",
    "مين الشخص اللي بتلجئي له لما تحتاجي نصيحة؟",
    "شو حلم نفسك تحققيه قريب؟ ✨",
    "بتفضلي الصبح بكير ولا السهر؟ 🌞🌙",
    "شو أهم درس تعلمتيه من الحياة؟",
    "لو فيكي تقضي يوم كامل بدون موبايل، بتقدري؟ 😂",
    "شو أكتر فيلم أو مسلسل ممكن تعيدي مشاهدته؟",
    "شو البلد اللي نفسك تزوريه أول شي؟",
    "شو أكتر شي بيخلي يومك أحلى؟ ❤️",
    "لو عندك آلة زمن، بتروحي للماضي ولا المستقبل؟",
]

JOKES = [
    "مرة واحد راح عالدكتور وقاله: دكتور كل ما أشرب شاي عيني بتوجعني… قاله الدكتور: جرّب شيل المعلقة من الكاسة 😂",
    "مرة واحد بخيل مات، كتبوا على قبره: ممنوع الدفن هون… الأرض إيجار 😂",
    "واحد سأل صاحبه: ليش الكمبيوتر بردان؟ قاله: لأنه فاتح الويندوز 😂",
    "مرة واحد كسلان كتير، لما حلم إنه عم يركض… صحى تعبان 😂",
    "واحد راح يشتري نظارة، سأله البائع: نظر ولا شمس؟ قاله: لا، أنا اسمي أحمد 😂",
    "مرة واحد نسي ينام… صحى لقى حاله تعبان من السهر 😂",
    "واحد قال لصاحبه: أنا سريع بالحساب. قاله: كم 2+2؟ قاله: لحظة… عم احسبها بسرعة 😂",
    "مرة واحد سأل صاحبه: شو أخبارك؟ قاله: نفس الأخبار بس بنسخة جديدة 😂",
    "واحد فتح محل عصير وسماه: عصير وخلصنا 😂",
    "مرة واحد دخل مطعم وقال: عندكم رجل ضفدع؟ قالوله: لا. قال: طيب جيبولي رجل دجاج 😂",
    "واحد قال لمرته: أنا بحب المفاجآت. قالتله: طيب مفاجأة… ما طبخت اليوم 😂",
    "مرة واحد اشترى ساعة ضد المي، عطش وما شربها 😂",
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
]

HATE_REPLIES = [
    "وأنا شو عملتلك؟ 😭😂",
    "لااااا طبوشة حساسة 😭",
    "خلص زعلت منك 😤😂",
    "بكرا بترجع بتحبني، بعرفك 😌😂",
    "مرفوضة هاي الكلمة 😂",
    "معقول بعد كل هالحب؟ 😭",
]

RELATIONSHIP_REPLIES = [
    "موافقة 😌💍 بس الشبكة على حسابك 😂",
    "تمت الموافقة رسميًا 💍😂",
    "موافقة، بس عندي شروط 😏",
    "خلص ارتبطنا، مبروك إلك ولي 😂❤️",
    "طلبك قيد الدراسة من لجنة طبوشة 😂",
    "ممكن… بس بدك تثبت إنك بتستاهل 😌",
    "ارتباط؟ بهالسرعة؟ 😭😂",
    "حط طلبك بالدور، في ناس قبلك 😂",
    "موافقة مبدئية… والباقي حسب التصرفات 👀😂",
]

MARRIAGE_REPLIES = [
    "موافقة 😭💍 بس وين الشبكة؟ 😂❤️",
    "إي موافقة… خلص احجز الموعد 😂💍",
    "موافقة مبدئية، بس بدي مهر عبارة عن شوكولا 😂❤️",
    "موافقة… بس ممنوع الندم بعدين 😌💍",
    "أكيد موافقة، طبوشة قالت نعم 😂❤️",
    "لااااا 😭😂 خلينا أصحاب أحسن.",
    "مرفوض الطلب 😂💔 جرب حظك مع غيري.",
    "لا يا روحي، هالمرة طبوشة قالت لأ 😂",
    "الزواج؟ شكراً، بس طلبك مرفوض مع الحب 😂",
    "مو موافقة 😭😂 بس فينا نضل حلوين مع بعض.",
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
]

SHUTUP_REPLIES = [
    "إنت بتخرس 😂",
    "خرسة بوجهك يا قليل الأدب 😭😂",
    "أنا؟ إنت ابدأ واسكت 😂",
    "طبوشة ما بتخرس… بس إنت جرّب 😂",
    "مين سمحلك تأمرني؟ 😭",
    "خرس أنت أول وبعدين منحكي 😂",
]

INSULT_REPLIES = [
    "عيببب 😂",
    "بلا تربية 😭😂",
    "وين التربية والأخلاق؟ 😂",
    "احترم حالك يا قليل الأدب 😭",
    "طبوشة سمعت كل شي 👀😂",
    "استغفر ربك وروق 😂",
]

WHERE_REPLIES = [
    "بقلبك ❤️",
    "هون… بس مخبية 👀",
    "جنبك بس إنت ما بتشوفني 😂",
    "ببالك يا حلو 😌",
    "موجودة، وين بدي روح؟ 😂",
]

BYE_REPLIES = [
    "بالناقص وارتحنا 😂",
    "مع السلامة… لا تطول الغيبة 😌😂",
    "يلا باي، الكروب رح يرتاح شوي 😂",
    "باي؟ أخيراً 😂",
    "روح روح، الله معك 😂",
    "بالناقص يا عيوني 😭😂",
]

ISTAGHFAR_REPLIES = [
    "هي اصطخفر الله 😭😂",
    "اصطخفر الله العظيم 😂",
    "طبوشة استغفرت معك 😭",
    "الله يغفرلنا جميعاً 😂❤️",
]


# =========================
# البداية والمساعدة
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "• أغنية\n"
        "• نرتبط\n"
        "• تتزوجيني\n"
        "• بوسيني\n"
        "• مساعدة"
    )


async def help_ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😈 أوامر طبوشة:\n\n"
        "🫣 صراحة\n"
        "🔥 جرأة\n"
        "💕 كت\n"
        "❓ أسئلة\n"
        "😂 نكتة\n"
        "💘 نسبة\n"
        "🎲 نرد\n"
        "🎵 أغنية\n"
        "💍 نرتبط\n"
        "💒 تتزوجيني\n"
        "💋 بوسيني\n\n"
        "وكمان احكي مع طبوشة عادي 😂❤️"
    )


# =========================
# الألعاب
# =========================

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


async def general_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ سؤال طبوشة:\n\n" + random.choice(GENERAL_QUESTIONS)
    )


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 نكتة طبوشة:\n\n" + random.choice(JOKES)
    )


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)

    await update.message.reply_text(
        f"🎲 طبوشة رمت النرد...\n\n"
        f"وطلع الرقم: {number} 😂"
    )


# =========================
# نسبة الحب
# =========================

async def love_percentage(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    members = context.chat_data.get("members", {})
    current_user = update.effective_user

    candidates = [
        (user_id, data)
        for user_id, data in members.items()
        if user_id != current_user.id
    ]

    if not candidates:
        await update.message.reply_text(
            "❤️ لسا ما بعرف حدا غيرك بالكروب 😂\n"
            "خلي كم شخص يحكوا معي وبعملكن النسبة."
        )
        return

    chosen_id, chosen = random.choice(candidates)

    chosen_name = html.escape(
        chosen.get("name") or "الشخص"
    )

    mention = (
        f'<a href="tg://user?id={chosen_id}">'
        f'{chosen_name}'
        f'</a>'
    )

    percent = random.randint(0, 100)

    await update.message.reply_text(
        f"💘 نسبة الحب بينك وبين {mention}: "
        f"<b>{percent}%</b> 😂❤️\n\n"
        "📊 حسب جهاز طبوشة العاطفي العشوائي طبعاً!",
        parse_mode="HTML",
    )


# =========================
# ترحيب الأعضاء الجدد
# =========================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message or not update.message.new_chat_members:
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
            "نورتينا 🌷❤️\n\n"
            "عرفينا عن حالك 😌\n"
            "شو اسمك؟ كم عمرك؟ من وين؟ "
            "وشو حالتك الاجتماعية؟ 👀😂"
        )


# =========================
# الأغاني - النظام القديم
# =========================

async def search_freesound(
    update: Update,
    query_text: str
):
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
            headers={
                "User-Agent": "TabosheBot/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        results = data.get("results", [])

        if not results:
            await update.message.reply_text(
                f"😢 ما لقيت صوت مناسب لـ:\n"
                f"🎵 {query_text}"
            )
            return

        sound = results[0]

        previews = sound.get(
            "previews",
            {}
        )

        audio_url = (
            previews.get("preview-hq-mp3")
            or previews.get("preview-lq-mp3")
        )

        if not audio_url:
            await update.message.reply_text(
                "😢 لقيت النتيجة بس ما فيها "
                "معاينة صوتية."
            )
            return

        name = sound.get(
            "name",
            query_text
        )

        username = sound.get(
            "username",
            "Unknown"
        )

        license_name = sound.get(
            "license",
            "Unknown"
        )

        sound_page = sound.get(
            "url",
            ""
        )

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
            "😢 صار خطأ وأنا عم دور على الصوت، "
            "جربي مرة تانية."
        )


async def random_song(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    songs = [
        "piano",
        "romantic music",
        "love music",
        "happy music",
        "sad music",
        "lofi",
    ]

    await search_freesound(
        update,
        random.choice(songs)
    )


# =========================
# الردود الرئيسية
# =========================

async def chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    # حفظ الأشخاص الذين تفاعلوا مع البوت
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
        await update.message.reply_text(
            "💍 " + random.choice(
                RELATIONSHIP_REPLIES
            )
        )
        return

    # تتزوجيني
    if (
        "تتزوجيني" in text
        or "تتجوزيني" in text
        or "تتزوجني" in text
    ):
        await update.message.reply_text(
            "💍 " + random.choice(
                MARRIAGE_REPLIES
            )
        )
        return

    # بوسيني
    if (
        "بوسيني" in text
        or "بوسة" in text
    ):
        await update.message.reply_text(
            random.choice(KISS_REPLIES)
        )
        return

    # وينك
    if "وينك" in text:
        await update.message.reply_text(
            random.choice(WHERE_REPLIES)
        )
        return

    # استغفر الله
    if (
        "استغفر الله" in text
        or "استغفرالله" in text
    ):
        await update.message.reply_text(
            random.choice(
                ISTAGHFAR_REPLIES
            )
        )
        return

    # اخرس / اخرسي
    if text in [
        "اخرس",
        "اخرسي",
        "اخرص",
        "اخرصي",
    ]:
        await update.message.reply_text(
            random.choice(
                SHUTUP_REPLIES
            )
        )
        return

    # الشتائم
    bad_words = [
        "خرا",
        "طيزي",
        "كس",
        "زب",
        "شرموط",
        "قحبة",
        "نيك",
    ]

    if any(
        word in text
        for word in bad_words
    ):
        await update.message.reply_text(
            random.choice(
                INSULT_REPLIES
            )
        )
        return

    # التحيات
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
            random.choice(
                GREETING_REPLIES
            )
        )
        return

    # باي
    if text in [
        "باي",
        "bye",
        "باي باي",
        "مع السلامة",
    ]:
        await update.message.reply_text(
            random.choice(
                BYE_REPLIES
            )
        )
        return

    # نكتة
    if (
        text == "نكتة"
        or text == "نكت"
    ):
        await joke(update, context)
        return

    # أسئلة
    if text in [
        "اسئلة",
        "أسئلة",
        "اسئله",
        "أسئله",
    ]:
        await general_questions(
            update,
            context
        )
        return

    # نسبة
    if text == "نسبة":
        await love_percentage(
            update,
            context
        )
        return

    # طبوشة
    if "طبوشة" in text:
        await update.message.reply_text(
            random.choice([
                "يا عيون طبوشة وقلبها وروحها 😭❤️",
                "يا روحي إنت، طبوشة هون 😌❤️",
                "عيون طبوشة إلك، شو بدك؟ 🥹❤️",
                "يا قلب طبوشة إنت 😭❤️",
                "يا بعد قلب طبوشة وروحها 😂❤️",
                "نعم يا عيوني، ناديتني؟ 😌",
                "طبوشة كلها سمعتك وجاية لعندك 😂❤️",
                "يا روح الروح، شو بدك من طبوشة؟ 🥹",
            ])
        )
        return

    clean = (
        text[1:].strip()
        if text.startswith("/")
        else text
    )

    # صراحة
    if clean == "صراحة":
        await truth(
            update,
            context
        )
        return

    # جرأة
    if clean in [
        "جرأة",
        "جراءة",
        "جرائه",
    ]:
        await dare(
            update,
            context
        )
        return

    # كت
    if clean == "كت":
        await kat(
            update,
            context
        )
        return

    # نرد
    if clean == "نرد":
        await dice(
            update,
            context
        )
        return

    # أغنية + اسم
    if clean.startswith("أغنية "):

        song_name = clean.replace(
            "أغنية ",
            "",
            1
        ).strip()

        if song_name:
            await search_freesound(
                update,
                song_name
            )
            return

    # أغنية عشوائية
    if clean in [
        "أغنية",
        "اغنية",
        "أغاني",
        "اغاني",
    ]:
        await random_song(
            update,
            context
        )
        return

    # مساعدة
    if clean == "مساعدة":
        await help_ar(
            update,
            context
        )
        return


# =========================
# تشغيل البوت
# =========================

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
