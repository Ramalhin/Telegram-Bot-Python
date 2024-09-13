from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
import config

app = Flask(__name__)

client = MongoClient(config.MONGO_URI)
db = client['divulgacao_bot']
channels_collection = db['channels']

@app.route('/')
def lista_canais():
    canais = channels_collection.find({'aprovado': False})
    return render_template('lista.html', canais=canais)

@app.route('/aprovar/<canal_id>')
def aprovar_canal(canal_id):
    channels_collection.update_one({'_id': canal_id}, {'$set': {'aprovado': True}})
    return redirect(url_for('lista_canais'))

if __name__ == '__main__':
    app.run(debug=True)
