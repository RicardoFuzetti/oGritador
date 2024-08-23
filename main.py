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
AUDIO_FOLDER_PATH = os.getenv('AUDIO_FOLDER_PATH')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


def get_random_audio_file(folder_path):
    """Retorna um caminho de arquivo de áudio aleatório dentro da pasta especificada."""
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
    if audio_files:
        return os.path.join(folder_path, random.choice(audio_files))
    print(f"Nenhum arquivo de áudio encontrado em {folder_path}")
    return None


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!')
    guild = bot.get_guild(GUILD_ID)
    if guild:
        voice_channel = guild.get_channel(VOICE_CHANNEL_ID)
        if voice_channel:
            await voice_channel.connect()
            play_audio.start()
            print("Função play_audio iniciada.")
        else:
            print(f"Canal de voz com ID {VOICE_CHANNEL_ID} não encontrado.")
    else:
        print(f"Guilde com ID {GUILD_ID} não encontrada.")


#@tasks.loop(seconds=1)
@tasks.loop(minutes=1)
async def play_audio():
    # Espera um tempo aleatório entre 40min e 60min
    await asyncio.sleep(random.randint(2400, 3600))
    #await asyncio.sleep(random.randint(1, 10))

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"Guilde com ID {GUILD_ID} não encontrada.")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=guild)
    if not voice_client or not voice_client.is_connected():
        print("Não estou conectado a um canal de voz.")
        return

    if voice_client.is_playing():
        print("Já está tocando áudio.")
        return

    audio_file = get_random_audio_file(AUDIO_FOLDER_PATH)
    if audio_file and os.path.isfile(audio_file):
        audio_source = discord.FFmpegPCMAudio(audio_file)
        voice_client.play(audio_source, after=lambda e: print(f'Finished playing: {audio_file}'))
        print(f"Reproduzindo: {audio_file}")
    else:
        print(f"Arquivo de áudio não encontrado ou pasta vazia: {AUDIO_FOLDER_PATH}")


@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        print("Desconectado do canal de voz.")
    else:
        print("Não estou em um canal de voz.")

bot.run(DISCORD_TOKEN)
