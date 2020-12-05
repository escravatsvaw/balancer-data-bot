#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple telegram bot to read crypto currencies prices and liquidity
"""
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
import graph_api
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def price(bot, update, args):

    if len(args) == 0:
        err_msg = 'You should specify coin ticker\n'
        err_msg += '/price <coin>'
        bot.send_message(chat_id=update.message.chat_id, text=err_msg)
        return

    coin = args[0].upper()
    coin_info = graph_api.get_token_info(coin)

    if len(coin_info) == 0:
        bot.send_message(chat_id=update.message.chat_id, text=f'Couldn\'t find coin {coin}!')
        return
    else:
        coin_info = coin_info[0]

    usd = float(coin_info['price'])
    pool_liquidity = float(coin_info['poolLiquidity'])

    msg = f'{coin_info["name"]} ({coin}): \n'
    msg += f'Price: {usd:.3f} $\n'
    msg += f'Liquidity: {pool_liquidity:.3f} $\n'
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def start(bot, update):
    msg = 'This bot provides token price and liquidity on the Bancor platform.\n'
    msg += 'Bot uses api from the subgraph https://thegraph.com/explorer/subgraph/balancer-labs/balancer\n\n'
    msg += 'To get data use command /price TOKEN-NAME\n'
    msg += 'For example: /price YFI'
    update.message.reply_text(msg)

def help(bot, update):
    update.message.reply_text('/price <coin> - to get coin price and liquidity')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # EventHandler
    updater = Updater(os.environ['BALANCER_DATA_BOT_TOKEN'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands
    dp.add_handler(CommandHandler("price", price, pass_args=True))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print('Bot is running')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
