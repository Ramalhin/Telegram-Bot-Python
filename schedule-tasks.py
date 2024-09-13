import schedule
import time
from threading import Thread
from database.mongo import listar_canais_aprovados


def enviar_lista(bot):
    categorias = listar_canais_aprovados().distinct('categoria')
    for categoria in categorias:
        canais = listar_canais_aprovados().find({'categoria': categoria})
        lista_canais = "\n".join([f"{canal['nome']} - {canal['link']}" for canal in canais])
        bot.send_message(chat_id, f"Categoria: {categoria}\n{lista_canais}")


# Função para rodar as tarefas agendadas
def job_divulgar_canais(bot):
    schedule.every().day.at("10:00").do(enviar_lista, bot=bot)


def start_scheduler(bot):
    t = Thread(target=run_scheduler, args=(bot,))
    t.start()


def run_scheduler(bot):
    job_divulgar_canais(bot)
    while True:
        schedule.run_pending()
        time.sleep(1)
