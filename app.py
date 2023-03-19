from flask import Flask
from flask import request
from slack import WebClient
from utils import group_random, slack_channel_members, safeget, slack_users
import config
import time

app = Flask(__name__)
@app.route('/',)
def index():
  return "Welcome to 1v1 slack app"

@app.route('/schedule_1v1s',methods = ['POST'])
def schedule_1v1s():
  channel_id = request.form.get('channel_id')
  user_id = request.form.get('user_id')

  # logger
  print(f"User ran command: schedule_1v1s\nuser_id: {user_id}\nchannel_id: {channel_id}")

  slack_client = WebClient(config.SLACK_BOT_TOKEN)
  users_info = slack_users(slack_client)
  if not users_info: return "Failed to schedule"

  # logger
  print(f"email: {safeget(users_info, user_id, 'email')}")

  # check if user is allowed to execute command
  if safeget(users_info, user_id, 'email') not in config.ALLOWED_USERS:
    return "Not allowed to perform this action"

  channel_members = slack_channel_members(slack_client, channel_id)
  if not channel_members: return "Failed to schedule"

  channel_members_info = [safeget(users_info, user_id) for user_id in channel_members]
  
  # remove bot
  channel_members_info = list(filter(lambda user: not safeget(user, 'is_bot'), channel_members_info))
  
  # group members
  member_groups = group_random(channel_members_info)

  for i in range(1):
    slack_client.chat_postMessage(channel="U04U41MRT8S", text="Hey there :raised_hands:,\nWe have successfully found a match with <@U04U40W200J> for your 1v1 meet this weekend.", parse=True)
    time.sleep(1)

  return member_groups