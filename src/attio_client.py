import requests
from typing import List, Dict, Any
from datetime import datetime
from .config import settings

class AttioClient:
    def __init__(self):
        self.base_url = "https://api.attio.com/v2"
        self.headers = {
            "Authorization": f"Bearer {settings.ATTIO_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def get_deals_with_telegram_id(self) -> List[Dict[str, Any]]:
        """Fetch all deals that have a telegram chat ID configured."""
        response = requests.get(
            f"{self.base_url}/objects/deals",
            headers=self.headers,
            params={
                "attributes": [settings.TELEGRAM_IDENTIFIER_ATTRIBUTE_ID]
            }
        )
        response.raise_for_status()
        return [
            deal for deal in response.json()["data"]
            if deal["attributes"].get(settings.TELEGRAM_IDENTIFIER_ATTRIBUTE_ID)
        ]
    
    def create_activity(self, deal_id: str, messages: List[Dict[str, Any]]) -> None:
        """Create an activity in Attio for a batch of Telegram messages."""
        if not messages:
            return
            
        # Group messages by sender
        messages_by_sender = {}
        for msg in messages:
            sender = msg["sender"]
            if sender not in messages_by_sender:
                messages_by_sender[sender] = []
            messages_by_sender[sender].append(msg["text"])
        
        # Create summary
        summary = []
        for sender, texts in messages_by_sender.items():
            msg_count = len(texts)
            summary.append(f"{sender}: {msg_count} messages")
        
        # Create activity
        activity_data = {
            "type": "telegram_conversation",
            "title": "Telegram Conversation Update",
            "description": "\n".join([
                f"Summary of Telegram conversation from {messages[0]['timestamp']} to {messages[-1]['timestamp']}",
                "",
                "Message Count by Participant:",
                *summary,
                "",
                "Latest Messages:",
                *[f"{msg['sender']}: {msg['text']}" for msg in messages[-3:]]  # Show last 3 messages
            ]),
            "deal_id": deal_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = requests.post(
            f"{self.base_url}/activities",
            headers=self.headers,
            json=activity_data
        )
        response.raise_for_status()
