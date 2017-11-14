# -*- coding: utf-8 -*-

import os
import telebot
import telebot
import requests
import urllib
import constants
import pymongo
import datetime
import json
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']

#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis


#       Your bot code below
# bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...
bot = telebot.TeleBot(constants.token)

client = MongoClient("mongodb://admin:admin@cluster0-shard-00-00-clzyx.mongodb.net:27017,cluster0-shard-00-01-clzyx.mongodb.net:27017,cluster0-shard-00-02-clzyx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

db = client.test_database
collection = db.test_collection

cena1 = 10
cena2 = 20

client = MongoClient("mongodb://admin:admin@cluster0-shard-00-00-clzyx.mongodb.net:27017,cluster0-shard-00-01-clzyx.mongodb.net:27017,cluster0-shard-00-02-clzyx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.btc9

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("koupit m", "koupit a", )
    bot.send_message(message.from_user.id, "Привет, друг! Зашел купить немного Андреев?", reply_markup=user_markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "koupit m":
        bot.send_message(message.from_user.id, "за 1г андреев - ", cena1)
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "На указанный ниже адрес тебе нужно заплатить посредством биткоина", reply_markup=hide_markup)
        parameters = {"confirmations": 3, }
        response = requests.get("https://bitaps.com/api/create/redeemcode", params=parameters)
        print(response.text)

        address = json.loads(response.text)['address']
        invoice = json.loads(response.text)['invoice']
        redeem_code = json.loads(response.text)['redeem_code']
        print(address)
        print(invoice)
        print(redeem_code)
        user_markup2 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup2.row("Нажми для обновления статуса платежа")
        bot.send_message(message.from_user.id, address, reply_markup=user_markup2)
        id = message.from_user.id
        print(id)
        url = 'https://bitaps.com/api/get/redeemcode/info'
        parameters = {'redeemcode': redeem_code}
        response = requests.post(url, data=json.dumps(parameters))
        print(response.text)
        balance = (json.loads(response.text)["balance"])
        print(balance)



        db.btc9.insert({"id": id,
                        "adrbtc": address,
                        "pay_code": invoice,
                        "balance": balance,
                        "invoice": invoice
                        })
    if message.text == "Нажми для обновления статуса платежа":
         id = message.from_user.id
         rezalt = db.btc9.find_one({'id': id})
         rezult = rezalt.get('balance')
         print(rezult)
         if rezult >= cena1:
                print("да")
                bot.send_message(message.from_user.id,
                         "Вы успешно заплатили за ваш заказ, сейчас вы получите сообщение с адресом закладки")
         elif rezult < cena1:
                print("нет")
                bot.send_message(message.from_user.id, "Деньги еще не получены, повторите через 10 минут")

    if message.text == "koupit a":
        bot.send_message(message.from_user.id, "за 2г максимов - 1 крон")
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "На указанный ниже адрес тебе нужно заплатить посредством биткоина", reply_markup=hide_markup)
        parameters = {"confirmations": 3, }
        response = requests.get("https://bitaps.com/api/create/redeemcode", params=parameters)
        print(response.text)

        address = json.loads(response.text)['address']
        invoice = json.loads(response.text)['invoice']
        redeem_code = json.loads(response.text)['redeem_code']
        print(address)
        print(invoice)
        print(redeem_code)

        bot.send_message(message.from_user.id, address)


@bot.message_handler(content_types=["text"])
def handle_obnova(message):
    if message.text == "Нажми для обновления статуса платежа":
        print('1')
        rezalt = db.btc9.find_one({'id': id})
        rezult = json.loads(rezalt)['balance']
        print(rezult)

        if rezult >= cena1:
            print("да")
            bot.send_message(message.from_user.id, "Вы успешно заплатили за ваш заказ, сейчас вы получите сообщение с адресом закладки")
        elif rezult < cena1:
            print("да")
            bot.send_message(message.from_user.id, "Деньги еще не получены, повторите через 10 минут")



bot.polling()
