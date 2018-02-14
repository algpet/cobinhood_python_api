import urllib3
import requests
import time
import json
import logging
from enum import Enum

urllib3.disable_warnings()

# Live and Sandbox URL here. Sandbox does not work at all
LIVE_API = "https://api.cobinhood.com"
SANDBOX_API = "https://sandbox-api.cobinhood_api.com"

# API resources. SYSTEM
SYSTEM_INFO = "/v1/system/info"
SYSTEM_TIME = "/v1/system/time"

# API resources. MARKET
MARKET_CURRENCIES = '/v1/market/currencies'
MARKET_TRADING_PAIRS = '/v1/market/trading_pairs'
MARKET_ORDER_BOOK = '/v1/market/orderbooks/{trading_pair}?limit={limit}'
MARKET_STATS = '/v1/market/stats'
MARKET_TICKER = '/v1/market/tickers/{trading_pair}'
MARKET_RECENT_TRADES = '/v1/market/trades/{trading_pair}'

# API resources. CANDLES
CHART_CANDLES = '/v1/chart/candles/{trading_pair}?timeframe={timeframe}'

class CHART_CANDLE_TIMEFRAME(Enum):
    TIMEFRAME_1_MINUTE = "1m"
    TIMEFRAME_5_MINUTES = "5m"
    TIMEFRAME_15_MINUTES = "15m"
    TIMEFRAME_30_MINUTES = "30m"
    TIMEFRAME_1_HOUR = "1h"
    TIMEFRAME_3_HOURS = "3h"
    TIMEFRAME_6_HOURS = "6h"
    TIMEFRAME_12_HOURS = "12h"
    TIMEFRAME_1_DAY = "1D"
    TIMEFRAME_7_DAYS = "7D"
    TIMEFRAME_14_DAYS = "14D"
    TIMEFRAME_1_MONTH = "1M"

#[1m, 5m, 15m, 30m, 1h, 3h, 6h, 12h, 1D, 7D, 14D, 1M]

# API resources. TRADING
TRADING_ORDERS = '/v1/trading/orders'
TRADING_ORDER = '/v1/trading/orders/{order_id}'
TRADING_ORDERS_HISTORY = '/v1/trading/order_history'
TRADING_TRADE = '/v1/trading/trades/{trade_id}'
TRADING_TRADE_HISTORY = '/v1/trading/trades'
TRADING_ORDER_TRADES = '/v1/trading/orders/{order_id}/trades'


class TRADING_ORDER_SIDE(Enum):
    SIDE_BUY = "bid"
    SIDE_SELL = "ask"
    SIDE_BID = "bid"
    SIDE_ASK = "ask"


class TRADING_ORDER_TYPE(Enum):
    TYPE_MARKET = "market"
    TYPE_LIMIT = "limit"
    TYPE_STOP = "stop"
    TYPE_STOP_LIMIT = "stop_limit"
    #TYPE_TRAILING_STOP = "trailing_stop"  # according to docks this one is unavailable when placing via api ..
    #TYPE_FILL_OR_KILL = "fill_or_kill"    # according to docks this one is unavailable when placing via api ..


# API resources. WALLET
WALLET_DEPOSIT_ADDRESSES = '/v1/wallet/deposit_addresses'
WALLET_WITHDRAWAL_ADDRESSES = "/v1/wallet/withdrawal_addresses"
WALLET_LEDGER = "/v1/wallet/ledger"
WALLET_DEPOSIT = '/v1/wallet/deposits/{deposit_id}'
WALLET_WITHDRAWAL = '/v1/wallet/withdrawals/{withdrawal_id}'
WALLET_WITHDRAWALS = '/v1/wallet/withdrawals'
WALLET_DEPOSITS = '/v1/wallet/deposits'



