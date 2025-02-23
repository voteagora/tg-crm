from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timedelta
from tdlib import Client
from .config import settings

class TelegramClient:
    def __init__(self):
        self.client = Client({
            'api_id': settings.TELEGRAM_API_ID,
            'api_hash': settings.TELEGRAM_API_HASH,
            'database_directory': 'tdlib',
            'files_directory': 'tdlib_files'
        })
        self._authorized = False
        
    async def authorize(self, phone: str, code: Optional[str] = None):
        """Handle Telegram authorization flow."""
        if not self._authorized:
            await self.client.send({
                '@type': 'setAuthenticationPhoneNumber',
                'phone_number': phone
            })
            
            if code:
                await self.client.send({
                    '@type': 'checkAuthenticationCode',
                    'code': code
                })
                self._authorized = True
    
    async def get_messages(self, chat_id: int, since: datetime) -> List[Dict]:
        """Fetch messages from a specific chat since given timestamp."""
        messages = []
        
        # Get chat info first
        chat = await self.client.send({
            '@type': 'getChat',
            'chat_id': chat_id
        })
        
        # Get messages
        result = await self.client.send({
            '@type': 'getChatHistory',
            'chat_id': chat_id,
            'limit': 100,  # Adjust based on needs
            'from_message_id': 0,
            'offset': 0,
            'only_local': False
        })
        
        for msg in result['messages']:
            msg_time = datetime.fromtimestamp(msg['date'])
            if msg_time < since:
                break
                
            if 'content' in msg and 'text' in msg['content']:
                sender = await self._get_sender_name(msg['sender_id'])
                messages.append({
                    'sender': sender,
                    'text': msg['content']['text']['text'],
                    'timestamp': msg_time.isoformat()
                })
        
        return messages
    
    async def _get_sender_name(self, sender_id: Dict) -> str:
        """Get sender name from sender ID."""
        if sender_id['@type'] == 'messageSenderUser':
            user = await self.client.send({
                '@type': 'getUser',
                'user_id': sender_id['user_id']
            })
            return f"{user['first_name']} {user.get('last_name', '')}"
        elif sender_id['@type'] == 'messageSenderChat':
            chat = await self.client.send({
                '@type': 'getChat',
                'chat_id': sender_id['chat_id']
            })
            return chat['title']
        return "Unknown"
