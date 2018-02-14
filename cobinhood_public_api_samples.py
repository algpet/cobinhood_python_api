import cobinhood_api.cobinhood as cobinhood
api = cobinhood.CobinhoodClient()


print("Following calls will help you understand basics of public part of Cobinhood REST API")
print("")
print("getSystemInfo and getSystemTime are used to retrieve most basic information about server your are connected to")
print("api.getSystemInfo() : {result}".format(result=api.getSystemInfo()))
print("api.getSystemTime() : {result}".format(result=api.getSystemTime()))
print("")
print("getMarketCurrencies and getMarketTradingPairs let you to get list of available currencies and trading pairs")
print("  api.getMarketCurrencies() : {result}: ".format(result=api.getMarketCurrencies()))
print("api.getMarketTradingPairs() : {result}: ".format(result=api.getMarketTradingPairs()))
print()
print("getMarketStats and getAllLastPrices let you to get most basic market stats")
print("  api.getMarketStats() : {result}".format(result=api.getMarketStats()))
print()
print("getAllLastPrices let you to get current prices for all tickers")
print("  api.getAllLastPrices() : {result}".format(result=api.getAllLastPrices()))
print()
print("getTicker let you to get latest ticker for a given trading pair. Require single parameter - trading pair")
print("  api.getTicker('BTC-USD') : {result}".format(result=api.getTicker('BTC-USD')))
print("  api.getTicker('COB-ETH') : {result}".format(result=api.getTicker('COB-ETH')))
print("  api.getTicker('MISTAKE') : {result}".format(result=api.getTicker('MISTAKE')))
print()
print("getRecentTrades let you to get most recent trades for a given trading pair. Require single parameter - trading pair")
print("  api.getRecentTrades('BTC-USD') : {result}".format(result=api.getRecentTrades('BTC-USD')))
print()
print("getMarketOrderBook let you dig into top entries of the order book for a given trading pair. Require single parameter - trading pair")
print("    api.getMarketOrderBook('ETH-USD') : {result}".format(result=api.getMarketOrderBook('ETH-USD')))
print("it also accept secont optional parameter limit=%some number% to get just %some number% top entries from order book")
print("  api.getMarketOrderBook('ETH-USD',2) : {result}".format(result=api.getMarketOrderBook('ETH-USD',2)))
print()
print("getChartCandles let you get history of prices for a given trading pair. Require single parameters - trading pair")
print("    api.getChartCandles('ETH-USD') : {result}".format(result=api.getChartCandles('ETH-USD')))
print("second parameter - timeframe , allow you to change timeframe for candles. defaults to 1H if absent.list of available timeframes accessable via cobinhood.CHART_CANDLE_TIMEFRAME enum")
print("    api.getChartCandles('ETH-USD',cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_1_DAY) : {result}".format(result=api.getChartCandles('ETH-USD',
                                                                                                                                   cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_1_DAY)))
print("moreover, getChartCandles accept two other optional parameters start_time and end_time which are intended to be unix style times (in milliseconds)")
print("    api.getChartCandles('ETH-USD',cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_15_MINUTE,start_time=1514750400000,end_time=1514750400000 + 10 * 900 * 1000) : {result}"
      .format(result=api.getChartCandles('ETH-USD', cobinhood.CHART_CANDLE_TIMEFRAME.TIMEFRAME_30_MINUTES, start_time=1514750400000, end_time=1514750400000 + 10 * 900 * 1000)))
print()
print("thats it for a public API")












