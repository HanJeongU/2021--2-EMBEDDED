#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    print(update.effective_user.id)

    print('Send SIGUSR1 to '+ sys.argv[1])
    os.kill(int(sys.argv[1]), signal.SIGUSR1)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def check(update: Update, context: CallbackContext) -> None:
    print("Sending user's data to server")
    socket.send(b"check")
    msg = socket.recv()
    print('client:', msg)

"""Start the bot."""
# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater("1448231342:AAEfxMMMamfiUgVNMWdWK2tWNn6aM2Ly9Xc", use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# on different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("check", check))

# on noncommand i.e message - echo the message on Telegram
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the Bot


# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
#updater.idle()

import cv2
import numpy as np
# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("yolov3.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading video
fourcc = cv2.VideoWriter_fourcc(*"XVID")
#out = cv2.VideoWriter("the_new_video_is.avi", fourcc , 25, (852, 480))

# repalce the test.mp4 with an video of your own 
camera = cv2.VideoCapture("fire1.mp4")

# Loading web cam
#camera = cv2.VideoCapture(0)
while True:
    _,img = camera.read()
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        
    objects = {}
    for i in indexes:
        i = i[0]
        label = str(classes[class_ids[i]])
        if label not in objects:
            objects[label] = 1
        else:
            objects[label] += 1
        if objects["Fire"]>=1 :
            print(objects)
            import telegram
            #telegram bot
            API_KEY = '1448231342:AAEfxMMMamfiUgVNMWdWK2tWNn6aM2Ly9Xc'
            msg="Warning! Warning Fire Fire detected you just check fire site!!"
            bot = telegram.Bot(token =API_KEY)
            chat_id ="1013693702"
            bot.sendMessage(chat_id= chat_id, text= "------------------------")
            bot.sendMessage(chat_id= chat_id, text= msg)
            import smtplib
            from email.mime.text import MIMEText
            import os, threading
            temp = os.popen("vcgencmd measure_temp").readline()
            msg1 = "RPI detected Temperature danger : " +temp+"''C"
            bot.sendMessage(chat_id= chat_id, text= "------------------------")
            bot.sendMessage(chat_id= chat_id, text= msg1)
            cv2.destroyAllWindows()
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()