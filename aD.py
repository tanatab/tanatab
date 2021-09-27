from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from details import api_id, api_hash, bot_token
from pyrogram.handlers import MessageHandler
from telegram import update
import time
from pyrogram.types import MessageEntity
from pyrogram.raw.types import InputMessagesFilterUrl
import re
from re import A, L, M, search
import os
import logging

#SELENIUM SETTINGS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = '/Users/davide/Desktop/chromedriver'


bot = Client("amz-bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)
global CHAT_ID 
CHAT_ID  = ''
global W1
W1 = "❌"

global W2
W2 = "❌"
W3 = "📥"

def W2_CHANG(client, message):
    global W2

    W2 = "✅"
    print(W2) 
    global keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'IMPOSTA CANALE{W1}', callback_data='IMPOSTA_CANALE')],
 
            [InlineKeyboardButton(text=f'IMPOSTA TAG ID{W2}', callback_data='IMPOSTA_TAG_ID'),
            InlineKeyboardButton(text=f'CREATE POST{W3}', callback_data='CREA_POST')],
        ])
    
    return W2, keyboard

def W1_CHANG(client, message):
    global W1
    W1 = "✅"


    print(W1)

    global keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'IMPOSTA CANALE{W1}', callback_data='IMPOSTA_CANALE')],
 
            [InlineKeyboardButton(text=f'IMPOSTA TAG ID{W2}', callback_data='IMPOSTA_TAG_ID'),
            InlineKeyboardButton(text=f'CREATE POST{W3}', callback_data='CREA_POST')],
        ])
    

    return W1, keyboard

global keyboard
keyboard = ''

    

@bot.on_message(filters.command(commands=['start']) & filters.private)
def start(client, message):

    global keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'IMPOSTA CANALE{W1}', callback_data='IMPOSTA_CANALE')],
 
            [InlineKeyboardButton(text=f'IMPOSTA TAG ID{W2}', callback_data='IMPOSTA_TAG_ID'),
            InlineKeyboardButton(text=f'CREATE POST{W3}', callback_data='CREA_POST')],
        ])

    global CHAT_ID
    #global message_ids
    

    message_ids=message.message_id  
    CHAT_ID=message.chat.id

    client.send_message(chat_id=CHAT_ID, text="scegli opzione", reply_markup=keyboard)
    return CHAT_ID,keyboard
    
global affiliate_tag
affiliate_tag=""
global baseURL
baseURL=('https://www.amazon.it/')
global pCode
pCode=""
link_prodotto_cercato_affiliato = baseURL+pCode+"/?tag="+affiliate_tag+"-21&psc=1"


global link 
link =  ""

global descrizione_post
descrizione_post = ""
global descrizione_post_confermata
descrizione_post_confermata = ""

global photo_post
photo_post = ""

global ID_post
ID_post =""

@bot.on_message(filters.regex("https://")& ~filters.forwarded)
def link_cristo_stronzo (client, message):
    global link 
    link = message.text.split()
    
    print(link)
    
    print ("cazzo")
    return link


@bot.on_callback_query(filters.regex("IMPOSTA_TAG_ID"))
def button2(client, message):
    global link
    global affiliate_tag 
    client.send_message(chat_id=CHAT_ID, text="Per impostare il tag-id invia un qualsiasi link affiliato con il tuo tag")  
    while 1<10:
        if link != "":
            print(link)
            q = re.search(r'(&tag=()[\w]*)', str(link))
            affiliate_tag = q.group(0)
            W2_CHANG(client, message)
            print(W2)
            client.send_message(chat_id=CHAT_ID, text=f"Tag id impostato con successo: {affiliate_tag}", reply_markup=keyboard)  
            print(affiliate_tag)
            link =  ""

            break
    return link, affiliate_tag




