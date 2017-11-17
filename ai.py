import dbInteraction
import utility
import genMod as gm
import game
import inputAnalyzer as ia
import telebot

class AI():
    db = dbInteraction.DBInteraction()
    evo=gm.Evolution()
    uc=utility.UtilityCalc(evo)
    games=[]


    #isGameStarted=False

    def startGame(self,game):
        #self.isGameStarted=True

        # for i in range(len(missingKeywords)):
        game.isRunning = True
        self.db.deleteUsedWords()

    def closeGame(self,res,game):
        #self.isGameStarted=False
        game.isRunning=False
        self.evo.setFitness(res)
        self.games.remove(game)

    def __init__(self):
        self.db.deleteUsedWords()

    def tupleToString(self,tup):
        used = ""
        for elem in tup:
            if elem is None:
                break
            else:
                used += "'" + elem[0] + "', "
        return used[:-2]

    def IsUsed(self,wrd,chat_id):
        tup=self.db.getUsedWords(chat_id)
        for elem in tup:
            if elem[0]==wrd.upper():
                return True
        return False

    def answer(self, str,chat_id,sendMessage):
        cur_game=None
        for i in range(0,len(self.games)):
            if self.games[i].chat_id==chat_id:
                cur_game=self.games[i]
        if cur_game is None:
            self.games.append(game.Game(chat_id))
            cur_game=self.games[-1]
        analyzer=ia.InputAnalyzer()
        analyzer.analyze(str,cur_game,self.gameProcess,self.idleChat,self.startGame,sendMessage)
        '''
        if (str=="/startGame"):
            if cur_game.isRunning:
                return "You have already started the game"
            else:
                cur_game.isRunning=True
                self.startGame(cur_game)
                sendMessage(chat_id,"It's your move")
                #return "It's your move"
        if cur_game.isRunning:
            #return self.gameProcess(str,chat_id,cur_game)
            sendMessage(chat_id, self.gameProcess(str,chat_id,cur_game))
        else:
            #return self.idleChat()
            sendMessage(chat_id, self.idleChat())
        '''

    def idleChat(self):
        return "Game isn't started"

    def gameProcess(self,str,chat_id,game):
        if self.IsUsed(str,chat_id):
            answer = "That word have already been used"
            return answer
        self.db.addUsedWord(str, chat_id)
        answer=self.makeDecision(str,chat_id)
        if answer is None:
            answer = "Have lost"
            self.closeGame(0,game)
        else:
            self.db.addUsedWord(answer, chat_id)
        return answer

    def makeDecision(self,word,chat_id):
        self.uc.actions.clear()
        self.uc.addActions(chat_id, word)
        res=self.uc.getFittest()
        return res

    def __exit__(self, exception_type, exception_value, traceback):
        pass
