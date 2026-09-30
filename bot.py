import os
import random
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# إعدادات عامة
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# =========================================================
# الأسئلة والألعاب
# =========================================================

TRUTHS = [
    "مين آخر شخص فكرت فيه قبل ما تنامي؟ 👀",
    "شو أكتر سر مخبيتيه عن أصحابك؟",
    "مين الشخص اللي بتشتاقيله وما بتقولي؟",
    "شو أكتر موقف ندمتي عليه؟",
    "لو فيكي ترجعي بالزمن، شو أول شي بتغيريه؟",
    "مين أكتر شخص بتثقي فيه؟",
    "شو أكتر شي بيزعجك بالعلاقات؟",
    "هل سبق وحبيتي شخص وما عرف؟",
    "شو أكتر صفة بتحبيها بالشخص اللي قدامك؟",
    "شو أكتر شي ممكن يخليكي تغاري؟",
    "هل بتسامحي بسهولة؟",
    "شو أكتر كذبة قلتيها بحياتك؟",
    "مين الشخص اللي مستحيل تنسيه؟",
    "شو الشي اللي بتخافي تخسريه؟",
    "لو لازم تعترفي بشي هلق، شو هو؟",
    "هل سبق وندمتي على حب؟",
    "شو أكتر موقف محرج صار معك؟",
    "مين أول حب بحياتك؟",
    "هل بتفضلي الحب ولا الاستقرار؟",
    "شو الشي اللي نفسك حدا يفهمه عنك؟",
]

DARES = [
    "ابعتي آخر إيموجي استخدمتيه 😂",
    "اكتبي أول كلمة بتخطر ببالك هلق.",
    "غيّري اسمك لدقيقة لاسم مضحك 😂",
    "ابعتي رسالة فيها 3 إيموجيات فقط.",
    "اكتبي جملة رومانسية بدون استخدام كلمة حب.",
    "قولي مين أكتر شخص بالكروب بيضحكك.",
    "اكتبي اعتذار لشخص ما عملتي له شي 😂",
    "اكتبي جملة كاملة بدون حرف الألف.",
    "احكي نكتة حتى لو كانت بايخة.",
    "اكتبي اسم أول شخص خطر ببالك.",
    "ابعتي 5 قلوب بألوان مختلفة.",
    "اكتبي جملة وكأنك شخصية مشهورة.",
]

KAT_QUESTIONS = [
    "مين أكتر شخص بالكروب ممكن تتزوجيه؟ 👀",
    "مين أكتر شخص بتحسيه غامض؟",
    "مين أكتر شخص بيضحكك؟",
    "مين أكتر شخص بتحسيه رومانسي؟",
    "مين أكتر شخص ممكن تثقي فيه بسر؟",
    "مين أكتر شخص ممكن تتخانقي معه؟ 😂",
    "مين أكتر شخص حضوره ملفت؟",
    "مين أكتر شخص ممكن تسافري معه؟",
    "مين أكتر شخص بتحسيه حنون؟",
    "مين أكتر شخص ممكن يكون شريك حياتك؟",
]

GENERAL_QUESTIONS = [
    "شو أكتر شي بتحبيه بشخصيتك؟",
    "شو أكتر عادة نفسك تتخلصي منها؟",
    "لو ربحتي مليون يورو شو أول شي بتشتريه؟",
    "شو البلد اللي نفسك تزوريه؟",
    "شو أكتر أكلة مستحيل تملّي منها؟",
    "شو فيلم أو مسلسل ما بتنسيه؟",
    "شو أغنية مرتبطة بذكرى عندك؟",
    "شو أكتر شي بيحسن مزاجك؟",
    "شو أكتر شي بيخليكي تعصبي؟",
    "لو فيكي تعيشي يوم واحد من الماضي، أي يوم؟",
    "لو فيكي تعرفي حقيقة واحدة عن المستقبل، شو بتختاري؟",
    "شو أهم صفة بالنسبة إلك بالشخص؟",
    "شو أكتر شي بتقدري تسامحي عليه؟",
    "شو أكتر شي مستحيل تسامحي عليه؟",
    "بتفضلي الحياة الهادية ولا المغامرات؟",
    "شو أكتر حلم نفسك تحققيه؟",
    "شو أكتر مكان بتحسي فيه براحة؟",
    "شو أكتر ذكرى بتضحكك؟",
    "لو عندك تذكرة سفر مجانية، لوين بتروحي؟",
    "شو الشي اللي مستحيل تشتريه مهما كان سعره؟",
    "شو أكتر كلمة بتحبي تسمعيها؟",
    "شو أكتر موقف غير طريقة تفكيرك؟",
    "بتفضلي تكوني مشهورة ولا غنية؟",
    "شو أكتر شي بتندمي عليه لما تتسرعي؟",
    "شو أكتر صفة بتكرهيها بالناس؟",
    "شو أكتر صفة بتحبيها بالناس؟",
    "مين الشخص اللي بتحكي معه لما تكوني مضايقة؟",
    "شو أكتر شي ممكن يخلي يومك حلو؟",
    "لو فيكي تغيري قانون واحد بالعالم، شو بتغيري؟",
    "شو أكتر قرار أخدتيه وكنتِ فخورة فيه؟",
    "شو أكتر شي نفسك تتعلميه؟",
    "بتفضلي الحب الهادئ ولا الحب المليان شغف؟",
    "شو أكتر موقف خلاكي تضحكي بوقت غلط؟",
    "شو أكتر شي الناس بيفهموه غلط عنك؟",
]

