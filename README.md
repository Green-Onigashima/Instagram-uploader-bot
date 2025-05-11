
## 📸 Instagram Reels Uploader Telegram Bot

A secure Telegram bot that lets you upload Instagram Reels by simply replying to a video with the `/upload` command. Designed for private use by the bot owner.

---

### ✨ Features

* ✅ Upload reels to Instagram by replying to any video or document with `/upload`
* 🔐 All commands are restricted to the bot owner (except `/start`)
* 🛠 Manage Instagram credentials via `/settings` command (through Telegram)
* ☁️ MongoDB for persistent IG credentials storage
* 📦 Deploy-ready for **Docker**, **Render**, **Koyeb**, etc.

---

### 🚀 How It Works

1. Start the bot: `/start`
2. Send a video or document (MP4) to the bot
3. **Reply** to that video with `/upload`
4. Done! The reel is uploaded to your Instagram account.

> ⚠️ You must set your IG credentials first using the `/settings` command.

---

### 🧠 Commands

| Command     | Description                             | Access     |
| ----------- | --------------------------------------- | ---------- |
| `/start`    | Start the bot                           | Public     |
| `/upload`   | Reply to a video with this to upload    | Owner only |
| `/settings` | Manage IG username/password via buttons | Owner only |
| `/cancel`   | Cancel any pending state                | Owner only |

---

### 🧪 Requirements

* Telegram bot token
* Your Telegram user ID
* MongoDB database URI
* A valid Instagram account (must allow logins via script)

---

### 📁 Setup

#### 1. Clone the repo

```bash
git clone https://github.com/yourusername/instagram-reels-bot.git
cd instagram-reels-bot
```

#### 2. Create `.env` file

Copy the example and fill in real values:

```bash
cp .env.example .env
```

```env
TELEGRAM_TOKEN=your_bot_token
BOT_OWNER_ID=123456789
MONGO_URI=your_mongodb_connection_uri
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### ▶️ Run the bot

```bash
python bot.py
```

---

### 🐳 Docker Support

#### Build and run

```bash
docker build -t insta-reels-bot .
docker run --env-file .env insta-reels-bot
```

---

### ☁️ Deployment (Render/Koyeb)

* Add your `.env` values in the environment settings
* Use `Procfile` for web service:

```
web: python bot.py
```

---

### 🛡 Security Notes

* All commands except `/start` are restricted to the owner using Telegram user ID
* IG credentials are securely stored in MongoDB, not in code
* No third-party services or login pages are involved

---

### 🧰 Tech Stack

* [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
* [`instagrapi`](https://github.com/adw0rd/instagrapi)
* [`pymongo`](https://www.mongodb.com/)
* [`python-dotenv`](https://github.com/theskumar/python-dotenv)

---

### 📷 Example Usage

1. Send a video to the bot
2. Reply to it with `/upload`
3. Get a success or error message directly

---

### 💡 Tips

* Use a test Instagram account first
* Keep IG credentials updated through `/settings`
* Ensure MongoDB URI allows external access

---

### 📄 License

MIT License

---

Would you like me to include a sample `.env`, or turn this into a real `README.md` file you can download directly?
