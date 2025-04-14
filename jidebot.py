import asyncio, random
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler, ConversationHandler

TELEGRAM_BOT_TOKEN = "7667383218:AAEZWdnov2hwLAkPECQMPSuaXpESwuY9fdI"
CHAT_ID = "411636236"

async def start(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await upd.message.reply_text("Enter number of teams: (Multiples of 4) ")

def number_of_teams(teams):
    teams_list = [f"Team {i+1}" for i in range(teams)]
    return teams_list   

def simulate(team1, team2):
    winner = random.choice ([team1, team2])
    return winner

def pair (teams):
    fixtures = {}
    current_round = 1
    current_teams = teams.copy()
    while len(current_teams) > 1 :
        round_name =  (f"Round {current_round}")
        fixtures[round_name] = []
        next_round_teams = []
        print (random.shuffle(current_teams))
        for i in range(0,len(current_teams), 2):
            if i+1 < len(current_teams):
                team1, team2 = current_teams[i], current_teams[i+1]
                winner = simulate(team1, team2)
                fixtures[round_name].append(f"{team1} vs {team2} -> Winner: {winner}")
                next_round_teams.append(winner)
            else:
                next_round_teams.append(current_teams[i])
                fixtures[round_name].append(f"{current_teams[i]} has a bye.")
        current_teams = next_round_teams
        current_round += 1
    
    if current_teams:
        fixtures["Champion"] = current_teams[0]
        return fixtures
        

async def handle_input(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_input = upd.message.text
    ctx.user_data['user_input'] = user_input  # Store the input in user data
    print (ctx.user_data['user_input'])
    if user_input:
        if user_input.isdigit():
        
            user_input = int(user_input)
            if user_input % 4 != 0:
                await upd.message.reply_text("Please enter a number that is a multiple of 4.")
            else:
                teams = number_of_teams(user_input)
                print (f"Teams: {teams}")
                ctx.user_data['teams'] = teams
                await upd.message.reply_text(f"Teams: {teams}")
                print (ctx.user_data['teams'])
    tournament = pair(teams)
    print(tournament)
    for round_name, matches in tournament.items():
        await upd.message.reply_text(f"{round_name}:")
        if isinstance(matches,list):
            for match in matches:
                await upd.message.reply_text(match)
                await asyncio.sleep(1) # Optional: Add a delay between messages
        else:
            await upd.message.reply_text(f"Trophy Winner: {matches}" )
                
                
            
            

        
 
        
     
         
        
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    # commented echo so that i can test the survey functionality
    input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input)

    application.add_handler(start_handler)
    application.add_handler(input_handler)

    print ("Jide Bot started.")
    application.run_polling()
    
    
    
if __name__ == "__main__":
    main()