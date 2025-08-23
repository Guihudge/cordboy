from typing import List


ROM_PATH = "roms/rom.gb" # Path of your rom
SAVESTATE_PATH = "roms/rom.gb.state" # Path of your save state
DISCORD_TOKEN = "discord-token" # Discord bot token
GIF_OUTPUT = "public/" # Output dir of gifs 
BASE_URL="https://gamecord.example.com" # Base URL used to build gifs url
COUNTER_PATH="framecounter.txt" # file saving frame count (used in case of bot restart)
SCALE=2 # Image scaling, gameboy_resolution * SCALE

FRAME_RESOLUTION=(144*SCALE,160*SCALE) # DO NOT CHANGE

REACTIONS: List[str] = [ # Controller, if change, change also in main>trigger_input()>mapping
    "⬆️",  # Haut
    "⬇️",  # Bas
    "⬅️",  # Gauche
    "➡️",  # Droite
    "🅰️",  # A
    "🅱️",  # B
    "⏯️",  # Start
    "🎯",  # Select
]