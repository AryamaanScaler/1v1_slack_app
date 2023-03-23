from flask import Flask
from flask import request
from slack import WebClient

from utils import schedule_1v1, safeget, slack_users

import config
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def index():
  return "Welcome to 1v1 slack app"

@app.route('/schedule_1v1s',methods = ['POST'])
def schedule_1v1s():
  channel_id = request.form.get('channel_id')
  user_id = request.form.get('user_id')

  # logger
  print(f"User ran command: schedule_1v1s\nuser_id: {user_id}\nchannel_id: {channel_id}")

  slack_client = WebClient(os.environ.get('SLACK_BOT_TOKEN'))
  users_info = slack_users(slack_client)
  if not users_info: return "Failed to schedule"

  # logger
  print(f"email: {safeget(users_info, user_id, 'email')}")

  # check if user is allowed to execute command
  if safeget(users_info, user_id, 'email') not in config.ALLOWED_USERS:
    return "Not allowed to perform this action"

  thread = Thread(target=schedule_1v1, args=(slack_client, channel_id, users_info,))
  thread.daemon = True
  thread.start()

  return "1v1 have start searching :mag:"