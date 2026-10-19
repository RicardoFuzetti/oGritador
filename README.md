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

3. **Arquivo `.env`**: copie o modelo e preencha (veja [Configurando o `.env`](#configurando-o-env)):

    ```bash
    cp .env.example .env
    ```

4. **Execução** (a partir da pasta do projeto, para o caminho `Audios` funcionar):

    ```bash
    python main.py
    ```

### Configurando o `.env`

| Variável | Obrigatória | O que é |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Sim | Token do bot |
| `GUILD_ID` | Sim | ID do servidor onde o bot vai gritar |
| `VOICE_CHANNEL_ID` | Sim | ID do canal de voz |
| `AUDIO_FOLDER_PATH` | Sim | Pasta com os áudios (`Audios`). No Docker é ignorada |
| `MIN_MINUTES` | Não | Intervalo mínimo entre gritos, em minutos (padrão `40`) |
| `MAX_MINUTES` | Não | Intervalo máximo entre gritos, em minutos (padrão `60`) |

**Token do bot**

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications) e abra sua aplicação (ou crie uma em **New Application**).
2. Na aba **Bot**, clique em **Reset Token** e copie o valor para `DISCORD_TOKEN`. O Discord só mostra o token uma vez.
3. Na mesma aba, ative **Message Content Intent**.
4. Para convidar o bot: aba **OAuth2 > URL Generator**, marque o escopo `bot` e as permissões **Connect** e **Speak**, e abra a URL gerada.

**IDs do servidor e do canal**

1. No Discord, ative o modo desenvolvedor: **Configurações de usuário > Avançado > Modo desenvolvedor**.
2. Clique com o botão direito no ícone do servidor > **Copiar ID do servidor** e cole em `GUILD_ID`.
3. Clique com o botão direito no canal de voz > **Copiar ID do canal** e cole em `VOICE_CHANNEL_ID`.

Exemplo preenchido (valores fictícios):

```plaintext
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4.GabcDe.exemplo_de_token_nao_use
GUILD_ID=123456789012345678
VOICE_CHANNEL_ID=234567890123456789
AUDIO_FOLDER_PATH=Audios
```

> **Atenção:** o token dá controle total do bot. Não commite o `.env` (ele já está no `.gitignore`) e não compartilhe o token. Se ele vazar, gere outro em **Reset Token**.

### Áudios

O bot sorteia um arquivo `.mp3` ou `.wav` da pasta definida em `AUDIO_FOLDER_PATH`. Para adicionar mais gritos, basta colocar mais arquivos na pasta `Audios/`.

### Rodando com Docker

Com o `.env` criado (o `AUDIO_FOLDER_PATH` dele é ignorado no container):

```bash
docker compose up -d --build
```

O container reinicia sozinho se cair ou se a máquina reiniciar. Os áudios da pasta `Audios/` são montados no container, então dá para adicionar novos sem refazer a imagem. Logs:

```bash
docker compose logs -f
```

### Rodando 24/7 com systemd (sem Docker)

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
