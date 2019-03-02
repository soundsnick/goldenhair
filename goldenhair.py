# -*- coding: utf-8 -*-

import vk, requests, random, json, threading
from pprint import pprint
import time
import argparse
import sys
import os
import subprocess as s




# ApiConfig
# __token: VK user access_token
# __version: VK API version
ApiConfig = {
    'token': 'USERS_VK_ACCESS_TOKEN',
    'version': '5.80',
    'myid': 'MY_VK_ID'
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
                if int(mes['from_id']) == ApiConfig['myid']:
                    print("\033[1;30;43m "+fromus+' \033[0m', end='')
                else:
                    print("\033[1;30;42m "+fromus+' \033[0m', end='')
                if mes['text'] != '':
                    print(' : '+mes['text']+' ', end='')
                else:
                    if 'sticker' in mes['attachments'][0]:
                        print(' : STICKER | '+mes['attachments'][0]['sticker']['images'][4]['url']+' ', end='')
                    else:
                        print(mes['attachments'], end='')
                print("\033[1;32;29m "+time.strftime('%Y-%m-%d %H:%M', time.localtime(mes['date']))+' \033[0m')
                time.sleep(1)
    if cmd == "longpoll":
        data = requests.get('https://api.vk.com/method/messages.getLongPollServer',
                            params={'access_token': ApiConfig['token'], 'v': ApiConfig['version']}).json()['response']
        while True:
            response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data['server'], key=data['key'], ts=data['ts'])).json()  # отправление запроса на Long Poll сервер со временем ожидания 20 и опциями ответа 2
            updates = response['updates']
            if updates:
                for element in updates:
                    # __Checking update for message
                    # print(element)
                    if element[0] == 4:
                        fromu = vkapi.users.get(user_ids=element[3], access_token=ApiConfig['token'], v=ApiConfig['version'])[0]
                        fromus = fromu['first_name'] + ' ' + fromu['last_name']
                        if element[2] == 51:
                            print("\033[1;30;43m Me -> "+fromus+' \033[0m', end='')
                        else:
                            print("\033[1;30;42m "+fromus+' -> Me \033[0m', end='')
                        print(' : '+element[5]+' ', end='')
                        print("\033[1;32;29m "+time.strftime('%Y-%m-%d %H:%M', time.localtime(element[4]))+' \033[0m')
                        # s.call(['notify-send', fromus,element[5]])
                        data['ts'] = response['ts']
