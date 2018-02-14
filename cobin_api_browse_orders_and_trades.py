import cobinhood_api.cobinhood as cobinhood

API_KEY = "your key"
api = cobinhood.CobinhoodClient(api_key=API_KEY)

print("Following calls will help you understand basics of cobinhood_api REST API part related to viewing your current and past orders , trades , etc")

print ('getOrders method shows currently opened orders')
print ('getOrderHistory method shows past orders (filled , canceled, all of them) ')
print("      api.getOrders() : {result}".format(result=api.getOrders()))
print("api.getOrderHistory() : {result}".format(result=api.getOrderHistory()))

print("either of methods accept optional parameter - trading pair")
print("      api.getOrders('COB-ETH') : {result}".format(result=api.getOrders('COB-ETH')))
print("api.getOrderHistory('COB-ETH') : {result}".format(result=api.getOrderHistory('COB-ETH')))
print("you can use getOrder method to access single order by it's ID. require single parameter - order id")
print("      api.getOrder('some_order_id') : {result}".format(result=api.getOrders('some_order_id')))
print()
print("you can use getOrderTrades method to access all trades of given order. require single parameter - order id")
print("      api.getOrderTrades('some_order_id') : {result}".format(result=api.getOrderTrades('some_order_id')))
print("any trade can be accessed with help of getTrade method")
print("      api.getTrade('some_trade_id') : {result}".format(result=api.getTrade('some_trade_id')))
print()
print("getTradeHistory method let you browse trade history for all of your orders")
print("      api.getTradeHistory() : {result}".format(result=api.getTradeHistory()))
print("this method accept optionala parameter - trading pair")
print("      api.getTradeHistory('COB-ETH') : {result}".format(result=api.getTradeHistory('COB-ETH')))
print()
print("thats all")
