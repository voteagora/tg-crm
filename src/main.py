from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from typing import Dict, Optional
import asyncio

from .telegram_client import TelegramClient
from .attio_client import AttioClient
from .config import settings

app = FastAPI()
telegram_client = TelegramClient()
attio_client = AttioClient()
scheduler = AsyncIOScheduler()

# Store the last sync time for each chat
last_sync_times: Dict[int, datetime] = {}

async def sync_messages():
    """Sync messages from Telegram to Attio."""
    try:
        # Get all deals with Telegram IDs
        deals = attio_client.get_deals_with_telegram_id()
        
        for deal in deals:
            chat_id = int(deal["attributes"][settings.TELEGRAM_IDENTIFIER_ATTRIBUTE_ID])
            since = last_sync_times.get(chat_id, datetime.now() - timedelta(hours=1))
            
            # Get messages from Telegram
            messages = await telegram_client.get_messages(chat_id, since)
            
            if messages:
                # Create activity in Attio
                attio_client.create_activity(deal["id"], messages)
                last_sync_times[chat_id] = datetime.now()
                
    except Exception as e:
        print(f"Error during sync: {str(e)}")

@app.on_event("startup")
async def startup():
    # Start the scheduler
    scheduler.add_job(sync_messages, 'interval', minutes=settings.BATCH_INTERVAL_MINUTES)
    scheduler.start()

@app.post("/auth/phone")
async def auth_phone(phone: str):
    """Start Telegram authentication process."""
    try:
        await telegram_client.authorize(phone)
        return {"message": "Verification code sent to your Telegram account"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/code")
async def auth_code(code: str):
    """Complete Telegram authentication with verification code."""
    try:
        await telegram_client.authorize(None, code)
        return {"message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
