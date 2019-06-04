import requests
import time


def huobi():
    sell_url = 'https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMe' \
               'thod=0&currPage=1&coinId=2&tradeType=sell&blockType=general&online=1'
    buy_url = 'https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMe' \
              'thod=0&currPage=1&coinId=2&tradeType=buy&blockType=general&online=1'
    sell_rsp = requests.get(sell_url)
    buy_rsp = requests.get(buy_url)
    print('火币网')
    print('出售价格：', sell_rsp.json()['data'][0]['price'])
    print('购买价格：', buy_rsp.json()['data'][0]['price'])


def gateio():
    url = 'https://www.gateio.news/json_svr/query_push/?u=21&c=741038'
    data = {'type': 'push_order_list', 'symbol': 'USDT_CNY', 'big_trade': '0'}
    rsp = requests.post(url, data=data)
    print('gate.io')
    sell, buy = False, False
    for i in rsp.json()['push_order']:
        if not sell and i['type'] == 'buy':
            sell = True
            print('出售价格：', i['rate'])
        if not buy and i['type'] == 'sell':
            buy = True
            print('购买价格：', i['rate'])


def okex():
    sell_url = 'https://www.okex.me/v3/c2c/tradingOrders/book?t={}&side=buy&baseCurrency=usdt' \
               '&quoteCurrency=cny&userType=certified&paymentMethod=all'
    buy_url = 'https://www.okex.me/v3/c2c/tradingOrders/book?t={}&side=sell&baseCurrency=usdt' \
              '&quoteCurrency=cny&userType=certified&paymentMethod=all'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    t = int(time.time() * 1000)
    sell_rsp = requests.get(sell_url.format(t), headers=headers)
    buy_rsp = requests.get(buy_url.format(t), headers=headers)
    print('okex')
    print('出售价格：', sell_rsp.json()['data']['buy'][0]['price'])
    print('购买价格：', buy_rsp.json()['data']['sell'][0]['price'])


huobi()
gateio()
okex()
