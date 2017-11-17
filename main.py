import telepot.telepot as tp
import ai
import state
from os import environ

TOKEN = environ['TOKEN']
bot = tp.Bot(TOKEN)

if not state.local:
    import os
    from flask import Flask, request
    from telepot.telepot.loop import OrderedWebhook


    PORT = os.environ['PORT']
    AI = ai.AI()



    def handle(msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        if content_type == 'text':
            answer = AI.answer(msg['text'], str(chat_id),bot.sendMessage)
            # bot.sendMessage(chat_id, answer)



    app = Flask(__name__)

    webhook = OrderedWebhook(bot, {'chat': handle})


    @app.route('/bot' + TOKEN, methods=['GET', 'POST'])
    def pass_update():
        webhook.feed(request.data)
        return 'OK'


    if __name__ == '__main__':
        try:
            bot.setWebhook('sinmo.herokuapp.com/bot' + TOKEN)
        # Sometimes it would raise this error, but webhook still set successfully.
        except tp.exception.TooManyRequestsError:
            pass

        webhook.run_as_thread()
        app.run(host='0.0.0.0', port=int(PORT))

else:
    import time
    import requests as rq
    from telepot.telepot.loop import MessageLoop

    AI = ai.AI()
    response = rq.get("https://api.telegram.org/bot" + TOKEN + "/setWebhook")
    print(response.content)


    def handle(msg):
        content_type, chat_type, chat_id = tp.glance(msg)
        if content_type == 'text':
            answer = AI.answer(msg['text'], str(chat_id),bot.sendMessage)
            # answer = msg['text']
            #bot.sendMessage(chat_id, answer)


    def on_callback_query(msg):
        query_id, from_id, query_data = tp.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)
        if query_data[:query_data.find('~')] == 'theme':
            bot.answerCallbackQuery(query_id, text='Got it, your theme is ' + query_data[query_data.find('~')+1:])



    MessageLoop(bot, { 'chat':handle,  'callback_query' : on_callback_query}).run_as_thread()
    print('Listening ...')

    while (1):
        time.sleep(10)
