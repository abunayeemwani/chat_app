import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Message, Thread, Message

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])

        if received_data.get('data_type') == 'user':
            user_id = received_data.get('user_id')
            user = await self.get_user(user_id)
            user_image = user.image
            user_full_name = user.first_name + " " + user.last_name

            thread = await self.get_user_thread(self.scope['user'], user)
            if thread is not None:
                messages = await self.get_messages(thread)
            else:
                messages = []

            response = {
                'id':user_id,
                'image': str(user_image),
                'name': user_full_name,
                'messages': messages,
                'data_type': "user"
            }

            await self.send(
                {
                    'type': 'websocket.send',
                    'text': json.dumps(response)
                }
            )
        elif received_data.get('data_type') == 'message':
            message = received_data.get('message')
            sent_by = await self.get_user(received_data.get('sent_by'))
            send_to = await self.get_user(received_data.get('send_to'))
            thread = await self.get_or_create_thread(sent_by, send_to)

            if thread is not None:
                await self.create_new_message(message, sent_by, thread)

            send_to_id = received_data.get('send_to')
            other_user_chat_room = f'user_chatroom_{send_to_id}'
            self_user = self.scope['user']
            response = {
                'message': message,
                'sent_by': self_user.id,
                'data_type': "message"
            }

            await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type': 'message',
                    'text': json.dumps(response)
                }
            )

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'message',
                    'text': json.dumps(response)
                }
            )

    async def websocket_disconnect(self, event):
        print('Disconnect', event)

    
    
    
    async def message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    
    
    
    @database_sync_to_async
    def get_messages(self, thread):
        messages = [[message.user.id, message.message, str(message.date)] for message in Message.objects.filter(thread = thread)]
        return messages

    
    
    
    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.filter(id = user_id)
        if user.exists():
            user = user.first()
        else:
            user = None
        return user

    
    
    
    @database_sync_to_async
    def get_or_create_thread(self, user1, user2):
        thread = Thread.objects.get_thread(user1=user1, user2=user2)
        if thread.exists():
            thread = thread.first()
        else:
            if user1 is not None and  user2 is not None:
                Thread.objects.create(first_user=user1, second_user=user2)
                thread = Thread.objects.get_thread(user1=user1, user2=user2).first()
            else:
                thread = None
        return thread

    
    
    
    @database_sync_to_async
    def get_user_thread(self, user1, user2):
        thread = Thread.objects.get_thread(user1=user1, user2=user2)
        if thread.exists():
            thread = thread.first()
        else:
            thread = None
        return thread

    
    
    
    @database_sync_to_async
    def create_new_message(self, message, sent_by, thread):
        Message.objects.create(message=message, user=sent_by, thread=thread)