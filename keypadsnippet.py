ctx.user_data['input_buffer'] = ""
    # Numeric keypad with an "Enter" button (3x4 grid)
    numeric_keyboard = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['0', '⌫ Delete', '✅ Enter']  # Added Delete and Enter buttons
    ]
    reply_markup = ReplyKeyboardMarkup(numeric_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await upd.message.reply_text(
  "🔢 Enter a number and press **✅ Enter**:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def number_of_teams(buffer):
    try:
        number_of_teams = int(buffer)
        if number_of_teams < 2:
            raise ValueError("Number of teams must be at least 2.")
    except ValueError as e:
        return str(e)
    teams = [f"Team {i+1}" for i in range(number_of_teams)]
    print(f"Teams: {teams}")
    return teams
    
async def handle_input(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_input = upd.message.text
    if user_input == '⌫ Delete':
        await upd.message.reply_text("Input deleted.")
        return
    elif user_input == '✅ Enter':
        buffer = ctx.user_data.get('input_buffer', '')
        if buffer:
            number_of_teams(buffer)
        
        await upd.message.reply_text(f"You entered: {ctx.user_data.get('input_buffer', 'No input')}")
        return
    else:
        #ctx.user_data['input'] = user_input  # Store the input in user data
        #await upd.message.reply_text(f"Current input: {user_input}")