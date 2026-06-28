import asyncio
import random
import httpx
from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from fastapi import FastAPI

# ─── CONFIG ───────────────────────────────────────────────────────────────────
TOKEN = "7500348646:AAG0JIi-PXX9Q7yEzP_-iSQ6QziVFLWy0-o"
CHANNEL_ID = "@mine1wgroup"
RENDER_URL = "https://minebot-y8sm.onrender.com"  # ← remplace par ton URL Render

MESSAGES_TO_FORWARD = [
    {"from_chat_id": "@mine1wgroup", "message_id": 285},
    {"from_chat_id": "@mine1wgroup", "message_id": 599},
    {"from_chat_id": "@mine1wgroup", "message_id": 1677},
    {"from_chat_id": "@mine1wgroup", "message_id": 867},
    {"from_chat_id": "@mine1wgroup", "message_id": 43035},
    {"from_chat_id": "@mine1wgroup", "message_id": 1236},
]

STICKERS = [
    "CAACAgIAAxkBAAEN3jZnuDFrQjM9UFkluMKs_JNY9hgVaAACAwEAAladvQoC5dF4h-X6TzYE",
    "CAACAgEAAxkBAAEN_fNnyTR9qijdQimoq2fC0Fo5ugxZWwAC_AADOA6CEUCO7Z9DKY4HNgQ",
    "CAACAgIAAxkBAAEN7oVnxLG76xXfbQ6xfgIBX2zUiUxOvQACKQADWbv8JWiEdiw7SWZ7NgQ",
]

WIN_MESSAGES = [
    "✅✅✅ <i>GREENNNNNN!!!</i> ✅✅✅💰",
    "✅✅✅ GREENNNNNN!!! ✅✅✅",
]

# ─── INIT ─────────────────────────────────────────────────────────────────────
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
app = FastAPI()

# ─── ROUTES HTTP ──────────────────────────────────────────────────────────────
@app.get("/")
async def home():
    return {"status": "Bot en cours d'exécution"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def generate_grid() -> str:
    grid_size = 5
    total_stars = 4 if random.randint(1, 5) != 5 else 5
    grid = [["🟦"] * grid_size for _ in range(grid_size)]
    for pos in random.sample(range(grid_size * grid_size), total_stars):
        row, col = divmod(pos, grid_size)
        grid[row][col] = "⭐"
    return "\n".join("".join(row) for row in grid)

# ─── TÂCHES ───────────────────────────────────────────────────────────────────
async def send_signals():
    """Envoie des signaux en continu avec gestion d'erreur par cycle."""
    while True:
        try:
            await bot.send_message(CHANNEL_ID, "🚨 <i>Checking new signal.....</i>")
            await asyncio.sleep(random.randint(20, 30))

            grid = generate_grid()
            message = (
                "✅ CONFIRMED ENTRY! \n"
                "<i>Valid for 3 minutes ......</i>\n"
                "Bombs: 3 💣\n\n"
                f"{grid}\n\n"
                '👉 <a href="https://one-vv1089.com/?open=register&p=8ocv">Play here !</a>\n'
                "❓ <a href=\"https://t.me/c/2183428707/285\">How to play ?  </a>"
            )
            signal_msg = await bot.send_message(
                CHANNEL_ID, message, disable_web_page_preview=True
            )

            await asyncio.sleep(5)
            await bot.send_message(CHANNEL_ID, "👉 <i>Play within 3 minutes...</i> ✅")

            await asyncio.sleep(160)
            await bot.send_message(
                CHANNEL_ID,
                random.choice(WIN_MESSAGES),
                reply_to_message_id=signal_msg.message_id,
            )

            await bot.send_sticker(CHANNEL_ID, random.choice(STICKERS))
             # ------------ newmsg --------------------
#         newmsg = "Register using the coupon CASHF and get a 500% bonus on your first deposit and activate the bot. 💎
# (Minimum $10 required to activate)"
            await bot.send_message(CHANNEL_ID, "Register using the coupon CASHF and get a 500% bonus on your first deposit and activate the bot. 💎
(Minimum $10 required to activate)",)      
            await asyncio.sleep(random.randint(2, 5))
            
        except Exception as e:
            print(f"[send_signals] Erreur : {e}")
            await asyncio.sleep(15)  # pause avant de réessayer


async def forward_scheduled_messages():
    """Transfère les messages planifiés en boucle."""
    while True:
        for ref in MESSAGES_TO_FORWARD:
            try:
                await bot.forward_message(
                    chat_id=CHANNEL_ID,
                    from_chat_id=ref["from_chat_id"],
                    message_id=ref["message_id"],
                )
            except Exception as e:
                print(f"[forward] Erreur message {ref['message_id']} : {e}")
            await asyncio.sleep(480)
        await asyncio.sleep(400)


async def keep_alive():
    """Ping le service toutes les 10 min pour éviter la mise en veille Render."""
    await asyncio.sleep(60)  # attendre que le serveur soit bien démarré
    async with httpx.AsyncClient(timeout=10) as client:
        while True:
            try:
                r = await client.get(f"{RENDER_URL}/health")
                print(f"[keep_alive] Ping OK ({r.status_code})")
            except Exception as e:
                print(f"[keep_alive] Ping échoué : {e}")
            await asyncio.sleep(600)  # toutes les 10 min


# ─── BOUCLE PRINCIPALE ────────────────────────────────────────────────────────
async def main():
    """Lance toutes les tâches avec redémarrage automatique en cas de crash."""
    print("✅ Bot démarré")
    while True:
        try:
            await asyncio.gather(
                send_signals(),
                forward_scheduled_messages(),
                keep_alive(),
            )
        except Exception as e:
            print(f"[main] Crash inattendu : {e} — redémarrage dans 10s")
            await asyncio.sleep(10)


# ─── STARTUP FASTAPI ──────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(main())


# ─── LANCEMENT DIRECT ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())
