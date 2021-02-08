""" Pagermaid currency exchange rates plugin. Plugin by @fruitymelon """

import asyncio, json
from json.decoder import JSONDecodeError
import urllib.request
from pyrogram import Client, filters
from main import cmd, par, des


cmd.extend(['rate'])
par.extend(['<FROM> <TO> <NB>'])
des.extend(['货币汇率。'])

API = "https://api.exchangeratesapi.io/latest"
currencies = []
data = {}

inited = False


def init():
    with urllib.request.urlopen(API) as response:
        result = response.read()
        try:
            global data
            data = json.loads(result)
            data["rates"][data["base"]] = 1.0
            for key in list(enumerate(data["rates"])):
                currencies.append(key[1])
            currencies.sort()
        except JSONDecodeError as e:
            raise e
        global inited
        inited = True


init()


@Client.on_message(filters.me & filters.command('rate', list('.:!')))
async def rate(client, message):
    while not inited:
        await asyncio.sleep(1)
    if len(message.text.split()) == 1:
        await message.edit(
            f"这是货币汇率插件\n\n使用方法: `-rate <FROM> <TO> <NB>`\n\n支持货币: \n{', '.join(currencies)}")
        return
    if len(message.text.split()) != 4:
        await message.edit(f"使用方法: `-rate <FROM> <TO> <NB>`\n\n支持货币: \n{', '.join(currencies)}")
        return
    FROM = message.text.split()[1].upper().strip()
    TO = message.text.split()[2].upper().strip()
    try:
        NB = float(message.text.split()[3].strip())
    except:
        NB = 1.0
    if currencies.count(FROM) == 0:
        await message.edit(
            f"{FROM}不是支持的货币. \n\n支持货币: \n{', '.join(currencies)}")
        return
    if currencies.count(TO) == 0:
        await message.edit(f"{TO}不是支持的货币. \n\n支持货币: \n{', '.join(currencies)}")
        return
    await message.edit(f'{FROM} : {TO} = {NB} : {round(data["rates"][TO]/data["rates"][FROM]*NB,2)}')
