import telebot
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


TOKEN ='6793630195:AAHx_qd7-G9Xkb1QHrOoDuLmoYFvhoI7VEg' #list am new info bot
bot = telebot.TeleBot(token = TOKEN)


def parse_html(url):
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = Request(url, headers=headers)
            response = urlopen(req)
            html_content = response.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            products = []

            for div in soup.find_all('div', {'class': 'dl', 'id': None}):
                if not div.find_parents('div', {'id': 'tp'}):
                    for a in div.find_all('a', href=True):
                        price_div = a.find('div', {'class': 'p'})
                        div_elements = a.find_all('div')
                        if len(div_elements) >= 3 and price_div:
                            product_name = div_elements[1].text.strip()
                            price = price_div.text.strip()
                            link = a['href']
                            full_link = f"list.am{link}"
                            products.append((product_name, price, full_link))
            return products

        except Exception as e:
            print(f"Error with parsing html data: {e}")
            time.sleep(63)
            continue

def send_updates(chat_id):
    url = "https://www.list.am/category/11?n=1&cmtype=1&bid=0&gl=2&srt=3"
    product_list = parse_html(url)
    if product_list:
        last_content = product_list[0][2]
        print(f'Printing first last content - {' - '.join(product_list[0])}')
        time.sleep(15)
    else:
        time.sleep(15)

    while True:
        product_list2 = parse_html(url)
        if product_list2:
            if product_list2[0][2] == last_content:
                print(f'{datetime.now().strftime('%H:%M')} - No changes')
                print(f'Last content - {' - '.join(product_list2[0])}')
                time.sleep(57)
            else:
                i = 1
                new_data_list = [product_list2[0]]
                while True:
                    if product_list2[i][2] == last_content:
                        for a in range(len(new_data_list)):
                            print(f'{datetime.now().strftime('%H:%M')} NEW content - {' - '.join(new_data_list[a])}')
                            bot.send_message(chat_id, ' - '.join(new_data_list[a]))
                        break
                    else:
                        new_data_list.append(product_list2[i])
                        i += 1                
                last_content = new_data_list[0][2]
                time.sleep(58)
        else:
            time.sleep(120)


@bot.message_handler(commands=['command1', 'start'])
def send_welcome(message):
    bot.reply_to(message, f'Privet {message.from_user.first_name} jan, mna kapi mej, taza baner@ kuxarkem, knopka ban chsxmes')
    chat_id = message.chat.id
    send_updates(chat_id)  

# Start the bot
bot.polling(non_stop=True)




# if __name__ == '__main__':
#     send_updates('https://www.list.am/category/11?n=1&cmtype=1&bid=0&price1=&price2=&crc=&_a31=0&_a30=0&gl=2')