JOKES = [
    "مرة واحد بخيل مات… كتبوا على قبره: للبدل 😂",
    "واحد سأل صاحبه: ليش الكمبيوتر بردان؟ قاله: فاتح الويندوز 😂",
    "مرة واحد راح للدكتور وقاله: كل ما أشرب شاي بتوجعني عيني… قاله الدكتور: شيل الملعقة من الكاسة 😂",
    "واحد نام متأخر… فاته الحلم 😂",
    "مرة واحد سأل بخيل: ليش ما بتتزوج؟ قاله: خايف تطلع المصاريف شخصين 😂",
    "واحد راح يشتري نظارة… قال للبائع: بدي شي أشوف فيه مستقبلي… قاله: تفضل، هاي فاتورة الأسعار 😂",
]

# =========================================================
# صح أو غلط
# =========================================================

TRUE_FALSE_QUESTIONS = [
    ("الأخطبوط عنده ثلاثة قلوب.", "صح"),
    ("أستراليا أكبر من روسيا.", "غلط"),
    ("لسان الزرافة أزرق.", "صح"),
    ("كل البطاريق تعيش في القطب الشمالي.", "غلط"),
    ("القمر أكبر من الأرض.", "غلط"),
    ("قلب الإنسان يقع في منتصف الجسم تماماً.", "غلط"),
    ("المحيط الهادئ أكبر محيط في العالم.", "صح"),
    ("المشتري أكبر كواكب المجموعة الشمسية.", "صح"),
    ("الشمس كوكب.", "غلط"),
    ("النحل يتواصل بالرقص.", "صح"),
    ("الخفافيش من الثدييات.", "صح"),
    ("التماسيح تستطيع إخراج لسانها مثل الإنسان.", "غلط"),
    ("الجليد أقل كثافة من الماء.", "صح"),
    ("الدماغ نفسه لا يحتوي على مستقبلات للألم.", "صح"),
    ("الماء يغلي دائماً عند 100 درجة مئوية مهما كان الارتفاع.", "غلط"),
    ("أفريقيا أكبر قارة في العالم.", "غلط"),
    ("الأرض تدور حول الشمس.", "صح"),
    ("البرق يمكن أن يضرب نفس المكان أكثر من مرة.", "صح"),
    ("الحوت الأزرق أكبر حيوان معروف عاش على الأرض.", "صح"),
    ("الديناصورات عاشت قبل ظهور الثدييات.", "صح"),
    ("العسل يمكن أن يبقى صالحاً لفترة طويلة جداً إذا حُفظ جيداً.", "صح"),
    ("الملح يذوب في الزيت مثل الماء.", "غلط"),
    ("الدلافين من الأسماك.", "غلط"),
    ("قوس قزح يحتوي تقليدياً على سبعة ألوان.", "صح"),
    ("إيفرست أعلى جبل فوق مستوى سطح البحر.", "صح"),
    ("كل الثعابين سامة.", "غلط"),
    ("النباتات تطلق الأكسجين أثناء البناء الضوئي.", "صح"),
    ("الماء المالح يتجمد عند نفس درجة تجمد الماء النقي تماماً.", "غلط"),
    ("المغناطيس يجذب الحديد.", "صح"),
    ("القمر يضيء من نفسه.", "غلط"),
    ("الذهب معدن.", "صح"),
    ("العناكب من الحشرات.", "غلط"),
    ("الإنسان لديه 206 عظمة تقريباً عند البالغين.", "صح"),
    ("الصوت ينتقل في الفراغ.", "غلط"),
    ("كوكب الزهرة أقرب كوكب إلى الشمس.", "غلط"),
    ("الأرض لها قمر طبيعي واحد.", "صح"),
    ("الفيل يستطيع القفز.", "غلط"),
    ("الخفاش هو الثديي الوحيد القادر على الطيران الحقيقي.", "صح"),
    ("البرق أسخن من سطح الشمس.", "صح"),
    ("الذهب يصدأ مثل الحديد.", "غلط"),
    ("الماء يتكون من الهيدروجين والأكسجين.", "صح"),
]

