

class Game:

    isRunning=False
    ai_score=0
    user_score=0
    moves=0
    chat_id = ""

    def __init__(self,chat_id):
        self.chat_id=str(chat_id)