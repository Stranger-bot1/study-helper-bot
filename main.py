import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

# States
SELECTING_CATEGORY, SELECTING_CLASS, SELECTING_SECTION_CLASS = range(3)

# Links for each class and section
CLASS_LINKS = {
    'books': {
        '9': 'https://flameurl.com/class9books',
        '10': 'https://flameurl.com/class10books',
        '11': 'https://flameurl.com/class11books',
        '12': 'https://flameurl.com/class12books'
    },
    'pyq': {
        '9': 'https://flameurl.com/class9pyq',
        '10': 'https://flameurl.com/class10pyq',
        '11': 'https://linkpays.in/class11pyq',
        '12': 'https://linkpays.in/class12pyq'
    },
    'batches': {
        '9': 'https://t.me/BATCHESSSSS/4',
        '10': 'https://t.me/+x1KH0A9njt81N2U1',
        '11': 'https://linkpays.in/class11batches',
        '12': 'https://linkpays.in/class12batches'
    },
    'premium': {
        '9': 'https://t.me/+givaZUxyQLxjZTA1',
        '10': 'https://t.me/+givaZUxyQLxjZTA1',
        '11': 'https://linkpays.in/class11premiumbooks',
        '12': 'https://linkpays.in/class12premiumbooks'
    },
    'notes': {
        '9': 'https://linkpays.in/class9notes',
        '10': 'https://flameurl.com/class10notes',
        '11': 'https://linkpays.in/class11notes',
        '12': 'https://linkpays.in/class12notes'
    }
}

# Utility function to check if a link is valid
def is_valid_link(link):
    return link and "yourlink" not in link and not ("linkpays.in" in link and link.endswith("/"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 NCERT Books", callback_data='section_books')],
        [InlineKeyboardButton("📚 Previous Year Questions (PYQ)", callback_data='section_pyq')],
        [InlineKeyboardButton("👨‍🏫 Batches", callback_data='section_batches')],
        [InlineKeyboardButton("📗 Premium Books", callback_data='section_premium')],
        [InlineKeyboardButton("📝 Notes", callback_data='section_notes')],
        [InlineKeyboardButton("🎓 Premium Courses", callback_data='premium_courses')],
        [InlineKeyboardButton("💬 Help & Suggestions", callback_data='help')]
    ]
    await update.message.reply_text(
        "👋 Welcome to the Study Helper Bot!\n\nThis bot can provide:\n"
        "✅ NCERT Books (with class-wise selection)\n"
        "✅ Previous Year Questions (PYQ)\n"
        "✅ Batches (class-wise)\n"
        "✅ Premium Books (class-wise)\n"
        "✅ Notes (class-wise)\n"
        "✅ Help & Suggestions\n\n"
        "What are you looking for?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_CATEGORY

# Premium Courses direct post
async def premium_courses_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    link = "https://t.me/+KdEZFQH3miEyZTc1"
    if not is_valid_link(link):
        await query.edit_message_text("🚧 Sorry, this content is coming soon!")
    else:
        await query.edit_message_text(
            "🎓 *Premium Courses* 🚀\n\n"
            f"✅ Here is your premium course link: {link}\n\n"
            "🌟 Aim high, stay consistent, and make the most of this journey!",
            parse_mode="Markdown"
        )

    return await ask_more(query)

# Handle section selection
async def section_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    section = query.data.replace("section_", "")
    context.user_data['section'] = section

    await query.edit_message_text(
        f"📚 You selected {section.replace('_', ' ').title()} Section. Now select your class:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Class 9", callback_data='class_9')],
            [InlineKeyboardButton("Class 10", callback_data='class_10')],
            [InlineKeyboardButton("Class 11", callback_data='class_11')],
            [InlineKeyboardButton("Class 12", callback_data='class_12')]
        ])
    )
    return SELECTING_SECTION_CLASS

# Class selected
async def class_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_class = query.data.replace("class_", "")
    section = context.user_data.get('section')

    link = CLASS_LINKS.get(section, {}).get(selected_class)

    if not is_valid_link(link):
        await query.edit_message_text("🚧 Sorry, this content is coming soon!")
    else:
        message = f"📚 You selected {section.replace('_', ' ').title()} for Class {selected_class}!\n\n"
        if section == 'pyq' and selected_class == '9':
            message += "🙏 Special thanks to *Digraj Sir* for this amazing material!\n\n"
        message += f"✅ Here is your study material link: {link}\n\n"
        message += "💪 Keep going! You're doing great. Every small step leads to success."
        await query.edit_message_text(message, parse_mode="Markdown")

    return await ask_more(query)

# Ask to restart
async def ask_more(query):
    keyboard = [
        [InlineKeyboardButton("🔁 Start Again", callback_data='restart')],
        [InlineKeyboardButton("💬 Help & Suggestions", callback_data='help')]
    ]
    await query.message.reply_text(
        "Do you need more study material?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SELECTING_CATEGORY

# Help handler
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💡 Help & Suggestions:\n\n"
        "📌 If you face any issue or want to suggest something, just drop a message to our admin.\n"
        "📨 @youradminusername\n\n"
        "🔁 Click below to start again.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Start Again", callback_data='restart')]
        ])
    )
    return SELECTING_CATEGORY

# Restart
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    return await start(query, context)

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled. Type /start anytime to begin again.")
    return ConversationHandler.END

# Main
async def main():
    TOKEN = "7803895531:AAGIbvMUKX3eVOHxwTm6oB0v2m_8ovpBYX8"
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start)
        ],
        states={
            SELECTING_CATEGORY: [
                CallbackQueryHandler(premium_courses_handler, pattern="^premium_courses$"),
                CallbackQueryHandler(section_handler, pattern="^section_.*$"),
                CallbackQueryHandler(help_handler, pattern="^help$"),
                CallbackQueryHandler(restart, pattern="^restart$")
            ],
            SELECTING_SECTION_CLASS: [
                CallbackQueryHandler(class_selected, pattern="^class_\\d+$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("🚀 Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