# =========================================================
# هذا أو هذا
# =========================================================

THIS_OR_THAT = [
    "الحب ❤️ ولا المصاري 💰؟",
    "السفر ✈️ ولا القعدة بالبيت 🏠؟",
    "السهر 🌙 ولا النوم بكير 😴؟",
    "القهوة ☕ ولا الشاي 🍵؟",
    "بيتزا 🍕 ولا برغر 🍔؟",
    "الرسائل 💬 ولا المكالمات 📞؟",
    "الحضن 🤗 ولا البوسة 💋؟",
    "البحر 🌊 ولا الجبل ⛰️؟",
    "فيلم 🎬 ولا لعبة 🎮؟",
    "القطط 🐈 ولا الكلاب 🐕؟",
    "الزواج 💍 ولا الحب بدون زواج ❤️؟",
    "المدينة 🏙️ ولا الريف 🌳؟",
    "تصرفي المصاري 💸 ولا توفريها 💰؟",
    "الغيرة 🔥 ولا اللامبالاة 🧊؟",
    "الاهتمام ❤️ ولا الكلام الحلو 🥰؟",
    "تعرفي الحقيقة 🤯 ولا تفضلي ما تعرفي؟",
    "السرية 🤫 ولا الصراحة 🗣️؟",
    "الذكاء 🧠 ولا الجمال ✨؟",
    "شخص يضحكك 😂 ولا شخص يفهمك 🫂؟",
    "الصيف ☀️ ولا الشتاء ❄️؟",
    "شوكولا 🍫 ولا بوظة 🍦؟",
    "تغني 🎤 ولا ترقصي 💃؟",
    "إنستغرام 📸 ولا سناب 👻؟",
    "رسالة طويلة 💌 ولا كلمة مختصرة من الشخص الصح ❤️؟",
    "أصحاب كتير 👥 ولا شخص واحد مقرب 🫂؟",
    "بيت كبير 🏠 ولا سفر دائم ✈️؟",
    "تحبي ❤️ ولا تنحبي 🥰؟",
    "علاقة مليانة شغف 🔥 ولا علاقة هادية 🤍؟",
    "تكوني محبوبة ❤️ ولا محترمة 🤝؟",
    "ترجعي للماضي ⏳ ولا تشوفي المستقبل 🔮؟",
    "راتب عالي مع شغل متعب 💰 ولا راتب أقل مع راحة 😌؟",
    "سفر مفاجئ ✈️ ولا سفر مخطط 📋؟",
    "ورد 🌹 ولا شوكولا 🍫؟",
    "حفلة كبيرة 🎉 ولا سهرة هادية 🕯️؟",
    "صور كتير 📸 ولا ذكريات بدون صور 🧠؟",
    "تلميحات 👀 ولا اعتراف مباشر 🗣️؟",
    "تحكي كل شي 🗣️ ولا تحتفظي بأسرارك 🤫؟",
    "تعرفي سبب الفراق 💔 ولا تفضلي ما تعرفي؟",
    "شخص غامض 👀 ولا شخص واضح؟",
    "حضن طويل 🤗 ولا بوسة طويلة 💋؟",
    "الاهتمام بالأفعال ❤️ ولا بالكلام 💬؟",
    "تعيشي يوم بدون موبايل 📵 ولا بدون إنترنت 🌐؟",
    "تربحي سيارة 🚗 ولا رحلة حول العالم 🌍؟",
    "تكوني غنية 💰 ولا مشهورة ⭐؟",
    "تنامي طول اليوم 😴 ولا تسهري طول الليل 🌙؟",
    "تضحكي طول الوقت 😂 ولا تاكلي طول الوقت 🍕؟",
    "تعيشي بالبحر 🌊 ولا فوق الجبل ⛰️؟",
    "صديق صريح جداً 🗣️ ولا صديق حنون جداً 🫂؟",
]

