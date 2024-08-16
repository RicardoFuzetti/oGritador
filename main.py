import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Carregar variáveis do ambiente
GUILD_ID = int(os.getenv('GUILD_ID'))
VOICE_CHANNEL_ID = int(os.getenv('VOICE_CHANNEL_ID'))
AUDIO_FILE_PATH = os.getenv('AUDIO_FILE_PATH')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!')
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        await voice_channel.connect()
        play_audio.start()
        print("Função play_audio iniciada.")
    else:
        print(f"Canal de voz com ID {VOICE_CHANNEL_ID} não encontrado.")


@tasks.loop(seconds=1)
async def play_audio():
    await asyncio.sleep(random.randint(1, 10))  # Aguarda entre 1 a 10 segundos

    guild = bot.get_guild(GUILD_ID)
    if guild:
        voice_client = discord.utils.get(bot.voice_clients, guild=guild)
        if voice_client and voice_client.is_connected():
            if not voice_client.is_playing():
                if os.path.isfile(AUDIO_FILE_PATH):
                    audio_source = discord.FFmpegPCMAudio(AUDIO_FILE_PATH)
                    voice_client.play(audio_source, after=lambda e: print(f'Finished playing: {AUDIO_FILE_PATH}'))
                    print(f"Reproduzindo: {AUDIO_FILE_PATH}")
                else:
                    print(f"Arquivo de áudio não encontrado: {AUDIO_FILE_PATH}")
        else:
            print("voice_client não encontrado ou não está conectado.")
    else:
        print(f"Guilde com ID {GUILD_ID} não encontrada.")


@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        print("Desconectado do canal de voz.")
    else:
        print("Não estou em um canal de voz.")


bot.run(DISCORD_TOKEN)
