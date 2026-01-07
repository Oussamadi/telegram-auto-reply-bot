from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = "8242893940:AAGQzM2HfFtJkpdO2R5hI_J7Ao1ins41AzM"
ADMIN_ID = 1764395818  # ← ضع Telegram ID الحقيقي هنا

# نخزن من يريد مراسلة المشرف
waiting_for_admin_message = set()

# ===== start + الأزرار =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["👤 : من أنت؟", "💰 الأسعار"],
        ["🕒 أوقات العمل", "📞0669272484  تواصل معنا"],
        ["👨‍💼 راسل المشرف الآن", "❓ مساعدة"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "أهلاً وسهلاً 👋😊\n"
        "أنا المساعد الآلي 🤖\n"
        "اختر من الأزرار أو اكتب سؤالك مباشرة 👇",
        reply_markup=reply_markup
    )

# ===== الرسائل =====
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text_lower = text.lower()
    user = update.message.from_user
    user_id = user.id

    # ===== إذا كان ينتظر رسالة للمشرف =====
    if user_id in waiting_for_admin_message:
        notify_text = (
            "📩 رسالة مباشرة للمشرف\n\n"
            f"👤 الاسم: {user.first_name}\n"
            f"🔗 المستخدم: @{user.username}\n"
            f"🆔 ID: {user.id}\n\n"
            f"💬 الرسالة:\n{text}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notify_text
        )

        waiting_for_admin_message.remove(user_id)

        await update.message.reply_text(
            "✅ تم إرسال رسالتك للمشرف بنجاح\n"
            "سيتم الرد عليك في أقرب وقت 🤝"
        )
        return

    # ===== زر مراسلة المشرف =====
    if "راسل المشرف" in text_lower:
        waiting_for_admin_message.add(user_id)
        await update.message.reply_text(
            "👨‍💼 اكتب رسالتك الآن\n"
            "وسيتم إرسالها مباشرة إلى المشرف ✍️"
        )
        return

    # ===== إشعار عادي للمشرف =====
    notify_text = (
        "📨 رسالة جديدة للبوت\n\n"
        f"👤 {user.first_name} (@{user.username})\n"
        f"🆔 {user.id}\n\n"
        f"💬 {text}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=notify_text
    )

    # ===== الردود الطبيعية =====
    if any(w in text_lower for w in ["السلام", "السلام عليكم", "سلام"]):
        reply = "وعليكم السلام ورحمة الله 🌸 كيف نقدر نعاونك؟"

    elif any(w in text_lower for w in ["مرحبا", "أهلا", "hello", "hi"]):
        reply = "مرحباً 👋 نورتنا!"

    elif "كيف حالك" in text_lower:
        reply = "الحمد لله بخير 😊 شكراً لسؤالك"

    elif "من أنت" in text_lower:
        reply = "أنا بوت رد تلقائي 🤖 نساعدك ونوصلك بالمشرف عند الحاجة"

    elif "الأسعار" in text_lower:
        reply = "💰 الأسعار تختلف حسب الخدمة، اكتب التفاصيل وسنوضح لك"

    elif "أوقات" in text_lower:
        reply = "🕒 من السبت إلى الخميس\n09:00 ➜ 17:00"

    elif "تواصل" in text_lower:
        reply = "📞 يمكنك مراسلتنا هنا أو الضغط على (راسل المشرف)"

    elif "مساعدة" in text_lower:
        reply = "❓ اكتب سؤالك أو اختر زر مناسب وسنساعدك فورًا"

    elif any(w in text_lower for w in ["شكرا", "شكراً", "merci", "thanks"]):
        reply = "العفو 🌷 يسعدنا خدمتك دائمًا"

    else:
        reply = "وصلت رسالتك 👍 سنرد عليك قريبًا بإذن الله"

    await update.message.reply_text(reply)

# ===== تشغيل =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

print("🤖 البوت يعمل الآن...")
app.run_polling()
