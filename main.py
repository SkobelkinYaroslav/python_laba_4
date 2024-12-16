from flask import Flask, jsonify
from backend import QuoteAPI
from database import QuoteManagerDB
import sqlite3
app = Flask(__name__)

# Создание экземпляра нашего API класса
quote_api = QuoteAPI.BackendAPI(app)
QuoteManagerDB.create_tables()
app.run(debug=True)




