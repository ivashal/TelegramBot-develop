
from telepot.telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

class InputAnalyzer:

    def analyze(self,wrd,game,gameProcess,idleChat,startGame,sendMessage):
        if (wrd=="/startGame"):
            if game.isRunning:
                #return "You have already started the game"
                sendMessage(game.chat_id, "You have already started the game")
            else:
                game.isRunning=True
                startGame(game)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='theme1', callback_data='theme~theme1')],
                    [InlineKeyboardButton(text='theme2', callback_data='theme~theme2')]
                ])
                sendMessage(game.chat_id, "It's your move. Shoose theme:", reply_markup=keyboard)
                #return "It's your move"
        elif game.isRunning:
            #return self.gameProcess(str,chat_id,cur_game)
            sendMessage(game.chat_id, gameProcess(str,game.chat_id,game))
        else:
            #return self.idleChat()
            sendMessage(game.chat_id, idleChat())
