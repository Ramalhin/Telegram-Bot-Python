import pymongo
from config import MONGO_URI

# Conectando ao MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client['divulgacao_bot']
channels_collection = db['channels']
users_collection = db['users']

def cadastrar_usuario(user_id, chat_id, estado):
    users_collection.insert_one({
        "user_id": user_id,
        "chat_id": chat_id,
        "estado": estado
    })

def cadastrar_canal(nome, link, categoria, chat_id):
    channels_collection.insert_one({
        "nome": nome,
        "link": link,
        "categoria": categoria,
        "chat_id": chat_id,
        "aprovado": False
    })

def listar_canais_aprovados():
    return channels_collection.find({'aprovado': True})
