# Python wrapper for Cobinhood REST API

Following wrapper created based on version of API documentation published at February 2018. Cover all endpoints provided by official documentation.
- tickers , orderbook , market stats with public API.
- create, alter and cancel orders.
- viewing your orders and fills
- viewing your wallets and transactions

### Prerequests
Only other library you need to have this API work is "requests" library. This library is easily installed with pip
package manager
```
pip3 install requests
```

### Lets dig into public API

Project comes with set of runnable scripts which shows pretty much whole thing, but for those who love
readme's there are few sample usages down below

#### Get ticker for a given market pair
```
import cobinhood_api.cobinhood as cobinhood
api = cobinhood.CobinhoodClient()

t1 = api.getTicker('BTC-USD')
t2 = api.getTicker('COB-ETH')
print(t1)
print(t2)
```
produced output
```
{'trading_pair_id': 'BTC-USD', 'timestamp': 1518644400000, '24h_high': '9550', '24h_low': '9550', '24h_open': '9550',
    '24h_volume': '0', 'last_trade_price': '9550', 'highest_bid': '9550.3', 'lowest_ask': '9550'}
{'trading_pair_id': 'COB-ETH', 'timestamp': 1518644400000, '24h_high': '0.0002682', '24h_low': '0.0002307',
'24h_open': '0.000267', '24h_volume': '944451.0111002001', 'last_trade_price': '0.0002504', 'highest_bid': '0.00025', 'lowest_ask': '0.0002505'}
```

#### Get orderbook for a given market pair
```
import cobinhood_api.cobinhood as cobinhood
api = cobinhood.CobinhoodClient()
ob1 = api.getMarketOrderBook('ETH-USD')
ob2 = api.getMarketOrderBook('COB-ETH',2)
print(ob1)
print(ob2)
```
produced output
```
a lot of entries for eth-usd order book
{'sequence': 0, 'bids': [['710', '1', '0.10316901'], ['200', '1', '0.07'], ['175', '1', '0.3'],  ... , ['0.01', '4', '262']], 'asks': [['720', '1', '51.19778993']]}
and just 2 top entries for cob-eth order book
{'sequence': 0, 'bids': [['0.0002501', '1', '300'], ['0.00025', '1', '200']], 'asks': [['0.0002508', '3', '2096'], ['0.0002509', '2', '6933']]}
```

#### Get list of currencies and pairs
```
import cobinhood_api.cobinhood as cobinhood
api = cobinhood.CobinhoodClient()
currencies = api.getMarketCurrencies()
pairs = api.getMarketTradingPairs()
print(currencies)
print(pairs)
```
produced output
```
[   
    {'currency': 'TRX', 'name': 'TRON', 'min_unit': '0.00000001', 'deposit_fee': '0', 'withdrawal_fee': '195.23'}, 
    ..... , 
    {'currency': 'STK', 'name': 'STK', 'min_unit': '0.00000001', 'deposit_fee': '0', 'withdrawal_fee': '53.13'}
]
[
    {'id': 'BAT-ETH', 'base_currency_id': 'BAT', 'quote_currency_id': 'ETH', 'base_max_size': '2764882.672', 'base_min_size': '82.946', 'quote_increment': '0.0000001'}, 
    ...., 
    {'id': 'COB-BTC', 'base_currency_id': 'COB', 'quote_currency_id': 'BTC', 'base_max_size': '4122776.277', 'base_min_size': '123.683', 'quote_increment': '0.00000001'}
]
```

#### Get candles
```
import cobinhood_api.cobinhood as cobinhood
api = cobinhood.CobinhoodClient()
hour_candles = candles = api.getChartCandles('ETH-USD')
day_candles = api.getChartCandles('ETH-USD',cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_1_DAY)
period_candles = api.getChartCandles('ETH-USD', cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_30_MINUTES, start_time=1514750400000, end_time=1514750400000 + 9000000)
print(hour_candles[0])
print(day_candles[0])
print(period_candles[0])
```
produced output
```
{'timeframe': '1h', 'trading_pair_id': 'ETH-USD', 'timestamp': 1515045600000, 'volume': '0', 'open': '999.92', 'close': '999.92', 'high': '999.92', 'low': '999.92'}
{'timeframe': '1D', 'trading_pair_id': 'ETH-USD', 'timestamp': 1513641600000, 'volume': '6.11643775', 'open': '200', 'close': '857.99', 'high': '898.98', 'low': '200'}
{'timeframe': '30m', 'trading_pair_id': 'ETH-USD', 'timestamp': 1514750400000, 'volume': '1.72', 'open': '770', 'close': '785', 'high': '785', 'low': '770'}
```

### Private API 

