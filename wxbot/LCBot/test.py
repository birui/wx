#!/usr/bin/env python
import pickle

f = open('bot.pkl','rb')
account_info = pickle.load(f)
print(account_info['cookies']['wxsid'])
f.close()