# =========================================================
# الردود
# =========================================================

GREETING_REPLIES = [
    "هلا والله 😌",
    "أهلين فيكي ❤️",
    "يا هلااا 😂",
    "أهلاً وسهلاً 🌷",
    "نورتِ الكروب 😌",
]

LOVE_YES = [
    "وأنا كمان بحبك يا روحي 😂❤️",
    "بعرف 😌 بس لا تتعلق فيني كتير 😂",
    "طبوشة كمان بتحبك 😭❤️",
    "وأنا شو بدي ساوي بهالحب هاد؟ 😭😂",
    "خلص فضحتني قدام الكروب 😂❤️",
    "يا لطيف! هيك دغري؟ 😭😂",
    "وأنا كنت ناطرة منك هالكلمة 👀❤️",
]

LOVE_NO = [
    "يا خسارة 😂",
    "خلص كسرتي قلبي 😭",
    "ولا يهمك… طبوشة قوية 😂",
]

HATE_YES = [
    "واضح 😂",
    "وأنا شو عملتلك؟ 😭",
    "طيب ليش كل هالكراهية 😂",
]

HATE_NO = [
    "هيك بدي ياكي 😌",
    "كنت عارفة 😂❤️",
    "طبوشة محبوبة غصب 😌",
]

RELATIONSHIP_REPLIES = [
    "طبوشة ما بتدخل بعلاقات… أنا هون للخراب 😂",
    "العلاقة بدها شجاعة وأنا عندي بس نكت 😂",
    "خليكن إنتو حبّوا وأنا بتفرج 👀",
]

MARRIAGE_REPLIES = [
    "تم الزواج مبدئياً… بس وين العرس؟ 😂💍",
    "موافقة، بس المهر شو؟ 👀",
    "زوجني؟ طيب أول شي نشوف العريس 😂",
    "على سنة الله ورسوله… طبوشة دخلت بالجو 💍😂",
]

KISS_REPLIES = [
    "قبلة وصلت 😘",
    "هيك فجأة؟ 😂",
    "طبوشة انحرجت 😭😂",
    "خدي بوسة بالمقابل 😘",
]

BYE_REPLIES = [
    "مع السلامة ❤️",
    "باي باي 😭",
    "لا تطولي الغيبة 😂",
    "روحي وارجعي بسرعة 😌",
]

WHERE_REPLIES = [
    "هون بينكن 😂",
    "بكل مكان ولا مكان بنفس الوقت 👀",
    "طبوشة موجودة بالكروب 😌",
]

ISTAGHFAR_REPLIES = [
    "استغفر الله وأتوب إليه 🤍",
    "أستغفر الله العظيم 🌿",
    "الله يغفرلنا جميعاً 🤍",
]

DEEN_QUESTIONS = [
    ("كم عدد الصلوات المفروضة في اليوم؟", ["5", "خمسة"]),
    ("كم عدد أركان الإسلام؟", ["5", "خمسة"]),
    ("ما أول شهر في السنة الهجرية؟", ["محرم"]),
    ("ما اسم قبلة المسلمين؟", ["الكعبة", "الكعبة المشرفة"]),
    ("كم عدد أركان الإيمان؟", ["6", "ستة"]),
]

# =========================================================
# نجم - ممنوع التعديل
# =========================================================