#### Create , modify and cancel order
```
import cobinhood_api.cobinhood as cobinhood
import time

API_KEY = "api key"
api = cobinhood.CobinhoodClient(api_key=API_KEY)
ticker = api.getTicker('COB-ETH')
last = float(ticker['last_trade_price'])
print(last)
order = api.placeOrder('COB-ETH', cobinhood.TRADING_ORDER_SIDE.SIDE_ASK, cobinhood.TRADING_ORDER_TYPE.TYPE_LIMIT, size=135, price=last * 3)
print("response : ",order)
if order is None:
    print("aborting")
order_id = order["id"]
print("go to browser and check your order. then order will be modified. aftre other 20 second order will be removed")
time.sleep(20)
is_modified = api.modifyOrder(order_id,size=135,price=last * 2)
print("modify success ?",is_modified)

time.sleep(20)
is_canceled = api.cancelOrder(order_id)
print("cancel success ?",is_canceled)
```
produced output
```
0.0002436
response :  {'id': '0aebf0d6-1f38-4b94-9d36-fe38f46fda5b', 'trading_pair': 'COB-ETH', 'side': 'ask', 'type': 'limit', 'price': '0.0007308', 'size': '135', 'filled': '0', 'state': 'queued', 'timestamp': 1518646692426, 'eq_price': '0', 'completed_at': None}
go to browser and check your order. then order will be modified. aftre other 20 second order will be removed
modify success ? True
cancel success ? True
```

#### View your past and present orders
```
import cobinhood_api.cobinhood as cobinhood
import time

API_KEY = "api key"
api = cobinhood.CobinhoodClient(api_key=API_KEY)

present = api.getOrders("COB-ETH")
past = api.getOrderHistory("COB-ETH")
print("present",present)
print("past",past)
id = None
for order in past:
    if order["state"] == "filled":
        id = order["id"]
        break
if id is None:
    quit()
trades = api.getOrderTrades(id)
for trade in trades:
    print("trade:",trade)
```
produced output
```
present [{'id': '74398191-233e-4e43-bc8f-301623b9b8c5', 'trading_pair': 'COB-ETH', 'side': 'ask', 'type': 'limit', 'price': '1', 'size': '200', 'filled': '0', 'state': 'open', 'timestamp': 1518647321854, 'eq_price': '0', 'completed_at': None}]
past [{'id': '0aebf0d6-1f38-4b94-9d36-fe38f46fda5b', 'trading_pair': 'COB-ETH', 'side': 'ask', 'type': 'limit', 'price': '0.0004872', 'size': '135', 'filled': '0', 'state': 'cancelled', 'timestamp': 1518646692426, 'eq_price': '0', 'completed_at': '2018-02-14T22:18:53.268879Z'}, ..., {'id': '45f01513-e482-49ce-b399-a6bc39aa9aa5', 'trading_pair': 'COB-ETH', 'side': 'bid', 'type': 'limit', 'price': '0.0002986', 'size': '133', 'filled': '133', 'state': 'filled', 'timestamp': 1518291578629, 'eq_price': '0.0002986', 'completed_at': '2018-02-10T19:54:27.770173Z'}]

trade: {'id': '333438c2-53be-4535-b5b6-f05419299934', 'maker_side': 'bid', 'ask_order_id': '75cfa41e-2d46-487a-8781-d32b26df5dbb', 'bid_order_id': '509650a9-7ad7-4c6f-805e-c435e288c554', 'timestamp': 1518320098924, 'price': '0.00027', 'size': '134.54925238'}
trade: {'id': 'b08fe8c2-b29f-4991-afc4-09ee28a00e28', 'maker_side': 'bid', 'ask_order_id': '6c123773-84c6-4243-8ae2-42966aa09565', 'bid_order_id': '509650a9-7ad7-4c6f-805e-c435e288c554', 'timestamp': 1518320585978, 'price': '0.00027', 'size': '0.45074762'}
```


#### Constructor and list of all available methods
```
    """
    constructor
    """
    def __init__(self,api_key=None,isLive=True,console_log=False,log_file_name="cobinhood.log",log_responses=False):
```
```
    """
    SYSTEM resource methods
    """
    def getSystemInfo(self):
    def getSystemTime(self):
```
```
    """
    Market resource methods
    """
    def getMarketCurrencies(self):
    def getMarketTradingPairs(self):
    def getMarketOrderBook(self,trading_pair,limit=50):
    def getMarketStats(self):
    def getAllLastPrices(self):
    def getTicker(self,trading_pair):
    def getRecentTrades(self,trading_pair):
```
```
    """
    CHART resource methods
    """
    def getChartCandles(self,trading_pair,timeframe=CHART_CANDLE_TIMEFRAME.TIMEFRAME_1_HOUR,start_time=None,end_time=None):
```
```
    """
    TRADING resource methods
    """
    def getOrders(self,trading_pair=None):
    def getOrder(self,order_id):
    def getOrderHistory(self,trading_pair=None):
    def getOrderTrades(self,order_id):
    def getTrade(self,trade_id):
    def getTradeHistory(self,trading_pair=None):
    def placeOrder(self,trading_pair,side,order_type,size,price=None):
    def cancelOrder(self,order_id):
    def modifyOrder(self,order_id,size,price):
```
```
    """
    WALLET resource methods
    """
    def getLedger(self,currency=None):
    def getDepositAddresses(self,currency=None):
    def getWithdrawalAddresses(self,currency=None):
    def getDepositHistory(self,currency=None):
    def getWithdrawalHistory(self,currency=None):
    def getWithdrawal(self,withdrawal_id):
    def getDeposit(self,deposit_id):
```

### Buy me some beer or coffee
```
ETH
0x7318932B90eB97a46DC2873D722B8B2cAeacbf92
```



