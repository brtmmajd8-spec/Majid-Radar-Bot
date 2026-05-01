import telebot
import requests
import time

# التوكن الخاص بك تم وضعه هنا بشكل صحيح
API_TOKEN = '8630247037:AAGETKlpW-ZVLQRXlRgehnLCn7de0s10hMk'

bot = telebot.TeleBot(API_TOKEN)

def get_binance_data(symbol):
    symbol = symbol.upper().replace('USDT', '')
    clean_symbol = f"{symbol}USDT"
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={clean_symbol}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), symbol
        return None, symbol
    except:
        return None, symbol

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = "👋 أهلاً بك! أنا رادار ماجد 🛰️\n\nأرسل رمز العملة (مثال: BTC أو SOL) للحصول على التحليل."
    bot.reply_to(message, welcome_msg)

@bot.message_handler(func=lambda message: True)
def handle_prices(message):
    user_input = message.text.strip()
    data, coin_name = get_binance_data(user_input)
    
    if data:
        price = float(data['lastPrice'])
        change = float(data['priceChangePercent'])
        high = float(data['highPrice'])
        low = float(data['lowPrice'])
        volume = float(data['quoteVolume'])
        
        target1 = price * 1.05
        target2 = price * 1.10
        stop_loss = price * 0.95
        
        response = f"🛰️ **تحليل عملة {coin_name}**\n"
        response += f"______________________\n\n"
        response += f"💰 الدخول: {price:.4f}$\n"
        response += f"🎯 الهدف 1: {target1:.4f}$\n"
        response += f"🎯 الهدف 2: {target2:.4f}$\n"
        response += f"🛑 الاستوب: {stop_loss:.4f}$\n"
        response += f"______________________\n\n"
        response += f"📈 التغير: {change}%\n"
        response += f"🐋 الحيتان: تدفق إيجابي ✅\n"
        response += f"______________________\n\n"
        response += f"✨ بسم الله وفالك التوفيق"
        
        bot.reply_to(message, response, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ الرمز {user_input} غير مدعوم على Binance.")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(5)
