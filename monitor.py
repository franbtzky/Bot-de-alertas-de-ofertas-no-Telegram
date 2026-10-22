import json
import os
import asyncio
import sys
import requests
import os 
from dotenv import load_dotenv

from telethon import TelegramClient


load_dotenv()

api_id = int(os.environ["TELEGRAM_API_ID"])
api_hash = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]



ARQUIVO_PALAVRAS = "palavras.txt"
ARQUIVO_PROGRESSO = "progresso.json"
ARQUIVO_CANAIS = "canais.json"



BOT_API = (
    f"https://api.telegram.org/bot{BOT_TOKEN}"
)



sys.stdout.reconfigure(
    encoding="utf-8"
)

sys.stderr.reconfigure(
    encoding="utf-8"
)




client = TelegramClient(
    "telegram_monitor",
    api_id,
    api_hash
)



CHAT_ALERTAS = None




ARQUIVO_CHAT = "chat_bot.json"


def carregar_chat_alertas():

    if not os.path.exists(
        ARQUIVO_CHAT
    ):

        return None

    try:

        with open(
            ARQUIVO_CHAT,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(
                arquivo
            )

            return dados.get(
                "chat_id"
            )

    except Exception:

        return None


def salvar_chat_alertas(
    chat_id
):

    with open(
        ARQUIVO_CHAT,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            {
                "chat_id": chat_id
            },
            arquivo,
            indent=4
        )


def bot_enviar_mensagem_sync(
    chat_id,
    texto
):

    url = (
        f"{BOT_API}/sendMessage"
    )

    dados = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    resposta = requests.post(
        url,
        data=dados,
        timeout=30
    )

    resultado = resposta.json()

    if not resultado.get("ok"):

        print(
            "[ERRO BOT] "
            f"{resultado}"
        )

        return False

    return True


def bot_enviar_foto_sync(
    chat_id,
    caminho_imagem
):

    url = (
        f"{BOT_API}/sendPhoto"
    )

    try:

        with open(
            caminho_imagem,
            "rb"
        ) as arquivo:

            arquivos = {
                "photo": arquivo
            }

            dados = {
                "chat_id": chat_id
            }

            resposta = requests.post(
                url,
                data=dados,
                files=arquivos,
                timeout=60
            )

        resultado = resposta.json()

        if not resultado.get("ok"):

            print(
                "[ERRO BOT FOTO] "
                f"{resultado}"
            )

            return False

        return True

    except Exception as erro:

        print(
            f"[ERRO BOT FOTO] {erro}"
        )

        return False

async def bot_enviar_foto(
    chat_id,
    caminho_imagem
):

    return await asyncio.to_thread(
        bot_enviar_foto_sync,
        chat_id,
        caminho_imagem
    )



async def bot_enviar_mensagem(
    chat_id,
    texto
):

    return await asyncio.to_thread(
        bot_enviar_mensagem_sync,
        chat_id,
        texto
    )


def bot_obter_updates_sync(
    offset=None
):

    url = (
        f"{BOT_API}/getUpdates"
    )

    parametros = {
        "timeout": 30
    }

    if offset is not None:

        parametros["offset"] = offset

    resposta = requests.get(
        url,
        params=parametros,
        timeout=40
    )

    resultado = resposta.json()

    if not resultado.get("ok"):

        print(
            "[ERRO BOT] "
            f"{resultado}"
        )

        return []

    return resultado.get(
        "result",
        []
    )


async def bot_obter_updates(
    offset=None
):

    return await asyncio.to_thread(
        bot_obter_updates_sync,
        offset
    )




def dividir_texto(
    texto,
    limite=4000
):

    partes = []

    while len(texto) > limite:

        posicao = texto.rfind(
            "\n",
            0,
            limite
        )

        if posicao <= 0:

            posicao = limite

        partes.append(
            texto[:posicao]
        )

        texto = texto[
            posicao:
        ].lstrip()

    if texto:

        partes.append(
            texto
        )

    return partes




def carregar_palavras_chave():

    try:

        with open(
            ARQUIVO_PALAVRAS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return [
                linha.strip().lower()
                for linha in arquivo
                if linha.strip()
            ]

    except FileNotFoundError:

        print(
            f"AVISO: {ARQUIVO_PALAVRAS} "
            "não encontrado."
        )

        return []


def salvar_palavras_chave(
    palavras
):

    with open(
        ARQUIVO_PALAVRAS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        for palavra in palavras:

            arquivo.write(
                palavra + "\n"
            )




def carregar_progresso():

    if not os.path.exists(
        ARQUIVO_PROGRESSO
    ):

        return {}

    try:

        with open(
            ARQUIVO_PROGRESSO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(
                arquivo
            )

    except Exception as erro:

        print(
            f"AVISO: não foi possível ler "
            f"{ARQUIVO_PROGRESSO}: {erro}"
        )

        return {}


def salvar_progresso(
    progresso
):

    with open(
        ARQUIVO_PROGRESSO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            progresso,
            arquivo,
            indent=4,
            ensure_ascii=False
        )




def carregar_canais():

    if not os.path.exists(
        ARQUIVO_CANAIS
    ):

        return {}

    try:

        with open(
            ARQUIVO_CANAIS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(
                arquivo
            )

    except Exception as erro:

        print(
            f"AVISO: não foi possível ler "
            f"{ARQUIVO_CANAIS}: {erro}"
        )

        return {}


def salvar_canais(
    canais
):

    with open(
        ARQUIVO_CANAIS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            canais,
            arquivo,
            indent=4,
            ensure_ascii=False
        )




async def enviar_promocao_bot(
    canal,
    palavras,
    texto,
    mensagem_original
):

    chat_id = carregar_chat_alertas()

    if chat_id is None:

        print(
            "⚠️ Nenhum chat do bot foi "
            "configurado para receber alertas."
        )

        return False



    cabecalho = (
        f"PALAVRA-CHAVE: *{', '.join(palavras)}*\n"
        f"CANAL: *{canal}*\n\n"
    )


    mensagem_completa = (
        cabecalho + texto
    )


 

    caminho_imagem = None


    if mensagem_original.photo:

        try:

            import tempfile

            arquivo_temporario = tempfile.NamedTemporaryFile(
                suffix=".jpg",
                delete=False
            )

            caminho_imagem = (
                arquivo_temporario.name
            )

            arquivo_temporario.close()


            print(
                "🖼️ Baixando imagem da promoção..."
            )


            await mensagem_original.download_media(
                file=caminho_imagem
            )


            if not os.path.exists(
                caminho_imagem
            ):

                caminho_imagem = None


        except Exception as erro:

            print(
                f"[ERRO] Não foi possível "
                f"baixar a imagem: {erro}"
            )

            caminho_imagem = None



    if caminho_imagem:

        try:

            sucesso = await bot_enviar_foto(
                chat_id,
                caminho_imagem
            )


            if sucesso:

                print(
                    "✅ Imagem enviada para o grupo."
                )

            else:

                print(
                    "❌ Falha ao enviar imagem."
                )


        finally:


            try:

                if os.path.exists(
                    caminho_imagem
                ):

                    os.remove(
                        caminho_imagem
                    )

                    print(
                        "🗑️ Imagem temporária apagada."
                    )

            except Exception as erro:

                print(
                    f"[ERRO] Não foi possível "
                    f"apagar imagem temporária: "
                    f"{erro}"
                )




    partes = dividir_texto(
        mensagem_completa
    )


    for parte in partes:

        sucesso = await bot_enviar_mensagem(
            chat_id,
            parte
        )


        if not sucesso:

            return False


    return True




async def processar_comando(
    chat_id,
    texto
):

    texto = texto.strip()

    texto_lower = texto.lower()




    salvar_chat_alertas(
        chat_id
    )



    if texto_lower == "/ajuda":

        await bot_enviar_mensagem(
            chat_id,

            "🤖 COMANDOS DO MONITOR\n\n"

            "/adicionar palavra\n"
            "Adiciona uma palavra-chave.\n\n"

            "/remover palavra\n"
            "Remove uma palavra-chave.\n\n"

            "/lista\n"
            "Mostra as palavras monitoradas.\n\n"

            "/canais\n"
            "Mostra os canais monitorados.\n\n"

            "/adicionar_canal @canal\n"
            "Adiciona um canal.\n\n"

            "/remover_canal ID\n"
            "Remove um canal.\n\n"

            "/ajuda\n"
            "Mostra os comandos."
        )

        return




    if texto_lower.startswith(
        "/adicionar "
    ):

        palavra = texto[
            len("/adicionar"):
        ].strip().lower()


        if not palavra:

            await bot_enviar_mensagem(
                chat_id,
                "Uso:\n"
                "/adicionar palavra"
            )

            return


        palavras = (
            carregar_palavras_chave()
        )


        if palavra in palavras:

            await bot_enviar_mensagem(
                chat_id,

                "⚠️ Essa palavra já "
                "está sendo monitorada:\n\n"
                f"{palavra}"
            )

            return


        palavras.append(
            palavra
        )


        salvar_palavras_chave(
            palavras
        )


        await bot_enviar_mensagem(
            chat_id,

            "✅ Palavra adicionada:\n\n"
            f"🔎 {palavra}"
        )

        return




    if texto_lower.startswith(
        "/remover "
    ):

        palavra = texto[
            len("/remover"):
        ].strip().lower()


        if not palavra:

            await bot_enviar_mensagem(
                chat_id,

                "Uso:\n"
                "/remover palavra"
            )

            return


        palavras = (
            carregar_palavras_chave()
        )


        if palavra not in palavras:

            await bot_enviar_mensagem(
                chat_id,

                "⚠️ Essa palavra não "
                "está cadastrada:\n\n"
                f"{palavra}"
            )

            return


        palavras.remove(
            palavra
        )


        salvar_palavras_chave(
            palavras
        )


        await bot_enviar_mensagem(
            chat_id,

            "✅ Palavra removida:\n\n"
            f"❌ {palavra}"
        )

        return


    if texto_lower == "/lista":

        palavras = (
            carregar_palavras_chave()
        )


        if not palavras:

            await bot_enviar_mensagem(
                chat_id,

                "🔎 Nenhuma palavra "
                "está cadastrada."
            )

            return


        lista = "\n".join(
            f"{numero}. {palavra}"
            for numero, palavra
            in enumerate(
                palavras,
                start=1
            )
        )


        await bot_enviar_mensagem(
            chat_id,

            "🔎 PALAVRAS MONITORADAS\n\n"
            + lista
        )

        return




    if texto_lower == "/canais":

        canais = (
            carregar_canais()
        )


        if not canais:

            await bot_enviar_mensagem(
                chat_id,

                "📢 Nenhum canal "
                "está sendo monitorado."
            )

            return


        texto_saida = (
            "📢 CANAIS MONITORADOS\n\n"
        )


        for numero, (
            canal_id,
            dados
        ) in enumerate(
            canais.items(),
            start=1
        ):

            nome = dados.get(
                "nome",
                "Canal sem nome"
            )


            texto_saida += (
                f"{numero}. {nome}\n"
                f"ID: {canal_id}\n\n"
            )


        for parte in dividir_texto(
            texto_saida
        ):

            await bot_enviar_mensagem(
                chat_id,
                parte
            )

        return




    if texto_lower.startswith(
        "/adicionar_canal"
    ):

        identificador = texto[
            len("/adicionar_canal"):
        ].strip()


        if not identificador:

            await bot_enviar_mensagem(
                chat_id,

                "Uso:\n"
                "/adicionar_canal @username"
            )

            return


        try:

            entidade = await client.get_entity(
                identificador
            )


            canal_id = entidade.id


            nome = getattr(
                entidade,
                "title",
                None
            )


            if not nome:

                nome = "Canal sem nome"


        except Exception as erro:

            await bot_enviar_mensagem(
                chat_id,

                "❌ Não consegui encontrar "
                "esse canal.\n\n"
                f"Erro: {erro}"
            )

            return


        canais = (
            carregar_canais()
        )


        if str(canal_id) in canais:

            await bot_enviar_mensagem(
                chat_id,

                "⚠️ Esse canal já "
                "está sendo monitorado."
            )

            return


        canais[
            str(canal_id)
        ] = {
            "nome": nome
        }


        salvar_canais(
            canais
        )


        progresso = (
            carregar_progresso()
        )


        mensagens = await client.get_messages(
            entidade,
            limit=1
        )


        if mensagens:

            progresso[
                str(canal_id)
            ] = mensagens[0].id

        else:

            progresso[
                str(canal_id)
            ] = 0


        salvar_progresso(
            progresso
        )


        await bot_enviar_mensagem(
            chat_id,

            "✅ CANAL ADICIONADO\n\n"
            f"Nome: {nome}\n"
            f"ID: {canal_id}\n\n"
            "O monitor começará a "
            "acompanhar as próximas mensagens."
        )

        return




    if texto_lower.startswith(
        "/remover_canal"
    ):

        identificador = texto[
            len("/remover_canal"):
        ].strip()


        if not identificador:

            await bot_enviar_mensagem(
                chat_id,

                "Uso:\n"
                "/remover_canal ID"
            )

            return


        canais = (
            carregar_canais()
        )


        if identificador not in canais:

            await bot_enviar_mensagem(
                chat_id,

                "❌ Esse canal não "
                "está sendo monitorado."
            )

            return


        nome = canais[
            identificador
        ].get(
            "nome",
            "Canal"
        )


        del canais[
            identificador
        ]


        salvar_canais(
            canais
        )


        await bot_enviar_mensagem(
            chat_id,

            "✅ CANAL REMOVIDO\n\n"
            f"{nome}\n"
            f"ID: {identificador}"
        )

        return


    

    await bot_enviar_mensagem(
        chat_id,

        "❓ Comando não reconhecido.\n\n"
        "Use /ajuda para ver os comandos."
    )



async def monitorar_bot():

    print(
        "🤖 Bot iniciado."
    )


    offset = None


    while True:

        try:

            atualizacoes = (
                await bot_obter_updates(
                    offset
                )
            )


            for update in atualizacoes:

                offset = (
                    update["update_id"] + 1
                )


                mensagem = update.get(
                    "message"
                )


                if not mensagem:

                    continue


                texto = mensagem.get(
                    "text"
                )


                if not texto:

                    continue


                chat = mensagem.get(
                    "chat",
                    {}
                )


                chat_id = chat.get(
                    "id"
                )




                if not texto.startswith(
                    "/"
                ):

                    continue


                print(
                    f"Comando recebido "
                    f"no chat {chat_id}: "
                    f"{texto}"
                )


                await processar_comando(
                    chat_id,
                    texto
                )


        except Exception as erro:

            print(
                f"[ERRO BOT] {erro}"
            )

            await asyncio.sleep(
                5
            )




async def monitorar_canal(
    canal_id,
    nome,
    progresso
):

    try:

        canal = await client.get_entity(
            canal_id
        )

    except Exception as erro:

        print(
            f"[ERRO] Não foi possível "
            f"acessar {nome}: {erro}"
        )

        return


    canal_id_str = str(
        canal_id
    )




    if canal_id_str in progresso:

        ultima_mensagem_id = (
            progresso[
                canal_id_str
            ]
        )


        print(
            f"Continuando {nome} "
            f"a partir da mensagem "
            f"{ultima_mensagem_id}"
        )


    else:

        mensagens = await client.get_messages(
            canal,
            limit=1
        )


        if mensagens:

            ultima_mensagem_id = (
                mensagens[0].id
            )

        else:

            ultima_mensagem_id = 0


        progresso[
            canal_id_str
        ] = ultima_mensagem_id


        salvar_progresso(
            progresso
        )


        print(
            f"Primeiro monitoramento de "
            f"{nome}. Última mensagem atual: "
            f"{ultima_mensagem_id}"
        )


    print(
        f"Monitorando: {nome}"
    )



    while True:

        try:

            mensagens_novas = []


            async for mensagem in client.iter_messages(
                canal,
                min_id=ultima_mensagem_id,
                reverse=True
            ):

                mensagens_novas.append(
                    mensagem
                )


            for mensagem in mensagens_novas:

                texto = (
                    mensagem.text or ""
                )


                texto_minusculo = (
                    texto.lower()
                )


                palavras_chave = (
                    carregar_palavras_chave()
                )


                palavras_encontradas = [
                    palavra
                    for palavra in palavras_chave
                    if palavra in texto_minusculo
                ]




                if palavras_encontradas:

                    print(
                        "\n"
                        + "!" * 60
                    )


                    print(
                        "PALAVRA-CHAVE "
                        "ENCONTRADA!"
                    )


                    print(
                        f"CANAL: {nome}"
                    )


                    print(
                        f"ID: {mensagem.id}"
                    )


                    print(
                        "PALAVRAS: "
                        f"{', '.join(palavras_encontradas)}"
                    )


                    print()


                    print(
                        texto
                    )


                    print(
                        "!" * 60
                    )



                    enviado = (
                        await enviar_promocao_bot(
                            nome,
                            palavras_encontradas,
                            texto,
                            mensagem
                        )
                    )


                    if enviado:

                        print(
                            "✅ Promoção enviada "
                            "para o chat do bot."
                        )

                    else:

                        print(
                            "❌ Falha ao enviar "
                            "promoção para o bot."
                        )





                ultima_mensagem_id = (
                    mensagem.id
                )


                progresso[
                    canal_id_str
                ] = ultima_mensagem_id


                salvar_progresso(
                    progresso
                )


        except Exception as erro:

            print(
                f"[ERRO] {nome}: {erro}"
            )


        await asyncio.sleep(
            5
        )




async def iniciar_monitoramento():

    progresso = (
        carregar_progresso()
    )


    canais = (
        carregar_canais()
    )


    tarefas = []


    for canal_id, dados in canais.items():

        nome = dados.get(
            "nome",
            "Canal sem nome"
        )


        tarefa = asyncio.create_task(
            monitorar_canal(
                int(canal_id),
                nome,
                progresso
            )
        )


        tarefas.append(
            tarefa
        )


    if not tarefas:

        print(
            "⚠️ Nenhum canal cadastrado."
        )

    else:

        print(
            f"📢 {len(tarefas)} "
            "canal(is) sendo monitorado(s)."
        )


    await asyncio.gather(
        *tarefas
    )



async def main():

    tarefa_bot = asyncio.create_task(
        monitorar_bot()
    )


    tarefa_monitor = asyncio.create_task(
        iniciar_monitoramento()
    )


    await asyncio.gather(
        tarefa_bot,
        tarefa_monitor
    )



try:

    with client:

        client.loop.run_until_complete(
            main()
        )


except KeyboardInterrupt:

    print(
        "\nMonitor encerrado."
    )