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
AUDIO_FOLDER_PATH = os.environ["AUDIO_FOLDER_PATH"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
MIN_MINUTES = int(os.getenv("MIN_MINUTES", 40))
MAX_MINUTES = int(os.getenv("MAX_MINUTES", 60))

log = logging.getLogger("gritador")

# Canal fixado pelo !entrar; volta a None quando o canal esvazia
pinned_channel_id = None

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_random_audio_file(folder_path):
    """Retorna um caminho de arquivo de áudio aleatório dentro da pasta especificada."""
    audio_files = [f for f in os.listdir(folder_path) if f.endswith((".mp3", ".wav"))]
    return os.path.join(folder_path, random.choice(audio_files)) if audio_files else None


def count_humans(channel):
    return sum(not member.bot for member in channel.members)


async def join(guild, channel):
    """Entra no canal, ou se move para ele se já estiver em outro."""
    voice_client = guild.voice_client
    if voice_client and voice_client.is_connected():
        if voice_client.channel != channel:
            await voice_client.move_to(channel)
        return voice_client
    return await channel.connect()


def pick_channel(guild):
    """Canal fixado pelo !entrar enquanto tiver gente; senão, o canal com mais pessoas."""
    global pinned_channel_id

    pinned = guild.get_channel(pinned_channel_id) if pinned_channel_id else None
    if pinned and count_humans(pinned) > 0:
        return pinned
    pinned_channel_id = None

    channels = [
        channel
        for channel in guild.voice_channels
        if channel != guild.afk_channel
        and channel.permissions_for(guild.me).connect
        and channel.permissions_for(guild.me).speak
    ]
    target = max(channels, key=count_humans, default=None)
    if target is None or count_humans(target) == 0:
        return None
    return target


async def scream():
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        raise RuntimeError(f"Guilda com ID {GUILD_ID} não encontrada.")

    # Não troca de canal no meio de um grito
    if guild.voice_client and guild.voice_client.is_playing():
        return

    channel = pick_channel(guild)
    if channel is None:
        return
    voice_client = await join(guild, channel)

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


@bot.command(name="entrar")
@commands.has_permissions(move_members=True)
async def entrar(ctx):
    global pinned_channel_id

    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("Entre em um canal de voz primeiro.")
        return

    channel = ctx.author.voice.channel
    pinned_channel_id = channel.id
    await join(ctx.guild, channel)
    await ctx.send(f"Entrei em {channel.mention}. Fico aqui até o canal esvaziar.")


@bot.command(name="pausar")
@commands.has_permissions(move_members=True)
async def pausar(ctx):
    global pinned_channel_id

    pinned_channel_id = None
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
