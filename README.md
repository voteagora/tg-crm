# Telegram-Attio Integration

This service integrates Telegram conversations with Attio CRM, automatically syncing messages as activities in Attio deals.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
ATTIO_API_KEY=your_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/tg_crm
```

3. Initialize the database:
```bash
alembic upgrade head
```

4. Start the service:
```bash
uvicorn src.main:app --reload
```

## User Guide

### Linking Telegram Chats to Attio Deals

1. In Telegram Desktop:
   - Open Settings > Advanced > Developer Options
   - Enable "Show Chat ID in Chat Info"
   - Right-click on any chat and select "Copy Chat ID"

2. In Attio:
   - Open the deal you want to link
   - Find the "Telegram Chat ID" field
   - Paste the copied Chat ID

The service will automatically start tracking messages for any deal with a valid Telegram chat ID.

### Authentication

On first run, you'll need to:
1. Visit `http://localhost:8000/auth`
2. Enter your Telegram phone number
3. Enter the verification code sent to your Telegram account

## Architecture

- Uses TDLib for Telegram integration (no bot required)
- Batches messages hourly to create consolidated activities in Attio
- Stores minimal mapping data between Telegram chats and Attio deals
