
# Bot de Alertas de Ofertas no Telegram

Bot desenvolvido em Python para monitorar canais do Telegram e enviar automaticamente ofertas que correspondam a palavras-chave configuradas.

## Funcionalidades

- Monitoramento automatizado de múltiplos canais do Telegram.
- Filtragem de mensagens por palavras-chave personalizáveis.
- Encaminhamento de ofertas com textos e imagens.
- Comandos para adicionar e remover palavras-chave.
- Gerenciamento dos canais monitorados.
- Armazenamento do progresso para evitar o processamento repetido de mensagens.

## Tecnologias utilizadas

- Python
- Telethon
- Telegram Bot API
- Requests
- JSON
- Programação assíncrona (asyncio)

## Como funciona

O sistema monitora os canais configurados e analisa as mensagens recebidas.

Quando identifica uma mensagem contendo alguma das palavras-chave cadastradas, encaminha a oferta para o chat de destino por meio da API do Telegram.

O bot também permite gerenciar os canais e as palavras-chave por comandos, sem precisar alterar diretamente o código.

## Instalação

### 1. Baixar o projeto

Clone o repositório usando o Git:

```bash
git clone https://github.com/franbtzky/Bot-de-alertas-de-ofertas-no-Telegram.git
```

Entre na pasta do projeto:

```bash
cd Bot-de-alertas-de-ofertas-no-Telegram
```

Também é possível baixar os arquivos pela opção **Code → Download ZIP** no GitHub.

### 2. Instalar as dependências

É necessário ter o Python instalado.

No terminal, execute:

```bash
pip install -r requirements.txt
```

### 3. Configurar as credenciais

Crie um arquivo chamado `.env` na pasta principal do projeto, utilizando o `.env.example` como referência.

Preencha com suas próprias credenciais:

```dotenv
TELEGRAM_API_ID=seu_api_id
TELEGRAM_API_HASH=seu_api_hash
TELEGRAM_BOT_TOKEN=seu_token_do_bot
```

O `API_ID` e o `API_HASH` podem ser obtidos em https://my.telegram.org.

O token do bot pode ser gerado pelo **@BotFather**, no Telegram.

**Importante:** o arquivo `.env` contém informações privadas e não deve ser publicado.

### 4. Configurar os canais e as palavras-chave

Crie o arquivo `canais.json` a partir do modelo `canais.example.json`, substituindo os dados fictícios pelos canais desejados.

No arquivo `palavras.txt`, configure os termos que deseja monitorar.

As palavras-chave também podem ser gerenciadas pelos comandos do bot.

### 5. Executar o projeto

No terminal, dentro da pasta do projeto, execute:

```bash
python monitor.py
```

Na primeira execução, o Telethon poderá solicitar a autenticação da conta do Telegram utilizada no monitoramento.

Após a configuração inicial, o sistema poderá monitorar os canais cadastrados e encaminhar as ofertas encontradas.

## Comandos disponíveis

| Comando | Função |
|---------|--------|
| `/ajuda` | Exibe os comandos disponíveis |
| `/adicionar palavra` | Adiciona uma palavra-chave |
| `/remover palavra` | Remove uma palavra-chave |
| `/lista` | Lista as palavras-chave cadastradas |
| `/canais` | Lista os canais monitorados |
| `/adicionar_canal @canal` | Adiciona um canal ao monitoramento |
| `/remover_canal ID` | Remove um canal monitorado |

## Segurança

As credenciais de acesso e os arquivos de sessão do Telegram devem permanecer privados.

O projeto utiliza variáveis de ambiente para evitar a exposição de informações sensíveis no código-fonte.
