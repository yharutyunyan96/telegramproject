import telebot
import time
from datetime import datetime
from bs4 import BeautifulSoup

from urllib.request import urlopen, Request

TOKEN ='7048967212:AAGj3E0hdbgDKw-ATzGfDNOQ_GzplUx3Uik' #financebot
bot = telebot.TeleBot(token = TOKEN)


# @bot.message_handler()
# def info(message):
#     dicti = {
#         'barev': f'Privet {message.from_user.first_name} jan',
#         'privet': f'Privet {message.from_user.first_name} jan',
#         'inchka?': 'Ban che du asa',
#         'inch ka?':'Ban che du asa'
#     }
#     try:
#         bot.send_message(message.chat.id, dicti[message.text.lower()])
#     except Exception as e:
#         bot.send_message(message.chat.id, 'Chem jogum inch es asum')


def parse_html(url):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = Request(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            exchange_section = soup.find('section', class_='exchange_tab_container')

            if exchange_section:
                currency_div = exchange_section.find('div', class_='inline_txt')
                tds = exchange_section.find_all('td')

                numbers = [td.get_text(strip=True) for td in tds[1:4]]  # Second, third, and fourth td elements
                required_html = f"{currency_div.prettify()}\n{' '.join(map(str, tds[1:4]))}"

                content_dict = {
                    'raw_html': exchange_section.prettify(),
                    'required_html': required_html,
                    'numbers': {'ARQ': numbers[0], 'VACHARQ': numbers[1], 'CBA': numbers[2]}
                }
            else:
                content_dict = {
                    'raw_html': "Section with class 'exchange_tab_container' not found.",
                    'required_html': "",
                    'numbers': ""
                }

            return content_dict

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(63)
            continue
        

def send_updates(chat_id):
    url = "https://www.aeb.am/"  # or any example url
    last_content = {'raw_html': "", 'required_html': "", 'numbers': ""}

    while True:
        content_dict = parse_html(url)

        if content_dict:
            current_time = datetime.now().strftime('%H:%M')
            listik = [float(i) for i in content_dict['numbers'].values()]

            print('-'*41)
            print(f'{"Time":<8} | {"Buy":<8} | {"Sell":<8} | {"CB":<8}')
            print(f'{current_time:<8} | {listik[0]:<8.2f} | {listik[1]:<8.2f} | {listik[2]:<8.2f}')
            print('-'*41)
            print()

            # Check if content has changed since the last check
            if content_dict['required_html'] != last_content.get('required_html', ''):
                bot.send_message(chat_id, f"առք` {listik[0]}, \nվաճառք` {listik[1]}, \nԿԲ` {listik[2]}")

            # Update the last content with the new raw HTML
            last_content['raw_html'] = content_dict['raw_html']
            last_content['required_html'] = content_dict['required_html']
            last_content['numbers'] = content_dict['numbers']

        time.sleep(60)  # Check for changes every minute

# Define the message handler for the /start command
@bot.message_handler(commands=['command1', 'start'])
def send_welcome(message):
    bot.reply_to(message, f'Պրիվետ {message.from_user.first_name} ջան հեսա ուղարկեմ դոլարի կուրսերը նայի')
    chat_id = message.chat.id
    send_updates(chat_id)  # Start sending updates to this chat

# Start the bot
bot.polling(non_stop=True)