class CobinhoodClient:
    """
    Init class object with live/sandbox URL
    """
    def __init__(self,api_key=None,isLive=True,console_log=False,log_file_name="cobinhood_api.log",log_responses=False):
        self.init_logging(console_log=console_log,log_file_name=log_file_name)
        self.log_responses = log_responses
        logging.info("")
        logging.info("STARTED")
        if isLive:
            self.path = LIVE_API
            logging.info("CONNECTION : LIVE")
        else:
            raise NotImplemented("Sandbox did not worked at time of development")
            self.path = SANDBOX_API
            logging.info("CONNECTION : SANDBOX")

        self.auth = None
        if api_key is not None:
            self.auth = {"authorization":api_key}
            logging.info("CONNECTION : AUTHENTICATED CONNECTION")
        else:
            logging.info("CONNECTION : UNAUTHENTICATED CONNECTION")

    def init_logging(self,console_log=False, log_file_name=None):

        if log_file_name is not None:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s : %(levelname)-8s :  %(message)s',
                                datefmt='%y-%m-%d %H:%M:%S',
                                filename=log_file_name,
                                filemode='a')
            if console_log:
                console = logging.StreamHandler()
                console.setLevel(logging.INFO)
                formatter = logging.Formatter('%(levelname)-8s : %(message)s')
                console.setFormatter(formatter)
                logging.getLogger('').addHandler(console)
        else:
            if console_log:
                logging.basicConfig(level=logging.INFO, format='%(levelname)-8s : %(message)s')
            else:
                logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s : %(message)s')


    """
    core stuff for later use
    """
    def request_headers(self):
        headers = {}
        headers["authorization"] = self.auth["authorization"]
        headers["nonce"] = str(int(time.time() * 1000000))
        return headers

    def request(self,method,request_url,params=None,data=None,auth=None):

        if auth and not self.auth:
            raise Exception("Not authenticated")

        if params is not None:
            request_url = request_url.format(**params)
        request_url = self.path + request_url

        if not auth:
            logging.info("REQUEST URL : {method} {request_url}"
                         .format(request_url=request_url,method=method))
            response = requests.request(method, request_url, verify=False).json()
        else:
            header = self.request_headers()
            if data is None:
                logging.info("REQUEST URL : {method} {request_url}"
                             .format(request_url=request_url, method=method))
                response = requests.request(method, request_url, verify=False, headers=header).json()
            else:
                logging.info("REQUEST URL : {method} {request_url} DATA : {data}"
                        .format(request_url=request_url,method=method,data=data))
                response = requests.request(method,request_url,verify=False,headers=header,data=json.dumps(data)).json()

        if self.log_responses:
            logging.info("RESPONSE : {response}".format(response=response))
            logging.info("")
        return response

    def get(self,request_url,params=None,auth=None):
        return self.request("get",request_url,params=params,auth=auth)

    def put(self,request_url,params=None,data=None,auth=True):
        return self.request("put",request_url,params=params,data=data,auth=auth)

    def post(self,request_url,params=None,data=None,auth=True):
        return self.request("post",request_url,params=params,data=data,auth=auth)

    def delete(self,request_url,params=None,auth=True):
        return self.request("delete",request_url,params=params,auth=auth)

    """
    more routines
    """
    def add_filter(self,filter,value,url,params):
        if value is not None:
            if url.find("?") == -1:
                url += "?"
            else:
                url += "&"
            url += filter + "={" + filter + "}"
            params[filter] = value
        return url


    """
    extract contents of API responce. Only cream go outside     
    """
    def result(self,request_result,entry=None):
        if request_result is None:
            return None
        if 'success' not in request_result or 'result' not in request_result:
            return None
        if entry is None:
            return request_result['result']
        else:
            return request_result['result'][entry]

    """
    check success for PUT / DELETE requests 
    """
    def outcome(self,request_result):
        if request_result is None:
            return False
        if 'success' not in request_result or 'result' not in request_result:
            return None
        return request_result['success']


    """
    SYSTEM resource methods
    """
    def getSystemInfo(self):
        response = self.get(SYSTEM_INFO)
        return self.result(response,'info')
    def getSystemTime(self):
        response = self.get(SYSTEM_TIME)
        return self.result(response)

    """
    Market resource methods
    """
    def getMarketCurrencies(self):
        response = self.get(MARKET_CURRENCIES)
        return self.result(response,'currencies')

    def getMarketTradingPairs(self):
        response = self.get(MARKET_TRADING_PAIRS)
        return self.result(response,'trading_pairs')

    def getMarketOrderBook(self,trading_pair,limit=50):
        response = self.get(MARKET_ORDER_BOOK,params={"trading_pair":trading_pair,"limit":limit})
        return self.result(response,'orderbook')

    def getMarketStats(self):
        response = self.get(MARKET_STATS)
        return self.result(response)

    def getAllLastPrices(self):
        prices = {}
        response = self.get(MARKET_STATS)
        result = self.result(response)
        if result is None:
            return None
        for trading_pair,stats in result.items():
            prices[trading_pair] = stats['last_price']
        return prices


    def getTicker(self,trading_pair):
        response = self.get(MARKET_TICKER, params={"trading_pair": trading_pair})
        return self.result(response,'ticker')

    def getRecentTrades(self,trading_pair):
        response = self.get(MARKET_RECENT_TRADES, params={"trading_pair": trading_pair})
        return self.result(response,'trades')

    """
    CHART resource methods
    """
    def getChartCandles(self,trading_pair,timeframe=CHART_CANDLE_TIMEFRAME.TIMEFRAME_1_HOUR,start_time=None,end_time=None):
        if type(timeframe) == CHART_CANDLE_TIMEFRAME:
            timeframe = timeframe.value
        params = {"trading_pair": trading_pair,"timeframe":timeframe}
        base_url = self.add_filter("start_time",start_time,CHART_CANDLES,params)
        base_url = self.add_filter("end_time", end_time, base_url, params)
        response = self.get(base_url,params=params)
        return self.result(response,"candles")

    """
    TRADING resource methods
    """
    def getOrders(self,trading_pair=None):
        params ={}
        base_url = self.add_filter("trading_pair_id",trading_pair,TRADING_ORDERS,params)
        response = self.get(base_url,params=params,auth=True)
        return self.result(response,"orders")

    def getOrder(self,order_id):
        params = {"order_id":order_id}
        response = self.get(TRADING_ORDER, params=params, auth=True)
        return self.result(response,"order")

    def getOrderHistory(self,trading_pair=None):
        params = {}
        base_url = self.add_filter("trading_pair_id",trading_pair, TRADING_ORDERS_HISTORY, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response,"orders")

    def getOrderTrades(self,order_id):
        params = {"order_id": order_id}
        response = self.get(TRADING_ORDER_TRADES, params=params, auth=True)
        return self.result(response, "trades")

    def getTrade(self,trade_id):
        params = {"trade_id": trade_id}
        response = self.get(TRADING_TRADE, params=params, auth=True)
        return self.result(response, "trade")

    def getTradeHistory(self,trading_pair=None):
        params = {}
        base_url = self.add_filter("trading_pair_id",trading_pair, TRADING_TRADE_HISTORY, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "trades")

    def placeOrder(self,trading_pair,side,order_type,size,price=None):

        if type(side) == TRADING_ORDER_SIDE:
            side = side.value
        if type(order_type) == TRADING_ORDER_TYPE:
            order_type = order_type.value

        if price is None and order_type != TRADING_ORDER_TYPE.TYPE_MARKET.value:
            raise AttributeError("Price should be set for all order types except TRADING_ORDER_TYPE.TYPE_MARKET")

        data = {
            "trading_pair_id":trading_pair,
            "side":side,
            "type":order_type,
            "price":str(price),
            "size":str(size)
        }
        response = self.post(TRADING_ORDERS,data=data)
        return self.result(response, "order")

    def cancelOrder(self,order_id):
        params = {"order_id": order_id}
        response = self.delete(TRADING_ORDER, params=params)
        return self.outcome(response)

    def modifyOrder(self,order_id,size,price):
        params = {"order_id":order_id}
        data = {
            "price":str(price),
            "size":str(size)
        }
        response = self.put(TRADING_ORDER,params=params,data=data)
        return self.outcome(response)


    """
    WALLET resource methods
    """
    def getLedger(self,currency=None):
        params = {}
        base_url = self.add_filter("currency", currency, WALLET_LEDGER, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "ledger")

    def getDepositAddresses(self,currency=None):
        params = {}
        base_url = self.add_filter("currency",currency, WALLET_DEPOSIT_ADDRESSES, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "deposit_addresses")

    def getWithdrawalAddresses(self,currency=None):
        params = {}
        base_url = self.add_filter("currency", currency, WALLET_WITHDRAWAL_ADDRESSES, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "withdrawal_addresses")

    def getDepositHistory(self,currency=None):
        params = {}
        base_url = self.add_filter("currency", currency, WALLET_DEPOSITS, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "deposits")

    def getWithdrawalHistory(self,currency=None):
        params = {}
        base_url = self.add_filter("currency", currency, WALLET_WITHDRAWALS, params)
        response = self.get(base_url, params=params, auth=True)
        return self.result(response, "withdrawals")

    def getWithdrawal(self,withdrawal_id):
        params = {"withdrawal_id":withdrawal_id}
        response = self.get(WALLET_WITHDRAWAL, params=params, auth=True)
        return self.result(response, "withdrawal")

    def getDeposit(self,deposit_id):
        params = {"deposit_id":deposit_id}
        response = self.get(WALLET_DEPOSIT, params=params, auth=True)
        return self.result(response, "deposit")