LIP_REPLIES = [
    "دكتورة؟ لا… هاي لحالها مستوى تاني 🖤",
    "الدكتورة إذا حكت، الكل بينتبه غصباً عنه",
    "الدكتورة ما بتحتاج تثبت حالها… وجودها لحاله إثبات",
    "مو كل دكتورة بتكون بهالحضور… بس دكتورتي غير",
    "في ناس بتلفت الانتباه، ودكتورتي بتاخده كله",
    "مين سمح للدكتورة تكون بهالقد جميلة؟",
    "لو في لقب أعلى من دكتورة، كان لازم يكون إلها.",
    "هي مو نجم بس… هي الدكتورة اللي النجوم بتتطلع عليها",
    "الدكتورة إذا ابتسمت، كل نظريات الجمال بتحتاج تحديث",

    "نجمي هي كل الحكاية 🖤",
    "نجمي هي الاستثناء الوحيد بكل القواعد",
    "لو للكون مركز، نجمي هي المركز.",
    "نجمي هي النقطة اللي عندها كل شي بيوقف",
    "نجمي إذا ابتسمت، خلص… انتهى الموضوع",
    "ما في مقارنة، لأن نجمي مابتتقارن",
    "لو خيروني ألف مرة، كل مرة رح اختار نجمي",

    "أنا بحب نجم… والباقي ما بيعنيني.",
    "وأنا بحب نجم، والباقي مجرد تفاصيل",
    "نجمي بتعرف إنها محور الكون تبعي، حتى لو عملت حالها ما بتعرف",
    "أنا بحب نجم، وبصراحة ما عندي استعداد أشرح ليش 😌",
    "كل الطرق عندي بتوصل لنجمي",
    "انا بحب نجمي محور كوني والكون كله",
    "دكتورتي 🖤",
    "فماذا أكونُ انا إذا لم تكوني 🖤",
]

# =========================================================
# الأذكار
# =========================================================

ADHKAR = [
    "🌿 سبحان الله وبحمده، سبحان الله العظيم.",
    "🤍 لا إله إلا الله وحده لا شريك له.",
    "🌿 أستغفر الله وأتوب إليه.",
    "🤍 سبحان الله، والحمد لله، والله أكبر.",
    "🌿 لا حول ولا قوة إلا بالله.",
    "🤍 اللهم صل وسلم على نبينا محمد.",
    "🌿 الحمد لله رب العالمين.",
    "🤍 سبحان الله وبحمده.",
    "🌿 أستغفر الله العظيم.",
    "🤍 حسبي الله ونعم الوكيل.",
]

# =========================================================
# أدوات مساعدة
# =========================================================

def normalize_arabic(text: str) -> str:
    text = text.strip().lower()

    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ة": "ه",
        "ى": "ي",
        "ؤ": "و",
        "ئ": "ي",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def answer_matches(user_answer: str, answers) -> bool:
    normalized = normalize_arabic(user_answer)

    for answer in answers:
        if normalized == normalize_arabic(answer):
            return True

    return False


def get_name(user):
    return user.first_name or user.username or "شخص"


def add_active_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat and chat.type in ("group", "supergroup"):
        active_chats = context.application.bot_data.setdefault(
            "active_chats",
            set()
        )
        active_chats.add(chat.id)


# =========================================================
# ذكر كل ساعة
# =========================================================

async def hourly_dhikr(context: ContextTypes.DEFAULT_TYPE):
    active_chats = context.application.bot_data.get("active_chats", set())

    if not active_chats:
        return

    dhikr = random.choice(ADHKAR)

    for chat_id in list(active_chats):
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🌿 ذكر الساعة\n\n{dhikr}"
            )
        except Exception as e:
            logging.warning(
                f"فشل إرسال الذكر إلى {chat_id}: {e}"
            )


# =========================================================
# ترحيب الأعضاء
# =========================================================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    add_active_chat(update, context)

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        members = context.chat_data.setdefault("members", {})

        members[member.id] = {
            "name": get_name(member),
            "username": member.username,
        }

        await update.message.reply_text(
            f"أهلاً وسهلاً بـ {get_name(member)} 🌷❤️"
        )


# =========================================================
# لعبة صح أو غلط
# =========================================================

