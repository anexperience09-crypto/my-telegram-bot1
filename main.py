import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# 1. عند ضغط الطالب على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton(text="مشاركة رقم الهاتف للتحقق 📱", request_contact=True)
    reply_keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)
    
    welcome_text = (
        "🎓 **مرحباً بك في بوت الخدمات الجامعية الشامل!**\n\n"
        "يرجى الضغط على الزر أدناه لمشاركة رقم هاتفك للتحقق من الحساب والبدء في استخدام البوت."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_keyboard)

# 2. استقبال رقم الهاتف وعرض القائمة الرئيسية بالأزرار الشفافة
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    
    inline_keyboard = [
        [
            InlineKeyboardButton("📚 الملازم والملخصات", callback_data="pdf_files"),
            InlineKeyboardButton("📝 أسئلة الامتحانات", callback_data="exams")
        ],
        [
            InlineKeyboardButton("🧮 حاسبة المعدل التراكمي", callback_data="gpa_calc"),
            InlineKeyboardButton("📢 إعلانات القسم", callback_data="news")
        ],
        [
            InlineKeyboardButton("👨‍💻 الدعم الفني والمساعدة", url="https://t.me/your_username")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    await update.message.reply_text(
        f"✅ **تم التحقق بنجاح!**\nمرحباً بك، اختر الخدمة التي تحتاجها من القائمة أدناه:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# 3. التفاعل مع الضغط على الأزرار الشفافة
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "pdf_files":
        sub_keyboard = [
            [InlineKeyboardButton("المرحلة الأولى", callback_data="stage_1"), InlineKeyboardButton("المرحلة الثانية", callback_data="stage_2")],
            [InlineKeyboardButton("المرحلة الثالثة", callback_data="stage_3"), InlineKeyboardButton("المرحلة الرابعة", callback_data="stage_4")],
            [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("اختر مرحلتك الدراسية:", reply_markup=InlineKeyboardMarkup(sub_keyboard))
        
    elif query.data == "gpa_calc":
        await query.edit_message_text("🧮 **حاسبة المعدل:** أرسل درجاتك وعدد الوحدات لحساب معدلك التراكمي.")

    elif query.data == "main_menu":
        await handle_contact(update, context)

# تشغيل البوت مع حماية التوكن
if __name__ == '__main__':
    request_settings = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    
    # هنا جعلنا البوت يقرأ التوكن من إعدادات السيرفر وليس من الكود مباشرة للحماية
    MY_TOKEN = os.environ.get("BOT_TOKEN")
    
    app = ApplicationBuilder().token(MY_TOKEN).request(request_settings).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(CallbackQueryHandler(button_click))
    
    app.run_polling()
