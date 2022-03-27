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
        print("Received:", event)
        received_data = json.loads(event['text'])

        print("Data:", received_data)


        message = received_data.get('message')
        sent_by = await self.get_user(received_data.get('sent_by'))
        send_to = await self.get_user(received_data.get('send_to'))
        thread = await self.get_thread(received_data.get('thread_id'))

        await self.create_new_message(message, sent_by, thread)

        send_to_id = received_data.get('send_to')
        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message': message,
            'sent_by': self_user.id,
            'thread_id': received_data.get('thread_id')
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
        print('Message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.filter(id = user_id)
        if user.exists():
            user = user.first()
        else:
            user = None
        return user

    @database_sync_to_async
    def get_thread(self, thread_id):
        thread = Thread.objects.filter(id = thread_id)
        if thread.exists():
            thread = thread.first()
        else:
            thread = None
        return thread

    @database_sync_to_async
    def create_new_message(self, message, sent_by, thread):
        print(f"New message created with message: {message}, user: {sent_by} and thread: {thread}")
        Message.objects.create(message=message, user=sent_by, thread=thread)