@bot.on_callback_query(filters.regex("CREA_POST"))
def button3(client, message):
    global baseURL
    global affiliate_tag

    client.send_message(chat_id=CHAT_ID, text="Per creare un post manda il link del prodotto amazon che vuoi postare")
    while 1<10:
        if link != "":    
            print(F'Prodotto cercato = {link}')
            m = re.search(r'(?:dp\/[\w]*)|(?:gp\/product\/[\w]*)', str(link))
            pCode = m.group(0)
            link_post_affiliato = baseURL+pCode+"/?tag="+affiliate_tag+"-21&psc=1"
            print(link_post_affiliato)
            bot.send_message(chat_id=CHAT_ID, text=F'''Creazione del post in corso...\n\nNon mandare messaggi finché non ti verrà inviata una conferma!\n(tempo d'attesa stimato:20-30s, altrimenti -> /help)''')
            
            #OPEN LINK BY SELENIUM 
            driver = webdriver.Chrome(PATH)
            
            driver.get(link_post_affiliato)
                    
            'SCRAPING INFORMATIONS: !!!'
 
            #cookie button
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "sp-cc-accept"))       
            )   
            finally:
                WebDriverWait(driver, 2)
                cookie_button.click()
                print("bottone biscotti cliccato")
 
            #TITOLO POST
            try:
                title = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )   
            finally:
                print("titolo trovato")
 
            #PREZZO POST
            try:
                price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "price"))
            )
            finally:
                print("prezzo trovato") 
    
 
            #VALUTAZIONE POST
     
            try:
                rating = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "averageCustomerReviews_feature_div")) 
            )
            except:
                bot.send_message(message.chat.id, 'Valutazione non trovata')
                print("valutazione non trovata")        
            finally:
                print("valutazione trovata")
    
 
            print('creazione foto post')
 
            #URL FOTO
            try:
                photo_url = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.ID, "landingImage"))
            )       
            except:
                bot.send_message(message.chat.id, 'Foto non trovata') # get_attribute('src')
                print("Foto non trovata")    
            finally:
                print("foto trovata")
                foto = photo_url.get_attribute('src')
            global descrizione_post
            descrizione_post =  F'{title.text} 👀 \nn\n{price.text} 💲 \n \n{rating.text} ⭐️⭐️⭐️⭐️⭐️ \n \nLink: {link_post_affiliato}' # - {rating}
            
            global photo_post
            photo_post = foto
            
            driver.quit()

            keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f'ELIMINA POST ❌', callback_data='elimina_post'),
                        InlineKeyboardButton(text=f'CONFERMA POST ✅', callback_data='conferma_post')],
                    ])

            print('post creato ;)')  
            bot.send_message(chat_id=CHAT_ID, text=f'''Post creato con successo, scegli''', reply_markup=keyboard_2)  
    
            return descrizione_post, photo_post

#contatori
c=0
def counter(message):
    global c 
    if c <= 10:
        c = c+1
        print(c)
        #bot.send_message(message.chat.id, F'''Post numero{c}''')
        return c 
 
    else:
        bot.send_message(message.chat.id, F'''ATTENZIONE, hai creato il numero massimo di post, quindi il primo post che hai creato è stato sostituito con questo! \n(Post numero{c})''')
        c = 0
        print(c)
        return c
o = 0  
def counter_orario(message):
    global o 
    if o <= 10:
        o = o+1
        print(o)
        #bot.send_message(message.chat.id, F'''Post numero{o}''')
        return o 
 
    else:
        bot.send_message(message.chat.id, F'''ATTENZIONE, hai creato il numero massimo di post, quindi il primo post che hai creato è stato sostituito con questo! \n(Post numero{c})''')
        o = 0
        print(o)
        return o 

global photo_post_confermata
photo_post_confermata = ""   
@bot.on_callback_query(filters.regex("conferma_post"))
def conferma_post(client, message):
    global ID_post
    ID_post = counter(message)
    global descrizione_post_confermata
    descrizione_post_confermata = descrizione_post
    global photo_post_confermata
    photo_post_confermata = photo_post
    bot.send_message(chat_id=CHAT_ID, text=f'''Post numero {ID_post} confermato! \nAdesso imposta l'ora a cui vuoi che il post venga pubblicato.\n\nScrivi orario=orario \n\nNON METTERE LO SPAZIO DOPO L'UGUALE E SCRIVI L'ORARIO NEL FORMATO hh:mm:ss\n\nES. orario12:42:00''')

def trova_orario_post(msg):
    for text in msg:
        if 'orario=' in text:
            return text
        elif'Orario=' in text:
            return text
        elif'ORAIO=' in text:
            return text

