# Deploying to Railway.com

This guide walks you through deploying the Telegram-Attio integration on Railway.com.

## Prerequisites

1. A Railway.com account
2. Git installed on your local machine
3. Railway CLI (optional)

## Step 1: Initial Setup

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

2. Install Railway CLI (optional):
```bash
npm i -g @railway/cli
railway login
```

## Step 2: Create Railway Project

1. Go to [Railway.com](https://railway.com)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Click "Deploy Now"

## Step 3: Configure Services

### PostgreSQL Database

1. Click "New Service" in your Railway project
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance
4. The `DATABASE_URL` will be automatically added to your environment variables

### Environment Variables

Add the following variables in Railway's dashboard (Settings → Environment Variables):

```
ATTIO_API_KEY=your_attio_api_key
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
BATCH_INTERVAL_MINUTES=60
```

## Step 4: TDLib Setup

Since Railway uses containerized deployments, we need to ensure TDLib is installed. Add this to your project root:

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gperf \
    git \
    zlib1g-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and build TDLib
RUN git clone https://github.com/tdlib/td.git && \
    cd td && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . && \
    make install && \
    cd ../.. && \
    rm -rf td

# Set up app directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

2. Update `railway.toml` to use Dockerfile:
```toml
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 5
```

## Step 5: Deploy

If using Railway CLI:
```bash
railway up
```

Otherwise, Railway will automatically deploy when you push to your GitHub repository.

## Step 6: First-Time Setup

1. Get your application URL from Railway dashboard
2. Visit `https://your-railway-url/auth/phone` to authenticate with Telegram
3. Enter your phone number
4. Check your Telegram app for the verification code
5. Submit the code at `https://your-railway-url/auth/code`

## Monitoring

1. View logs in Railway dashboard under the "Deployments" tab
2. Check deployment status and metrics in the "Overview" tab
3. Monitor PostgreSQL usage in the database service dashboard

## Troubleshooting

1. If the build fails:
   - Check build logs in Railway dashboard
   - Verify Dockerfile syntax
   - Ensure all dependencies are listed in requirements.txt

2. If the application crashes:
   - Check application logs in Railway dashboard
   - Verify environment variables are set correctly
   - Check PostgreSQL connection

3. If Telegram authentication fails:
   - Verify API credentials in environment variables
   - Check TDLib installation in container
   - Ensure proper network connectivity

## Scaling

Railway.com automatically handles scaling for you. However, you can:

1. Adjust instance size in Railway dashboard
2. Configure auto-scaling rules
3. Add multiple regions if needed

## Backup

1. Enable Railway's automatic PostgreSQL backups
2. Download backups periodically using Railway CLI:
```bash
railway service postgres backup download
```

## Cost Optimization

1. Monitor usage in Railway dashboard
2. Set up spending limits
3. Use smaller instance sizes during development
4. Clean up unused services and deployments
