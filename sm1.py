from matplotlib.pyplot import title
import yfinance as yf 
import mplfinance as mpf
import matplotlib.animation as animation
import pandas as pd

ticker = '2330.TW'
start = '2021-08-26'
interval = '5m'

data = yf.download(tickers=ticker,start=start, period='1d', interval=interval)
#data.to_csv('data/tw2330.csv')
# print(data)

#df = pd.read_csv('data/tw2330.csv')
# df = df.reset_index(df['Date'])
#print(df)
col = mpf.make_marketcolors(up='#FF8500', down='#1b90a7',inherit=True)
sty = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=col)

# 自己加入VWAP指標
data['vwap'] = ((( data['High'] + data['Low'] ) / 2 )  *  data['Volume']).cumsum() / data['Volume'].cumsum()
addplot1 = mpf.make_addplot(data['vwap'])

kwargs = dict(type='candle', volume=True, style=sty, mav=(6,12), addplot=addplot1)


#mpf.plot(data=data, **kwargs)
#-----------------------------------------------------------------------------------
# 動畫圖
warmup = 20
_addplot1 = mpf.make_addplot(data.iloc[0:warmup]['vwap'])
_kwargs = dict(type='candle', volume=True, style=sty, mav=(6,12), addplot=_addplot1, 
               title= ticker + ' ' + interval + ' ' + start)
fig, axes = mpf.plot(data=data.iloc[0:warmup], returnfig=True, **_kwargs)
ax1 = axes[0] # Price
ax2 = axes[2] # Volume

def animate(i):
    _data = data.iloc[0:(warmup+i)]
    _addplot1 =  mpf.make_addplot(_data['vwap'], ax=ax1)
    ax1.clear()
    ax2.clear()
    _kwargs = dict(type='candle', style=sty, mav=(6,12), addplot=_addplot1)
    mpf.plot(data=_data, ax=ax1, volume=ax2, **_kwargs)

ani = animation.FuncAnimation(fig,animate,interval=100)   
mpf.show()

