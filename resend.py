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

# src_chat_name = ['solanascanner']
# target_chat_name = ['Jeffrey_E']
src_chat_name = ['solanascanner', 'solanapoolsnew',
                 'solana_tracker', 'bananagun_tracker']
target_chat_name = ['sol_broadcast_bot']

# src_chats = []
# target_chats = []
# src_chat_id = [-1002023951506, 6789, -987654, 123, -456789]
# target_chat_id = []

src_chat_id = []
target_chat_id = []
src_chats = []
target_chats = []

with TelegramClient('', api_id, api_hash) as client:
    client.start(phone=phone_number)

    # 2. 获取所有的chat_id 和 name
    chats = client.get_dialogs()
    for chat in chats:
        print(f'Chat ID: {chat.id}, Name: {chat.entity.username}')

        # 聊天频道和目标频道，分别去获取对应的id数组
        for src in src_chat_name:
            if src == chat.entity.username:
                if chat.id < 0:
                    src_chats.append(
                        {'id': int(str(chat.id)[4:]), 'name': chat.entity.username})
                else:
                    src_chats.append(
                        {'id': chat.id, 'name': chat.entity.username})
                src_chat_id.append(chat.id)
        for target in target_chat_name:
            if target == chat.entity.username:
                target_chat_id.append(chat.id)
                target_chats.append(
                    {'id': chat.id, 'name': chat.entity.username})

    print('src', src_chat_id, 'target', target_chat_id)
    print('src_chats', src_chats, 'target_chats', target_chats)

    @client.on(events.NewMessage(from_users=[int(user_id) for user_id in src_chat_id]))
    async def copyMsg(event: events.NewMessage.Event):
        original_update = event.original_update
        channel_id = original_update.message.peer_id.channel_id

        print('Received message in channel:', channel_id)

        from_name = next((item['name']
                          for item in src_chats if item['id'] == channel_id), None)

        print(from_name, 'desired_name')

        for target in target_chat_id:
            # message_content = f"  {event.message.message}"
            # await client.send_message(target, message=message_content)

            message_text = f"{from_name} " + '=' + event.message.message

            await client.send_message(target, message_text)

    client.run_until_disconnected()
