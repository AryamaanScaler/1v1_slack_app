from slack.errors import SlackApiError
import time
import random

def group_random(user_list, group_size=2, strict=True):
  random.shuffle(user_list)
  groups = [user_list[i:i+group_size] for i in range(0, len(user_list), group_size)]
  
  if strict: 
    groups = list(filter(lambda group: len(group) == group_size, groups))

  return groups

def safeget(dct, *keys):
  if not dct: return None

  for key in keys:
    try:
      dct = dct[key]
    except KeyError:
      return None
  return dct

def serialize_user(user):
  return {
    "id": safeget(user, 'id'),
    "name": safeget(user, 'name'),
    "real_name": safeget(user, 'real_name'),
    "first_name": safeget(user, 'profile', 'first_name'),
    "last_name": safeget(user, 'profile', 'last_name'),
    "email": safeget(user, 'profile', 'email'),
    "is_bot": safeget(user, 'is_bot')
  }

def slack_call(method, args={}, max_retries=3, wait=3):
  for retry in range(max_retries):
    try:
      response = method(**args)
      return response
    except SlackApiError as e:
      print(f"Retry: {retry+1}\nResponse: {e}")

    time.sleep(wait)

  return None

def slack_channel_members(slack_client, channel):
  response = slack_call(slack_client.conversations_members, {"channel": channel})
  return safeget(response, 'members')

def slack_users(slack_client):
  users_list = slack_call(slack_client.users_list)
  if not users_list: return None

  serialized_users = {}
  for user in safeget(users_list, 'members'):
    serialized_users[safeget(user, 'id')] = serialize_user(user)

  return serialized_users
