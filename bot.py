from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import pymongo
import mercadopago
import schedule
import time
from threading import Thread

# Configurações iniciais
API_KEY = 'SUA_TELEGRAM_BOT_API_KEY'
MONGO_URI = 'mongodb+srv://ramalho-user1:<kC3W4Yq8ZG9ycaW>@cluster0.jkfhm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
MERCADO_PAGO_ACCESS_TOKEN = 'SEU_ACCESS_TOKEN_DO_MERCADO_PAGO'

# Configurando o MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client['divulgacao_bot']
channels_collection = db['channels']
users_collection = db['users']

# Configurando Mercado Pago
sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

# Iniciando o bot
application = Application.builder().token(API_KEY).build()
dispatcher = application

# Função de cadastro de canal
def cadastrar_canal(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    chat_id = update.message.chat_id
    # Verificar se o usuário já está cadastrado
    if users_collection.find_one({"user_id": user_id}):
        update.message.reply_text('Você já cadastrou seu canal.')
        return

    update.message.reply_text('Envie o nome e o link do seu canal para cadastrá-lo.')

    # Salvar o usuário temporariamente
    users_collection.insert_one({"user_id": user_id, "chat_id": chat_id, "estado": "aguardando_canal"})


# Função de aprovação de canal
def aprovar_canal(canal_id, context: CallbackContext):
    canal = channels_collection.find_one({"_id": canal_id})
    if canal:
        channels_collection.update_one({"_id": canal_id}, {"$set": {"aprovado": True}})
        context.bot.send_message(canal['chat_id'], 'Seu canal foi aprovado e está na lista de divulgação!')
    else:
        context.bot.send_message(canal['chat_id'], 'Seu canal não foi encontrado.')


# Função para enviar a lista de canais
def enviar_lista(update: Update, context: CallbackContext):
    categorias = channels_collection.distinct('categoria', {'aprovado': True})
    for categoria in categorias:
        canais = channels_collection.find({'categoria': categoria, 'aprovado': True})
        lista_canais = "\n".join([f"{canal['nome']} - {canal['link']}" for canal in canais])
        update.message.reply_text(f"Categoria: {categoria}\n{lista_canais}")


# Banir um usuário
def banir_usuario(user_id, context: CallbackContext):
    users_collection.update_one({"user_id": user_id}, {"$set": {"banido": True}})
    context.bot.send_message(user_id, "Você foi banido e não pode mais enviar canais.")


# Função de agendamento de divulgação
def job_divulgar_canais(context: CallbackContext):
    categorias = channels_collection.distinct('categoria', {'aprovado': True})
    for categoria in categorias:
        canais = channels_collection.find({'categoria': categoria, 'aprovado': True})
        lista_canais = "\n".join([f"{canal['nome']} - {canal['link']}" for canal in canais])
        context.bot.send_message(chat_id_grupo, f"Categoria: {categoria}\n{lista_canais}")


# Função para agendar tarefas automáticas
def schedule_tasks():
    # Exemplo: Enviar lista de canais a cada dia às 10h
    schedule.every().day.at("10:00").do(job_divulgar_canais)

    while True:
        schedule.run_pending()
        time.sleep(1)


# Configurar handlers
dispatcher.add_handler(CommandHandler('start', cadastrar_canal))
dispatcher.add_handler(CommandHandler('enviar_lista', enviar_lista))


# Iniciar o bot
def main():
    # Iniciando o agendamento em uma thread separada
    t = Thread(target=schedule_tasks)
    t.start()

    application.run_polling()


if __name__ == '__main__':
    main()
