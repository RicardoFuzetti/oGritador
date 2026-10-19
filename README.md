## oGritador

Bot para Discord em Python, feito com `discord.py`. De tempos em tempos, ele entra sozinho no canal de voz com mais gente e toca um áudio aleatório da pasta configurada.

### Funcionalidades

- **Vai atrás do pessoal**: a cada grito, entra (ou se move) no canal de voz com mais pessoas, sem contar bots. Ignora o canal AFK e canais onde não pode falar.
- **Grito imediato**: grita assim que o bot inicia, se houver alguém em algum canal.
- **Grito aleatório**: toca um áudio aleatório a cada 40 a 60 minutos (configurável).
- **Não grita sozinho**: se todos os canais estiverem vazios, pula a vez.
- **Reconexão**: se cair do canal de voz, volta sozinho no próximo grito.
- **Comandos** (exigem a permissão "Mover membros"):
  - `!entrar` — entra no canal de voz de quem chamou e fica nele até o canal esvaziar. Depois volta a escolher o canal com mais gente.
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
| `AUDIO_FOLDER_PATH` | Sim | Pasta com os áudios (`Audios`). No Docker é ignorada |
| `MIN_MINUTES` | Não | Intervalo mínimo entre gritos, em minutos (padrão `40`) |
| `MAX_MINUTES` | Não | Intervalo máximo entre gritos, em minutos (padrão `60`) |

**Token do bot**

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications) e abra sua aplicação (ou crie uma em **New Application**).
2. Na aba **Bot**, clique em **Reset Token** e copie o valor para `DISCORD_TOKEN`. O Discord só mostra o token uma vez.
3. Na mesma aba, ative **Message Content Intent**.
4. Para convidar o bot: aba **OAuth2 > URL Generator**, marque o escopo `bot` e as permissões **Connect** e **Speak**, e abra a URL gerada.

**ID do servidor**

1. No Discord, ative o modo desenvolvedor: **Configurações de usuário > Avançado > Modo desenvolvedor**.
2. Clique com o botão direito no ícone do servidor > **Copiar ID do servidor** e cole em `GUILD_ID`.

Exemplo preenchido (valores fictícios):

```plaintext
DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4.GabcDe.exemplo_de_token_nao_use
GUILD_ID=123456789012345678
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
