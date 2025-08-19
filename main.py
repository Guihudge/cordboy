from typing import Optional

import discord
from discord.ext import commands
from discord import Reaction, User
from pyboy import PyBoy

from config import BASE_URL, ROM_PATH, SAVESTATE_PATH, REACTIONS, DISCORD_TOKEN, GIF_OUTPUT
from pyboyHelper import startEmulator, gen_video, savestate

# Discord stuff
intents: discord.Intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)

bot.menu_message_id: Optional[int] = None # pyright: ignore[reportUndefinedVariable, reportInvalidTypeForm, reportAttributeAccessIssue]  # noqa: F821

# Instance PyBoy globale
pyboy: Optional[PyBoy] = None

def trigger_input(pyboy: PyBoy, emoji: str, pressDuration: int = 5) -> bool:
    mapping = {
        "⬆️": "up",
        "⬇️": "down",
        "⬅️": "left",
        "➡️": "right",
        "🅰️": "a",
        "🅱️": "b",
        "⏯️": "start",
        "🎯": "select",
    }
    if emoji in mapping:
        pyboy.button(mapping[emoji], pressDuration)
        return True
    return False

@bot.command()
async def gameboy(ctx: commands.Context) -> None:
    """Affiche le contrôleur Game Boy avec des réactions"""
    message = await ctx.send(f"{BASE_URL}/out.webp")
    for r in REACTIONS:
        await message.add_reaction(r)

    bot.menu_message_id = message.id # type: ignore

@bot.event
async def on_reaction_add(reaction: Reaction, user: User) -> None:
    if user == bot.user:
        return
    if reaction.message.id != bot.menu_message_id: # pyright: ignore[reportAttributeAccessIssue]
        return

    emoji: str = str(reaction.emoji)
    global pyboy
    id = 1
    if pyboy:
        trigger_input(pyboy, emoji)
        id = gen_video(pyboy, 2, GIF_OUTPUT)
        savestate(pyboy)
        print(f"video id: {id}")

    await reaction.message.edit(content=f"{BASE_URL}/out_{id:06d}.webp")
    # Réinitialiser les réactions
    try:
        await reaction.message.remove_reaction(reaction.emoji, user)
    except discord.Forbidden:
        await reaction.message.channel.send("Pas la permission de gérer les réactions.")

def main():
    global pyboy
    pyboy = startEmulator(ROM_PATH, SAVESTATE_PATH)

    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()