from . import chat
from pyrogram import Client, filters
from string import Template
from utils import dirs, json_helper


def launch(bot, module_name):
    config = json_helper.read(dirs.MODULES_PATH + module_name + '/config.json')

    if 'api_key' in config:
        subconscious = chat.Subconscious(config['api_key'])

    @bot.app.on_message(filters.command('gpt', prefixes='.') & filters.me)
    def gpt(client, message):
        data = message.text.split(' ', maxsplit=2)
        mode = data[1]

        if mode == 'set_api_key':
            api_key = data[2]

            config['api_key'] = api_key
            json_helper.write(dirs.MODULES_PATH + module_name + '/config.json', config)

            subconscious = chat.Subconscious(config['api_key'])

            with open(dirs.MODULES_PATH + module_name + '/templates/success.html', encoding='utf-8') as f:
                message.edit(f.read())

    @bot.app.on_message(filters.command('ask', prefixes='.') & filters.me)
    def ask(client, message):
        data = message.text.split(' ', maxsplit=1)
        prompt = data[1]

        with open(dirs.MODULES_PATH + module_name + '/templates/loading.html', encoding='utf-8') as f:
            message.edit(f.read())

        try:
            response = subconscious.stream(prompt, subconscious)

            message.edit('ㅤ\n<b><emoji id="5282843764451195532">🖥</emoji> Ответ от нейросети:</b>\n\n' + response + 'ㅤ')
        except Exception as e:
            with open(dirs.MODULES_PATH + module_name + '/templates/warning.html', encoding='utf-8') as f:
                message.edit(f.read())
