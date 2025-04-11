import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler, ConversationHandler

TELEGRAM_BOT_TOKEN = "7667383218:AAEZWdnov2hwLAkPECQMPSuaXpESwuY9fdI"
CHAT_ID = "411636236"

NAME, AGE, FEEDBACK = range(3)

async def start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await upd.message.reply_text("Hello World emoji!")

async def echo(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_message = upd.message.text
    await upd.message.reply_text(f"Echo: {user_message}")
    

async def start_survey (upd: Update, ctx):
    await upd.message.reply_text("Please enter your name:")
    return NAME

async def get_name(upd: Update, ctx):
    ctx.user_data['name'] = upd.message.text
    print (ctx.user_data['name'])
    await upd.message.reply_text(f"Hi, {ctx.user_data['name']}, Please enter your age:")
    return AGE
    
async def get_age (upd: Update, ctx):
    ctx.user_data['age'] = upd.message.text
    print (ctx.user_data)
    await upd.message.reply_text(f"Hi, {ctx.user_data['name']}, Please enter your feedback:")
    return FEEDBACK
    

async def get_feedback(update: Update, ctx):
    ctx.user_data['feedback'] = update.message.text
    print("Context contents:")
    print("Args:", ctx.args)
    print("Chat Data:", ctx.chat_data)
    print("User Data:", ctx.user_data)
    print("Bot:", ctx.bot)
    print("Update:", update)
    await update.message.reply_text(
        f"Thanks, {ctx.user_data['name']} (Age: {ctx.user_data['age']})!\n"
        f"Feedback: {ctx.user_data['feedback']}"
    )
    return ConversationHandler.END


def main(): # Not using async for main function
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    # commented echo so that i can test the survey functionality
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('survey', start_survey)],
        states={
            NAME: [MessageHandler(filters.TEXT, get_name)],
            AGE: [MessageHandler(filters.TEXT, get_age)],
            FEEDBACK: [MessageHandler(filters.TEXT , get_feedback)]
        },
        #fallbacks=[CommandHandler("cancel", lambda update, context: update.message.reply_text("Survey cancelled."))],
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    application.add_handler(start_handler)
    #application.add_handler(echo_handler)
    application.add_handler(conv_handler)

    print ("Bot is started and running...") 
    application.run_polling()


if __name__ == "__main__":
    main()
    