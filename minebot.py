import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "7091485258:AAEbrnfh0gvjsuzh7OLdSignMKjBUPbSJuU"
CHANNEL_ID = "@agen1win"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Fonction pour générer une grille avec des étoiles aléatoires
def generate_grid():
    grid_size = 5  # 5x5
    total_stars = 4 if random.randint(1, 5) != 5 else 5  # 4 étoiles sauf 1 fois sur 5 où il y en a 5

    grid = [["🟦" for _ in range(grid_size)] for _ in range(grid_size)]
    
    positions = random.sample(range(grid_size * grid_size), total_stars)
    for pos in positions:
        row, col = divmod(pos, grid_size)
        grid[row][col] = "⭐"
    
    return "\n".join("".join(row) for row in grid)

# Fonction pour envoyer les messages automatiquement
async def send_signals():
    while True:
        # Étape 1 : "Checking new signal..."
        await bot.send_message(CHANNEL_ID, "🔴 Checking new signal...")
        await asyncio.sleep(random.randint(50, 60))

        # Étape 2 : Envoi du signal avec la grille générée
        grid = generate_grid()
        message = f"✅ CONFIRMED ENTRY!\nBombs: 3 💣\nAttempts: 3\n\n{grid}\n\n👉 <b>Play Here!</b>"
        await bot.send_message(CHANNEL_ID, message)
        await asyncio.sleep(5)

        # Étape 3 : Rappel de jouer avant 3 minutes
        await bot.send_message(CHANNEL_ID, "👉 <b>3 minutes left!</b> ✅")
        await asyncio.sleep(180)  # 3 minutes

        # Étape 4 : Envoi du sticker de victoire
        sticker_id = "CAACAgIAAxkBAAEN3jZnuDFrQjM9UFkluMKs_JNY9hgVaAACAwEAAladvQoC5dF4h-X6TzYE"  # Remplace par un vrai sticker ID
        await bot.send_sticker(CHANNEL_ID, sticker_id)

        # Pause avant le prochain cycle
        await asyncio.sleep(random.randint(10, 30))

# Démarrage du bot
async def main():
    asyncio.create_task(send_signals())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
