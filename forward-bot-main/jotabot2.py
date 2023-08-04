# Modulos
import telebot
from telebot import types
import threading
from config import telegram_token, chat_id_grupo_personal, chat_id_grupo_forward

####################################################  
 
"""CREACION DEL OBJETO BOT E INSTANCIADO EN TELEGRAM"""

#instanciar el bot en tg
bot = telebot.TeleBot(telegram_token,parse_mode=None)
bot_activo = True

####################################################

#Botones
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder= "Pulsa un botón")
boton_1 = types.KeyboardButton("📩INICIAR📩")
boton_2 = types.KeyboardButton("🛑ACT/DES🛑")


#Cuadricula de botones
markup.row(boton_1,boton_2)


# Comandos de los botones
# Respuesta a los mensajes (no comandos) (y respuesta a los botones sin la / de comando)
@bot.message_handler(func=lambda message: True, content_types=["text"])
def Mensajes_De_texto(message):
    global bot_activo

    # Verificación estado del bot
    if message.text == "🛑ACT/DES🛑":
        toggle_bot(message)
    elif bot_activo:
        # Gestiona los mensajes de texto recibidos
        # Respuesta para los mensajes que no son comandos (no tienen /) y que no están registrados para funcionar
        if message.text.startswith("/"):
            bot.send_message(message.chat.id, "introduce un comando válido")
        # Respuesta para el botón iniciar
        elif message.text == "📩INICIAR📩":
            send_welcome(message)
    else:
        bot.send_message(message.chat.id, "El bot está detenido. Presiona el botón para activarlo.")


# Comandos start y togglebot

def enviar_estado():
    global bot_activo
    estado = "activo" if bot_activo else "detenido"
    bot.send_message(chat_id_grupo_personal, f"El bot está {estado}.")



#Comando start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    #Da la bienvenida al usuario del bot
    bot.reply_to(message, ("Bienevenido al bot signal-forward de jota, creado por Jesus Bruzon <3"), reply_markup = markup)

@bot.message_handler(commands=['togglebot'])
def toggle_bot(message):
    global bot_activo  # Indica que se usará la variable global bot_activo

    bot_activo = not bot_activo  # Invierte el valor de bot_activo

    estado = "activado" if bot_activo else "detenido"
    bot.send_message(message.chat.id, f"El bot ha sido {estado}.")
    enviar_estado()


# Función principal del bot

"""COMPROBADOR DE MENSAJES INFINITO"""

def recibir_mensajes():
    #Bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()    

    
########################################################

"""FUNCION PRINCIPAL DEL BOT"""

#MAIN
if __name__ == "__main__":
    print("iniciando el bot")
    #ponemos el comprobador de mensajes entrantes en segundo plano
    hilo_bot = threading.Thread(name="telegram_hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print("Porfavor no apagues el dispositivo, ni cierres esta ventana . . . 100%")
    print("""Este bot ha sido desarrollado para jota broker
          por Jesus Bruzon Guerrero""")
    

    """FIN DEL SCRIPT"""
