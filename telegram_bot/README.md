# Telegram Bot with aiogram and FastAPI

A simple Telegram bot built with [aiogram](https://docs.aiogram.dev/) 3.x and [FastAPI](https://fastapi.tiangolo.com/). This bot can run in both webhook mode (for production) and polling mode (for development).

## Features

- **Modern Stack**: Built with aiogram 3.x and FastAPI
- **Dual Mode**: Supports both webhook and polling modes
- **RESTful API**: Includes FastAPI endpoints for bot management
- **Environment Configuration**: Easy configuration with environment variables
- **Logging**: Comprehensive logging for debugging and monitoring
- **Health Checks**: Built-in health check endpoints

## Bot Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show available commands
- `/echo <text>` - Echo your message
- `/info` - Get your user information
- Any other message will be echoed back

## Setup

### 1. Prerequisites

- Python 3.8+
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

### 2. Installation

```bash
# Clone or navigate to the project directory
cd telegram_bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file and set your configuration:

```env
# Required: Get this from @BotFather
BOT_TOKEN=your_bot_token_here

# For webhook mode (production)
WEBHOOK_HOST=https://yourdomain.com
WEBHOOK_PATH=/webhook
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8000
```

## Running the Bot

### Development Mode (Polling)

For local development, use polling mode:

```bash
python polling.py
```

This mode:
- Doesn't require a public URL
- Polls Telegram servers for updates
- Perfect for local development and testing

### Production Mode (Webhook)

For production deployment, use webhook mode:

```bash
python main.py
```

This mode:
- Requires a public HTTPS URL
- More efficient for production
- Includes FastAPI web server with additional endpoints

## API Endpoints

When running in webhook mode, the following endpoints are available:

- `GET /` - Root endpoint with bot status
- `GET /health` - Health check endpoint
- `POST /webhook` - Telegram webhook endpoint (automatically configured)
- `GET /webhook/info` - Get current webhook information
- `POST /webhook/set` - Manually set webhook
- `POST /webhook/delete` - Delete webhook (switch to polling)

### Example API Usage

```bash
# Check bot status
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Get webhook info
curl http://localhost:8000/webhook/info

# Set webhook
curl -X POST http://localhost:8000/webhook/set

# Delete webhook
curl -X POST http://localhost:8000/webhook/delete
```

## Project Structure

```
telegram_bot/
├── main.py              # FastAPI application with webhook
├── bot.py               # Bot handlers and logic
├── polling.py           # Polling mode script
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t telegram-bot .
docker run -p 8000:8000 --env-file .env telegram-bot
```

### Using systemd (Linux)

Create a service file `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/telegram_bot
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Using nginx (Reverse Proxy)

Configure nginx to proxy requests to your FastAPI app:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | - | Yes |
| `WEBHOOK_HOST` | Your domain for webhook (https://yourdomain.com) | - | No* |
| `WEBHOOK_PATH` | Webhook endpoint path | `/webhook` | No |
| `WEB_SERVER_HOST` | FastAPI server host | `0.0.0.0` | No |
| `WEB_SERVER_PORT` | FastAPI server port | `8000` | No |

*Required for webhook mode

## Troubleshooting

### Common Issues

1. **Bot Token Error**
   ```
   BOT_TOKEN not configured
   ```
   Solution: Make sure you've set the `BOT_TOKEN` in your `.env` file

2. **Webhook Issues**
   ```
   Webhook not accessible
   ```
   Solution: Ensure your domain is accessible via HTTPS and the webhook path is correct

3. **Port Already in Use**
   ```
   Address already in use
   ```
   Solution: Change the `WEB_SERVER_PORT` in your `.env` file or kill the process using the port

### Logs

The bot provides detailed logging. Check the console output for:
- Startup messages
- Webhook configuration status
- Error messages
- User interactions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.