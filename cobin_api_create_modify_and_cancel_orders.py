import cobinhood_api.cobinhood as cobinhood
import time

API_KEY = "your api key here"
api = cobinhood.CobinhoodClient(api_key=API_KEY, console_log=True)

print("Executing sample program which will place limit order , pause few seconds before altering it.")
print("Then it will pause another few seconds before removing order.")

ticker = api.getTicker('COB-ETH')
last = float(ticker['last_trade_price'])

print("executing api.placeOrder('COB-ETH',cobinhood_api.TRADING_ORDER_SIDE.SIDE_ASK,cobinhood_api.TRADING_ORDER_TYPE.TYPE_LIMIT,135,last * 3) .....")
order = api.placeOrder('COB-ETH', cobinhood.TRADING_ORDER_SIDE.SIDE_ASK, cobinhood.TRADING_ORDER_TYPE.TYPE_LIMIT, size=135, price=last * 3) # willing to sell 42 COB's . 3 times more expensive than 'last' price
print("response : ",order)
if order is None:
    print("aborting")
order_id = order["id"]
print("Sleeping 20 seconds before executing api.modifyOrder. Meanwhile you can check out placed order in your exchange screen")
time.sleep(20)
print("executing api.modifyOrder(order_id,135,last * 2)")
is_modified = api.modifyOrder(order_id,size=135,price=last * 2)
print("Success ?",is_modified)

print("Sleeping 20 seconds before executing api.cancelOrder(order_id). Meanwhile you can check out modified order in your exchange screen")
time.sleep(20)
is_canceled = api.cancelOrder(order_id)
print("Success ?",is_canceled)
print()
print()

print("Now lets execute market order")
order = api.placeOrder('MANA-BTC', cobinhood.TRADING_ORDER_SIDE.SIDE_BUY, cobinhood.TRADING_ORDER_TYPE.TYPE_MARKET, size=500)
print("api.placeOrder('MANA-BTC',cobinhood_api.TRADING_ORDER_SIDE.SIDE_BUY,cobinhood_api.TRADING_ORDER_TYPE.TYPE_MARKET,size=500)",order)
print()
print("Thats all for order placement , modifications and canceling")

