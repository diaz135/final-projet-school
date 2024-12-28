from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Salon, Message
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(AsyncWebsocketConsumer):
    # Méthode pour récupérer les messages d'un salon
    async def fetch_messages(self, data):
        salon_id = data['classe']
        try:
            # Optimisation avec `select_related` pour charger les auteurs des messages
            messages = await sync_to_async(
                lambda: list(
                    Message.objects.filter(salon__classe=int(salon_id))
                    .select_related('auteur')
                    .order_by('date_add')[:20]
                )
            )()
            content = {
                'command': 'messages',
                'messages': await self.messages_to_json(messages)
            }
            await self.send_message(content)
        except Exception as e:
            await self.send_message({'error': f'Erreur lors du chargement des messages: {str(e)}'})

    # Méthode pour créer un nouveau message
    async def new_message(self, data):
        auteur = data['from']
        salon_id = data['classe']
        try:
            # Récupération des objets Salon et User
            salon_object = await sync_to_async(Salon.objects.get)(classe__id=int(salon_id))
            auteur_user = await sync_to_async(User.objects.get)(username=auteur)

            # Création du message
            message = await sync_to_async(Message.objects.create)(
                auteur=auteur_user,
                salon=salon_object,
                message=data['message']
            )
            content = {
                'command': 'new_message',
                'message': await self.message_to_json(message)
            }
            await self.send_chat_message(content)
        except ObjectDoesNotExist as e:
            await self.send_message({'error': f'Objet introuvable: {str(e)}'})
        except Exception as e:
            await self.send_message({'error': f'Erreur lors de l\'envoi du message: {str(e)}'})

    # Conversion de plusieurs messages en JSON
    async def messages_to_json(self, messages):
        return [await self.message_to_json(message) for message in messages]

    # Conversion d'un message unique en JSON
    async def message_to_json(self, message):
        try:
            # Gestion des différents types d'utilisateur et récupération de l'image
            if hasattr(message.auteur, 'student_user'):
                image = await sync_to_async(lambda: message.auteur.student_user.photo.url)()
            elif hasattr(message.auteur, 'instructor'):
                image = await sync_to_async(lambda: message.auteur.instructor.photo.url)()
            else:
                image = '/static/default_avatar.png'

            # Construction de la réponse JSON
            return {
                'auteur': await sync_to_async(lambda: message.auteur.username)(),
                'auteur_image': image,
                'message': await sync_to_async(lambda: message.message)(),
                'date_add': await sync_to_async(lambda: message.date_add.strftime("%Y-%m-%d %H:%M:%S"))()
            }
        except Exception as e:
            return {'error': f'Erreur lors de la conversion du message: {str(e)}'}

    # Dictionnaire de commandes
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    # Connexion WebSocket
    async def connect(self):
        self.salon = self.scope['url_route']['kwargs']['classe']
        self.room_group_name = f'chat_{self.salon}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Déconnexion WebSocket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Réception de messages WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')
        if command in self.commands:
            await self.commands[command](self, data)
        else:
            await self.send_message({'error': 'Commande inconnue'})

    # Envoi d'un message à tous les membres du groupe
    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Envoi direct d'un message
    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    # Gestion des événements de messages de groupe
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
