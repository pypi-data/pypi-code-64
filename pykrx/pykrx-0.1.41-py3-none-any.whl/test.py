from pykrx import stock

df = stock.get_market_price_change_by_ticker("20200319", "20200503")
print(df.loc["019170", '시가'])
print(df.loc["019170", '종가'])

df = stock.get_market_ohlcv_by_date("20200319", "20200503", "019170")
print(df.iloc[0]['시가'])
print(df.iloc[-1]['종가'])
