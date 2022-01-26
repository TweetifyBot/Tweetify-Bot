#Made for getting notification from telegram bot when a user tweets or reply
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from server import update_username_to_the_data_base as update_db
from server import get_chat_id_from_the_data_base as get_db
import os

#Bot API key 
API_key = "Enter your bot APi key"
username_list = get_db()

updater = Updater(API_key, use_context=True)
PORT = int(os.environ.get('PORT', 5000))
#getting the data from the data base if the bot is stopped

telegram_token = API_key
#starting the bot
def start(update: Update, context: CallbackContext):

    #checking whether the telegram chat _id is already there
    if user_chat_id(update) in username_list.keys():
        pass
    else:
        username_list[user_chat_id(update)] = []

    update.message.reply_text("""HELLO!
I am a telegram bot used to notify you when a user name of your choice tweets or replies to a tweet.
/help -> Helps to choose commands.
/usernameList -> Shows the list of usernames.
/addUsername <username> -> Adds username to notify you.
/removeUsername <username> -> remove username to not to notify you.""")

#help command to display the commands of the bot
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""/help -> Helps to choose commands.
/usernameList -> Shows the list of usernames.
/addUsername <username> -> Adds username to notify you.
/removeUsername <username> -> remove username to not to notify you.""")

#getting chat id and returning it
def user_chat_id(update: Update):
	user = update.message.chat_id
	return str(user)

#displaying the chat id's username list
def username_list_reply(update: Update, context: CallbackContext):
    username_list 	
    username_list_str = ""
    
    if username_list[user_chat_id(update)] == []:
        update.message.reply_text("""There is no username in the list.
        
If you need any help /help.""")

    else:
        twitter_username_list = username_list.get(user_chat_id(update))

        for usr in twitter_username_list:
            username_list_str += f"{usr}\n"

        update.message.reply_text(f"""The usernames are
{username_list_str}""")

#command to add username to the list
def add_username(update: Update, context: CallbackContext):
    global username_list 
    username = str(update.message.text).split(" ")[1].strip()
    
    #for adding "@" symbol before if the telegram user forgot to add
    if username[0] != "@":
        username = "@" + username

    #verifying whether the given username y the user is there in twitter. if the username is there it will return true else false
    verification_state = verify_username(username)

    #checking whether the user name is already there in the list
    if username in username_list[user_chat_id(update)]:
        update.message.reply_text(f"""The username {username} is already there in the list.
        
if you want any help /help.""")

    elif verification_state == True:
        username_list[user_chat_id(update)].append(username)

        update_db(user_chat_id(update), username_list[user_chat_id(update)])

        update.message.reply_text(f"""The user name is successfully added to the list of usernames.
if you want any help /help.
https://www.twitter.com/{username}""")

    else:
        update.message.reply_text("""The username is not found in twitter
Make sure you have typed the correct letters(lower or upper), numbers and special characters.
If you want any help /help.
If you still have error contact the developers @Rakesh or @Arudhran""")

def verify_username(twitter_username):
    #verify whether the given username by the user is there in twitter by using API
    return True

#command to remove username form the list
def remove_username(update: Update, context: CallbackContext):
    global username_list 
    username = str(update.message.text).split(" ")[1].strip()

    if username[0] != "@":
        username = "@" + username

    #if the list of chat id is empty
    if username_list[user_chat_id(update)] == []:
        update.message.reply_text("""There is no username in the username list to remove.
If you want any help /help.""")

    elif username in username_list[user_chat_id(update)]:
            username_list[user_chat_id(update)].remove(username)

            update_db(user_chat_id(update), username_list[user_chat_id(update)])

            update.message.reply_text("""The username is successfully removed from the list.
If you want any help /help.""")
    #if there is no username in the list as chat id specified
    else:
        update.message.reply_text(f"""There is no username as {username} in the username list.
If youwant any help /help.
If you want to see the list of usernames /usernameList""")

#adding handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('usernameList', username_list_reply))
updater.dispatcher.add_handler(CommandHandler('addUsername', add_username))
updater.dispatcher.add_handler(CommandHandler('removeUsername', remove_username))

#starting the bot and to tell the bot for seeking for commands
updater.start_webhook(listen="0.0.0.0",port=int(PORT), url_path=telegram_token)
updater.bot.setWebhook('https://YourHerokuAppName.herokuapp.com/' + telegram_token)

#This code was made by Arudhran:-  https://github.com/ArudhranPK/   and     Rakesh:- https://github.com/ARKS-INDUSTRY/
