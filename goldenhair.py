# -*- coding: utf-8 -*-

import vk, requests, random, json, threading
from pprint import pprint
import time
import argparse
import sys
import os



# ApiConfig
# __token: VK user access_token
# __version: VK API version
ApiConfig = {
    'token': 'a26452685581733ea9f3f05057250fe5104a2793880e1689a9decffddf93f9d76b76e5dc22e28b02b6ea5',
    # 'token': '4321422f6a75aa06d4ef83317b88d39c7ad6f1fe96517d322f8f0efbd886204e6205d8ecf1f54c90d61d5',
    'version': '5.80',
    'conversation': 2000000045,
    'conversationShort': 45
}


session = vk.Session(access_token=ApiConfig['token'])
vkapi = vk.API(session, version=ApiConfig['version'])

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd")
    parser.add_argument("--user_id")
    parser.add_argument("--count")
    args = parser.parse_args()

    if not (args.cmd):
        print(" --- Command! ---")
        sys.exit(0)
    else:
        cmd = args.cmd
    if not (args.user_id):
      user_id = -1
    else:
      user_id = args.user_id
    if not (args.count):
      count = -1
    else:
      count = args.count
    return cmd, user_id, count

if __name__=="__main__":
    cmd, user_id, count = arguments()
    if cmd == "conversations":
        conversation = vkapi.messages.getConversations(access_token=ApiConfig['token'], v=ApiConfig['version'])
        for item in conversation['items']:
            if item['conversation']['peer']['id'] > 0:
                user = vkapi.users.get(user_ids=item['conversation']['peer']['id'], access_token=ApiConfig['token'], v=ApiConfig['version'])[0]
                name = user['first_name'] + ' ' + user['last_name']
                if len(name.split()) != 2:
                    name = item['conversation']['chat_settings']['title']
                mes = item['last_message']
                fromu = vkapi.users.get(user_ids=mes['from_id'], access_token=ApiConfig['token'], v=ApiConfig['version'])[0]
                fromus = fromu['first_name'] + ' ' + fromu['last_name']
                print("\033[1;30;42m "+name+' \033[0m', end='')
                print("\033[1;29;44m "+str(user['id'])+' \033[0m', end='')
                print("\033[1;30;43m "+fromus+' \033[0m', end='')
                print(' : '+mes['text'])
                time.sleep(1)
    if cmd == "mes":
        cmd, user_id, count = arguments()
        if int(user_id) < 0:
            print("WRONG USER ID")
        if int(count) < 0:
            print("WRONG COUNT")
        else:
            messages = vkapi.messages.getHistory(user_id=user_id, count=count, access_token=ApiConfig['token'], v=ApiConfig['version'])
            for mes in messages['items']:
                fromu = vkapi.users.get(user_ids=mes['from_id'], access_token=ApiConfig['token'], v=ApiConfig['version'])[0]
                fromus = fromu['first_name'] + ' ' + fromu['last_name']

                if int(mes['from_id']) == 293241527:
                    print("\033[1;30;43m "+fromus+' \033[0m', end='')
                else:
                    print("\033[1;30;42m "+fromus+' \033[0m', end='')
                print(' : '+mes['text']+' ', end='')
                print("\033[1;32;29m "+time.strftime('%Y-%m-%d %H:%M', time.localtime(mes['date']))+' \033[0m')
                time.sleep(1)
