## oGritador

Bot para Discord em Python, feito com `discord.py`. Ele entra automaticamente em um canal de voz e, de tempos em tempos, toca um áudio aleatório da pasta configurada.

### Funcionalidades

- **Conexão automática**: entra no canal de voz configurado assim que o bot inicia.
- **Grito imediato**: toca um áudio aleatório logo após conectar.
- **Grito aleatório**: toca um áudio aleatório a cada 40 a 60 minutos (configurável).
- **Não grita sozinho**: se não houver ninguém no canal, pula a vez.
- **Reconexão**: se cair do canal de voz, volta sozinho no próximo grito.
- **Comandos** (exigem a permissão "Mover membros"):
  - `!gritar` — toca um áudio agora.
  - `!pausar` — para os gritos e sai do canal.
  - `!voltar` — retoma os gritos.

### Configuração

1. **Requisitos**: Python 3.8+ e [FFmpeg](https://ffmpeg.org/) instalado (`sudo apt install ffmpeg`).

2. **Instalação**:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Arquivo `.env`** na raiz do projeto:

    ```plaintext
    DISCORD_TOKEN=seu_token_aqui
    GUILD_ID=id_do_servidor
    VOICE_CHANNEL_ID=id_do_canal_de_voz
    AUDIO_FOLDER_PATH=Audios

    # Opcional: intervalo entre gritos, em minutos (padrão 40 a 60)
    MIN_MINUTES=40
    MAX_MINUTES=60
    ```

4. **Execução** (a partir da pasta do projeto, para o caminho `Audios` funcionar):

    ```bash
    python main.py
    ```

### Áudios

O bot sorteia um arquivo `.mp3` ou `.wav` da pasta definida em `AUDIO_FOLDER_PATH`. Para adicionar mais gritos, basta colocar mais arquivos na pasta `Audios/`.

### Bot no Discord

No [Discord Developer Portal](https://discord.com/developers/applications), ative o intent **Message Content** do bot. Sem ele, os comandos com `!` não funcionam.

### Rodando 24/7 com systemd

Crie `/etc/systemd/system/gritador.service`:

```ini
[Unit]
Description=oGritador
After=network-online.target

[Service]
WorkingDirectory=/home/ubuntu/oGritador
ExecStart=/home/ubuntu/oGritador/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

E ative:

```bash
sudo systemctl enable --now gritador
```

Ajuste os caminhos para o usuário e a pasta da sua máquina.
