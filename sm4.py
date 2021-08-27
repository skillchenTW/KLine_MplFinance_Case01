from matplotlib.pyplot import ylabel
import mplfinance as mpf
import yfinance as yf
import pandas as pd
import pandas_ta as ta

ticker = '2330.TW'
tickers = ['2330.TW','2454.TW','0050.TW']
interval = '1d'
# for ticker in tickers:    
#      print(ticker)
#      data = yf.download(tickers=ticker, period='max', interval=interval)
#      data.to_csv(f'data/{ticker}.csv')    
    

df = pd.read_csv('data/0050.TW.csv', index_col='Date')
df.index = pd.to_datetime(df.index)
#print(df)
my_color = mpf.make_marketcolors(up='red',down='green',edge='inherit')
my_style = mpf.make_mpf_style(marketcolors=my_color)

col = mpf.make_marketcolors(up='#FF8500', down='#1b90a7',inherit=True)
sty = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=col)

# add_plot = [
#     mpf.make_addplot(df[['ma10','ma50']]),
#     mpf.make_addplot(df['signal_long'], scatter=True, markersize=80, markers='^', color='r'),
#     mpf.make_addplot(df['signal_short'], scatter=True, markersize=80, markers='v', color='g'),
#     mpf.make_addplot(df['signal_0'], scatter=True, markersize=80, markers='o', color='y')
# ]


mpf.plot(df, type='candle', 
    ylabel="Price(NT$)", 
    volume=True, ylabel_lower='Volume',
    style=sty,
    mav=(50,200),
    #addplot= add_plot,
)