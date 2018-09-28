#!/usr/bin/env python3
#-- coding:utf8 --
'''
Created on 2018年9月26日

@author: dev-lan
'''
import asyncio
import random
from www.orm import create_pool 
from www.models import User,Blog,Comment

async def test(loop):
    await create_pool(loop,user='root',password='root',db='awesome')
    u = User(name='Test01', email='test01@example.com', passwd='1234567890', image='about:blank')
    await u.save()
    
if __name__ == '__main__':
    loop =  asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([test(loop)]))
    loop.run_forever()
    print('Test finished.')
    loop.close()
    