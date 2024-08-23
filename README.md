## oGritador

Este projeto é um bot para Discord desenvolvido em Python, utilizando a biblioteca `discord.py`. O bot se conecta automaticamente a um canal de voz específico, onde reproduz arquivos de áudio de forma aleatória em intervalos definidos. Assim que se conecta ao canal, o bot toca um arquivo de áudio específico e, em seguida, continua tocando arquivos aleatórios a cada 1 a 10 segundos.

### Funcionalidades

- **Conexão Automática**: O bot se conecta automaticamente ao canal de voz especificado ao ser iniciado.
- **Reprodução Imediata**: Toca um arquivo de áudio específico imediatamente após se conectar ao canal de voz.
- **Reprodução Aleatória**: Reproduz arquivos de áudio aleatórios a cada 40 a 60 minutos enquanto está conectado ao canal de voz.
- **Comando de Saída**: Permite que o bot se desconecte do canal de voz com o comando `!leave`.

### Configuração

1. **Instalação**: Clone o repositório e instale as dependências usando:

    ```bash
    pip install -r requirements.txt
    ```

2. **Arquivo `.env`**: Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

    ```plaintext
    DISCORD_TOKEN=your_discord_token_here
    GUILD_ID=your_server_id
    VOICE_CHANNEL_ID=your_voice_channel_id
    AUDIO_FOLDER_PATH=your_audio_folder_path
    ```

3. **Execução**: Execute o bot com:

    ```bash
    python main.py
    ```

### Dependências

- `discord.py`
- `python-dotenv`

### Observações

Necessário ter o FFmpeg instalado na máquina.