ID_orario_post= ""
orario_post = ""
@bot.on_message(filters.regex("orario="))
def ricevi_orario_post (client, message):
    texts = message.text.split()
    orario_post_splittato = trova_orario_post(texts)  #testo splittato        
 
    o_p = format(orario_post_splittato[7:]) # = ORARIO POST
 
    print(F'Orario post = {o_p}')
    global orario_post
    orario_post = o_p
    keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=f'SALVA POST', callback_data='SALVA_POST')],
                    ])

    bot.send_message(chat_id=CHAT_ID, text=F'''Orario settato con successo! Orario = {orario_post}\n\nOra usa: ''', reply_markup=keyboard_3)
 
    global ID_orario_post
    ID_orario_post = counter_orario(message)
 
    return orario_post,ID_orario_post


global orario_post1
orario_post1 = ""
global ID_definitivo
ID_definitivo = ""
global descrizione_post1
descrizione_post1 = ""
global foto_post1
foto_post1 = ""
@bot.on_callback_query(filters.regex("SALVA_POST"))
def salva_post(client, message):
    #mettere CLASSE con una funzione per post (10) così che ogni post abbia il suo while - casomai cambiare libreria time o studiare per creare un database con i post
 
    if ID_post == ID_orario_post:
        global ID_definitivo 
        ID_definitivo = ID_post
        #serie di if in base ad id per creare 10 variabili diverse che pubblicano post
        
        #POST 1
        if ID_definitivo == 1:
            global orario_post1 
            orario_post1 = orario_post
            bot.send_message(chat_id=CHAT_ID, text=F'''Post {ID_definitivo} salvato con successo!\n\nVerrà postato alle {orario_post1} \nUsa: \n- /lista_comandi \n- /help''')
 
            global descrizione_post1 
            descrizione_post1 = descrizione_post_confermata
            global foto_post1 
            foto_post1 = photo_post_confermata
            
            posta(client, message)

        return orario_post1
 
global break_key_1
break_key_1='' 

global a                 
a = ""                 
global now                 
now = "" 
 

@bot.on_callback_query(filters.regex("elimina_post"))
def elimina_post(message):
    bot.send_message(chat_id=CHAT_ID, text='''Post eliminato''', reply_markup=keyboard)
    descrizione_post = None 
    photo_post = None


@bot.on_callback_query(filters.regex("IMPOSTA_CANALE"))
def button1(client, message):
        #global message_ids
        client.send_message(chat_id=CHAT_ID, text="Per impostare o modificare il canale a cui inviare i post prima di tutto aggiungi il bot al canale e rendilo amministratore.\n\nFatto ciò inoltra un qualsiasi messaggio dal canale a questo bot")

global ID_canale
ID_canale = 0
#IMPOSTA_CANALE
@bot.on_message(filters.forwarded)
def my(client, Message):
    global W1, keyboard
    global ID_canale

    ID_canale = Message['forward_from_chat']['id']
    print (ID_canale)
    W1_CHANG(client, Message)
    print(W1)


    client.send_message(chat_id=CHAT_ID, text=F'''Bot collegato con successo al canale!\nChat id del canale= {ID_canale} \n\nAdesso prima di poter usare altri comandi devi impostare il link affiliato tramite /imposta_nuovo_link_affiliato \n\n Usa /help se hai bisogno d'aiuto''', reply_markup=keyboard )
    return ID_canale

def posta(client, message):
    global break_key_1, orario_post1 
    global ID_canale
        
    print (ID_canale)

    break_key_1 ='bloccata'
    while True:
        global a,now
        a = time.ctime()
        a= a.split()
        now = a[3]  
        #print(now) 
        #time.sleep(1)
        print(F'''ORARIO = {now}\nORARIO POST 1 = {orario_post1}''')
        if now == orario_post1:
            client.send_photo(chat_id=ID_canale, photo=foto_post1, caption = descrizione_post1, disable_notification = None, reply_to_message_id = None, reply_markup = None, parse_mode = None)
            break_key_1 = 'sbloccata'
            #if notifiche == 'attivate':
            #    bot.send_message(message.chat.id, F'''Post numero {ID_definitivo} postato con successo!\n\nUsa: \n- /lista_comandi \n- /help''')

 
        if break_key_1 == 'sbloccata' :
            print('ORARII GIUSTI TROVATI -- TUTTI I POST SONO STATI PUBBLICATI CON SUCCESSO! ;) ')
            break
 
        else:
            print(ID_canale)

            print('sto aspettando')
            time.sleep(1)


bot.run()

