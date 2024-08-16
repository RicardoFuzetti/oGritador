## Discord Voice Bot

Este projeto é um bot para Discord desenvolvido em Python, utilizando a biblioteca `discord.py`, que se conecta a um canal de voz específico e reproduz arquivos de áudio em intervalos aleatórios. O bot é configurado para tocar um arquivo de áudio específico assim que se conecta ao canal de voz e, subsequentemente, toca o mesmo arquivo em intervalos aleatórios entre 1 e 10 segundos.

### Funcionalidades

- **Conexão Automática**: O bot se conecta automaticamente ao canal de voz especificado assim que é iniciado.
- **Reprodução Imediata**: Toca um arquivo de áudio específico assim que se conecta ao canal de voz.
- **Reprodução Aleatória**: Reproduz o arquivo de áudio em intervalos aleatórios entre 1 e 10 segundos enquanto está no canal de voz.
- **Comando de Saída**: Permite que o bot se desconecte do canal de voz com o comando `!leave`.

### Configuração

1. **Instalação**: Clone o repositório e instale as dependências usando:

    ```bash
    pip install -r requirements.txt
    ```

2. **Arquivo `.env`**: Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

    ```plaintext
    DISCORD_TOKEN=your_discord_token_here
    GUILD_ID=410939056390668288
    VOICE_CHANNEL_ID=691001053751279677
    AUDIO_FILE_PATH=C:\\Users\\Ricardo\\Desktop\\teste.mp3
    ```

3. **Execução**: Execute o bot com:

    ```bash
    python main.py
    ```

### Dependências

- `discord.py`
- `python-dotenv`

### Contribuição

Sinta-se à vontade para contribuir para o projeto! Você pode fazer isso enviando um pull request ou abrindo um issue para sugerir melhorias ou relatar problemas.

### Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
