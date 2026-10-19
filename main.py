import logging
import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# os.environ[...] falha com KeyError mostrando o nome da variável que falta
GUILD_ID = int(os.environ["GUILD_ID"])
VOICE_CHANNEL_ID = int(os.environ["VOICE_CHANNEL_ID"])
AUDIO_FOLDER_PATH = os.environ["AUDIO_FOLDER_PATH"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
MIN_MINUTES = int(os.getenv("MIN_MINUTES", 40))
MAX_MINUTES = int(os.getenv("MAX_MINUTES", 60))

log = logging.getLogger("gritador")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_random_audio_file(folder_path):
    """Retorna um caminho de arquivo de áudio aleatório dentro da pasta especificada."""
    audio_files = [f for f in os.listdir(folder_path) if f.endswith((".mp3", ".wav"))]
    return os.path.join(folder_path, random.choice(audio_files)) if audio_files else None


async def ensure_connected():
    """Retorna o voice client, reconectando ao canal se o bot tiver caído da voz."""
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        raise RuntimeError(f"Guilda com ID {GUILD_ID} não encontrada.")

    if guild.voice_client and guild.voice_client.is_connected():
        return guild.voice_client

    channel = guild.get_channel(VOICE_CHANNEL_ID)
    if channel is None:
        raise RuntimeError(f"Canal de voz com ID {VOICE_CHANNEL_ID} não encontrado.")
    return await channel.connect()


async def scream():
    voice_client = await ensure_connected()

    if voice_client.is_playing():
        return

    # Não grita para canal vazio
    if not any(not member.bot for member in voice_client.channel.members):
        return

    audio_file = get_random_audio_file(AUDIO_FOLDER_PATH)
    if audio_file is None:
        log.warning("Nenhum arquivo de áudio encontrado em %s", AUDIO_FOLDER_PATH)
        return

    def after(error):
        if error:
            log.error("Erro ao tocar %s: %s", audio_file, error)

    # FFmpeg já entrega Opus, sem recodificar no Python
    voice_client.play(discord.FFmpegOpusAudio(audio_file), after=after)
    log.info("Reproduzindo: %s", audio_file)


@tasks.loop(minutes=MIN_MINUTES)
async def play_audio():
    try:
        await scream()
    except Exception:
        # Exceção não tratada encerraria o loop
        log.exception("Falha ao gritar")
    play_audio.change_interval(minutes=random.randint(MIN_MINUTES, MAX_MINUTES))


@play_audio.before_loop
async def before_play_audio():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    log.info("Bot conectado como %s", bot.user)
    # on_ready dispara de novo a cada reconexão do gateway
    if not play_audio.is_running():
        play_audio.start()


@bot.command(name="gritar")
@commands.has_permissions(move_members=True)
async def gritar(ctx):
    await scream()


@bot.command(name="pausar")
@commands.has_permissions(move_members=True)
async def pausar(ctx):
    play_audio.cancel()
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    await ctx.send("Pausado. Use `!voltar` para retomar.")


@bot.command(name="voltar")
@commands.has_permissions(move_members=True)
async def voltar(ctx):
    if not play_audio.is_running():
        play_audio.start()
    await ctx.send("Voltei.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sem permissão para isso.")
    elif not isinstance(error, commands.CommandNotFound):
        log.error("Erro no comando %s: %s", ctx.command, error)


# root_logger=True faz os logs do "gritador" aparecerem junto com os do discord.py
bot.run(DISCORD_TOKEN, root_logger=True)