async def start_true_false(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    question, answer = random.choice(TRUE_FALSE_QUESTIONS)

    context.chat_data["true_false_game"] = {
        "question": question,
        "answer": answer,
    }

    await update.message.reply_text(
        "🧠 صح أو غلط؟\n\n"
        f"❓ {question}\n\n"
        "أول شخص يجاوب صح بيفوز 🏆"
    )


async def handle_true_false(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    game = context.chat_data.get("true_false_game")

    if not game:
        return False

    answer = normalize_arabic(update.message.text)

    if answer not in ("صح", "غلط"):
        return False

    correct_answer = game["answer"]

    if answer == correct_answer:
        winner = get_name(update.effective_user)

        await update.message.reply_text(
            f"🏆 صححح!\n\n"
            f"الفائز هو: {winner} 🎉\n\n"
            f"الإجابة الصحيحة: {correct_answer} ✅"
        )

        context.chat_data.pop("true_false_game", None)

    else:
        await update.message.reply_text(
            "❌ غلط 😂 جربوا مرة تانية!"
        )

    return True


# =========================================================
# الألعاب
# =========================================================

async def play_truth(update, context):
    await update.message.reply_text(
        "🎯 صراحة:\n\n" + random.choice(TRUTHS)
    )


async def play_dare(update, context):
    await update.message.reply_text(
        "🔥 جرأة:\n\n" + random.choice(DARES)
    )


async def play_kat(update, context):
    await update.message.reply_text(
        "👀 كت:\n\n" + random.choice(KAT_QUESTIONS)
    )


async def play_question(update, context):
    await update.message.reply_text(
        "❓ سؤال:\n\n" + random.choice(GENERAL_QUESTIONS)
    )


async def play_joke(update, context):
    await update.message.reply_text(
        "😂\n\n" + random.choice(JOKES)
    )


async def play_this_or_that(update, context):
    await update.message.reply_text(
        "⚖️ هذا أو هذا؟\n\n" +
        random.choice(THIS_OR_THAT)
    )


# =========================================================
# النرد = الحظ
# =========================================================

async def play_dice(update, context):
    number = random.randint(1, 6)

    luck_messages = {
        1: "💀 حظك اليوم زفت… حتى الحظ عامل لك بلوك.",
        2: "🗑️ حظك زبالة… لا تعتمدي على الحظ اليوم 😂",
        3: "😐 حظك عادي… لا منيح ولا سيئ.",
        4: "🙂 حظك بلّش يتحسن… في أمل.",
        5: "🍀 حظك قوي اليوم… جرّبي حظك بشي حلو.",
        6: "👑🔥 حظك خرافي! اليوم الدنيا معك، استغلي الفرصة 😂",
    }

    await update.message.reply_text(
        f"🎲 طلعتلك: {number}\n\n"
        f"{luck_messages[number]}"
    )


# =========================================================
# زوجني
# =========================================================

async def marry(update, context):
    members = context.chat_data.get("members", {})

    if not members:
        await update.message.reply_text(
            "لسا ما بعرف حدا بالكروب لحتى زوجك 😂"
        )
        return

    user_id = update.effective_user.id

    possible = [
        member for member_id, member in members.items()
        if member_id != user_id
    ]

    if not possible:
        await update.message.reply_text(
            "ما في حدا غيرك حالياً 😂"
        )
        return

    partner = random.choice(possible)

    messages = [
        f"💍 تم اختيار شريك حياتك: {partner['name']} 😂❤️",
        f"💍 طبوشة قررت… نصيبك مع {partner['name']} 👀❤️",
        f"💒 مبروك! زواجك من {partner['name']} تم اعتماده 😂",
        f"❤️ الكيمياء شكلها موجودة بينك وبين {partner['name']} 👀",
        f"💍 على سنة الله ورسوله… {partner['name']} نصيبك اليوم 😂",
    ]

    await update.message.reply_text(
        random.choice(messages)
    )


# =========================================================
# نسبة الحب
# =========================================================

async def love_percentage(update, context):
    members = context.chat_data.get("members", {})

    if not members:
        await update.message.reply_text(
            "ما عندي أشخاص كفاية لأحسب النسبة 😂"
        )
        return

    user_id = update.effective_user.id

    possible = [
        member for member_id, member in members.items()
        if member_id != user_id
    ]

    if not possible:
        await update.message.reply_text(
            "لازم يكون في شخص تاني بالكروب 😂"
        )
        return

    partner = random.choice(possible)
    percentage = random.randint(0, 100)

    if percentage < 20:
        comment = "💀 العلاقة بدها معجزة 😂"
    elif percentage < 40:
        comment = "😐 في شي… بس مو كتير."
    elif percentage < 60:
        comment = "🙂 في أمل."
    elif percentage < 80:
        comment = "❤️ الوضع حلو."
    elif percentage < 95:
        comment = "🔥 في كيمياء قوية!"
    else:
        comment = "👑❤️ هاي مو نسبة… هاي فضيحة حب 😂"

    await update.message.reply_text(
        f"❤️ نسبة الحب بينك وبين {partner['name']}\n\n"
        f"💘 {percentage}%\n\n"
        f"{comment}"
    )


# =========================================================
# دين
# =========================================================

async def start_deen(update, context):
    question, answers = random.choice(DEEN_QUESTIONS)

    context.chat_data["deen_game"] = {
        "answers": answers,
        "question": question,
    }

    await update.message.reply_text(
        f"🕌 سؤال ديني:\n\n{question}"
    )


async def handle_deen_answer(update, context):
    game = context.chat_data.get("deen_game")

    if not game:
        return False

    if answer_matches(update.message.text, game["answers"]):
        await update.message.reply_text(
            "✅ إجابة صحيحة! ما شاء الله 🤍"
        )
        context.chat_data.pop("deen_game", None)
        return True

    return False


# =========================================================
# البحث عن يوتيوب
# =========================================================

async def youtube_search(update, context):
    text = update.message.text.strip()

    if not text.startswith("يوتيوب "):
        return False

    query = text[7:].strip()

    if not query:
        await update.message.reply_text(
            "اكتبي اسم الأغنية بعد كلمة يوتيوب 🎵"
        )
        return True

    search_url = (
        "https://www.youtube.com/results?search_query="
        + query.replace(" ", "+")
    )

    await update.message.reply_text(
        f"🎵 بحث يوتيوب عن:\n{query}\n\n"
        f"{search_url}"
    )

    return True


# =========================================================
# Start / Help
# =========================================================

async def start(update, context):
    add_active_chat(update, context)

    await update.message.reply_text(
        "🌷 أهلاً فيكي مع طبوشة 😂❤️\n\n"
        "الألعاب المتوفرة:\n\n"
        "🎯 صراحة\n"
        "🔥 جرأة\n"
        "👀 كت\n"
        "❓ أسئلة\n"
        "😂 نكتة\n"
        "🎲 نرد — لعبة الحظ\n"
        "🕌 دين\n"
        "🧠 صح أو غلط\n"
        "⚖️ هذا أو هذا\n"
        "💍 زوجني\n"
        "❤️ نسبة\n\n"
        "🌿 وطبوشة بتنزل ذكر كل ساعة."
    )


async def help_ar(update, context):
    await update.message.reply_text(
        "📚 أوامر طبوشة:\n\n"
        "🎯 صراحة\n"
        "🔥 جرأة\n"
        "👀 كت\n"
        "❓ أسئلة\n"
        "😂 نكتة\n"
        "🎲 نرد\n"
        "🕌 دين\n"
        "🧠 صح أو غلط\n"
        "⚖️ هذا أو هذا\n"
        "💍 زوجني\n"
        "❤️ نسبة\n"
        "🎵 يوتيوب + اسم الأغنية"
    )


# =========================================================
# المحادثة الرئيسية
# =========================================================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    add_active_chat(update, context)

    text = update.message.text.strip()
    normalized = normalize_arabic(text)

    # تسجيل العضو
    members = context.chat_data.setdefault("members", {})

    user = update.effective_user

    if user and not user.is_bot:
        members[user.id] = {
            "name": get_name(user),
            "username": user.username,
        }

    # -----------------------------------------------------
    # صح أو غلط - لازم يجي قبل أي شيء
    # -----------------------------------------------------

    if await handle_true_false(update, context):
        return

    # -----------------------------------------------------
    # إجابات الدين
    # -----------------------------------------------------

    if await handle_deen_answer(update, context):
        return

    # -----------------------------------------------------
    # تشغيل الألعاب
    # -----------------------------------------------------

    if normalized in ("صح او غلط", "صح أو غلط"):
        await start_true_false(update, context)
        return

    if normalized == "صراحه":
        await play_truth(update, context)
        return

    if normalized == "جراه":
        await play_dare(update, context)
        return

    if normalized == "كت":
        await play_kat(update, context)
        return

    if normalized in ("اسئله", "سوال", "سؤال"):
        await play_question(update, context)
        return

    if normalized in ("نكته", "نكتة"):
        await play_joke(update, context)
        return

    if normalized in ("هذا او هذا", "هذا أو هذا"):
        await play_this_or_that(update, context)
        return

    if normalized in ("نرد", "حظ"):
        await play_dice(update, context)
        return

    if normalized in ("دين", "سؤال ديني"):
        await start_deen(update, context)
        return

    if normalized in ("زوجني", "زوجيني"):
        await marry(update, context)
        return

    if normalized in ("نسبه", "نسبة"):
        await love_percentage(update, context)
        return

    # -----------------------------------------------------
    # 🫦 نجم - لا تعدلي هذا الجزء
    # -----------------------------------------------------

    if "🫦" in text:
        await update.message.reply_text(
            random.choice(LIP_REPLIES)
        )
        return

    # -----------------------------------------------------
    # بحبك
    # -----------------------------------------------------

    if normalized in ("بحبك", "انا بحبك"):
        await update.message.reply_text(
            random.choice(LOVE_YES)
        )
        return

    # -----------------------------------------------------
    # بتكرهيني
    # -----------------------------------------------------

    if normalized in ("بتكرهيني", "بتكرهيني؟"):
        await update.message.reply_text(
            random.choice(HATE_NO)
        )
        return

    # -----------------------------------------------------
    # بتحبيني
    # -----------------------------------------------------

    if normalized in ("بتحبيني", "بتحبيني؟"):
        await update.message.reply_text(
            random.choice(LOVE_YES)
        )
        return

    # -----------------------------------------------------
    # علاقة
    # -----------------------------------------------------

    if any(word in normalized for word in [
        "نرتبط",
        "نرتبط؟",
        "ارتبط",
        "علاقه"
    ]):
        await update.message.reply_text(
            random.choice(RELATIONSHIP_REPLIES)
        )
        return

    # -----------------------------------------------------
    # زواج
    # -----------------------------------------------------

    if any(word in normalized for word in [
        "تتزوجيني",
        "تزوجيني",
        "تتزوجي"
    ]):
        await update.message.reply_text(
            random.choice(MARRIAGE_REPLIES)
        )
        return

    # -----------------------------------------------------
    # بوسة
    # -----------------------------------------------------

    if "بوسيني" in normalized or "بوسه" in normalized:
        await update.message.reply_text(
            random.choice(KISS_REPLIES)
        )
        return

    # -----------------------------------------------------
    # وينك
    # -----------------------------------------------------

    if normalized in ("وينك", "وينك؟", "وين"):
        await update.message.reply_text(
            random.choice(WHERE_REPLIES)
        )
        return

    # -----------------------------------------------------
    # استغفار
    # -----------------------------------------------------

    if "استغفر الله" in normalized:
        await update.message.reply_text(
            random.choice(ISTAGHFAR_REPLIES)
        )
        return

    # -----------------------------------------------------
    # تحيات
    # -----------------------------------------------------

    greetings = [
        "مرحبا",
        "اهلا",
        "أهلا",
        "هلا",
        "هاي",
        "هيلو",
        "السلام عليكم",
    ]

    if normalized in [normalize_arabic(x) for x in greetings]:
        await update.message.reply_text(
            random.choice(GREETING_REPLIES)
        )
        return

    # -----------------------------------------------------
    # وداع
    # -----------------------------------------------------

    if normalized in (
        "باي",
        "مع السلامه",
        "تصبحون على خير",
        "تصبحي على خير",
    ):
        await update.message.reply_text(
            random.choice(BYE_REPLIES)
        )
        return

    # -----------------------------------------------------
    # طبوشة
    # -----------------------------------------------------

    if normalized == "طبوشه":
        await update.message.reply_text(
            random.choice([
                "عيوني؟ 😂",
                "نعم؟ 👀",
                "معك طبوشة 😌",
                "شو بدك مني هالمرة؟ 😂",
            ])
        )
        return

    # -----------------------------------------------------
    # يوتيوب
    # -----------------------------------------------------

    if await youtube_search(update, context):
        return


# =========================================================
# تشغيل البوت
# =========================================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "لم يتم العثور على TELEGRAM_BOT_TOKEN"
        )

    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # الأوامر
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_ar)
    )

    # أعضاء جدد
    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )

    # كل الرسائل النصية
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    # =====================================================
    # ذكر كل ساعة
    # =====================================================

    if application.job_queue is not None:
        application.job_queue.run_repeating(
            hourly_dhikr,
            interval=3600,
            first=3600
        )
    else:
        logging.warning(
            "JobQueue غير متوفر. ثبتي python-telegram-bot[job-queue]"
        )

    print("طبوشة اشتغلت ❤️")

    application.run_polling()


if __name__ == "__main__":
    main()
