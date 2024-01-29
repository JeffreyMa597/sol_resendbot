from flask import Flask

app = Flask(__name__)

@app.route('/')
def run_telegram_client():
    from telethon.sync import TelegramClient, events
    from telethon.sessions import StringSession
    import os

    # all_proxy = os.environ.get('all_proxy') or ''

    # proxy = all_proxy.replace('//', '').split(':')
    # if proxy.len() > 2:
    #     proxy[2] = int(proxy[2])
    # print('proxy', proxy, all_proxy)

    #  1. 用户输入手机号码和验证码登录
    api_id = 2040
    api_hash = 'b18441a1ff607e10a989891a5462e627'
    phone_number = '+212600806448'
    username = 'eliseellon'
    session_string = ''

    # with open('session.txt', 'r') as f:
    #     session_string = f.read()

    # client = TelegramClient(StringSession(session_string),api_id, api_hash, proxy=proxy if all_proxy else None)
    # client = TelegramClient(username, api_id, api_hash)

    # with open('session.txt', 'w') as f:
    #     f.write(str(client.session.save()))

    # src_chat_name = ['solanascanner', 'solanapoolsnew', 'solana_tracker', ]
    # target_chat_name = ['Jeffrey_E']
    src_chat_name = ['solana_tracker']
    target_chat_name = ['sol_broadcast_bot']

    src_chat_id = []
    target_chat_id = []


    with TelegramClient('', api_id, api_hash) as client:
        client.start(phone=phone_number)

        # 2. 获取所有的chat_id 和 name
        chats = client.get_dialogs()
        for chat in chats:
            print(f'Chat ID: {chat.id}, Name: {chat.entity.username}')

            for src in src_chat_name:
                if src == chat.entity.username:
                    src_chat_id.append(chat.id)
            for target in target_chat_name:
                if target == chat.entity.username:
                    target_chat_id.append(chat.id)

        print('src', src_chat_id, 'target', target_chat_id)

        @client.on(events.NewMessage(from_users=[int(user_id) for user_id in src_chat_id]))
        async def copyMsg(event: events.NewMessage.Event):
            for target in target_chat_id:
                await client.send_message(target, message=event.message)

        client.run_until_disconnected()
    
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
