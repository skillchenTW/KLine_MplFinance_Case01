from matplotlib.pyplot import title
import yfinance as yf 
import mplfinance as mpf
import matplotlib.animation as animation
import pandas as pd
import pandas_ta as ta

ticker = '2330.TW'
ticker = '2454.TW'
start = '2021-08-27'
interval = '2m'

data = yf.download(tickers=ticker,start=start, period='1d', interval=interval)
col = mpf.make_marketcolors(up='#FF8500', down='#1b90a7',inherit=True)
sty = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=col)

data.ta.vwap(append=True)
data.ta.bbands(length=10, append=True)

print(data)

bbu_col = [col for col in data.columns if 'BBU' in col][0]
bbl_col = [col for col in data.columns if 'BBL' in col][0]

# 定義一個模擬交易的規則
class Filter():
    def __init__(self):
        self.sig = None
    def update(self, bars):
        data = bars.iloc[-1] # 抓取最後當前的收盤價
        if data['Close'] > data[bbu_col] :   # 超買
            self.sig = 'down'
        elif data['Close'] > data[bbl_col] : # 超賣
            self.sig = 'up'
        else:
            self.sig = None

f = Filter()
sig = []
for i in range(data.shape[0]):
    f.update(data.iloc[:(i+1)])
    sig.append(f.sig)

data['sig'] = sig

# 找信號的座標
data['up'] = data['Low'] - 0.1
data.loc[data['sig'] != 'up', 'up'] = float('nan')
data['down'] = data['High'] + 0.1
data.loc[data['sig'] != 'down', 'down'] = float('nan')
print(data)


#print(data)
# 動畫圖
warmup = 10
kwargs = dict(type='candle', volume=True, style=sty,  
               title= ticker + ' ' + interval + ' ' + start)
fig, axes = mpf.plot(data=data.iloc[0:warmup], returnfig=True, **kwargs)
ax1 = axes[0] # Price
ax2 = axes[2] # Volume

def animate(i):
    _data = data.iloc[0:(warmup+i)]
    add =  [ mpf.make_addplot(_data['VWAP_D'], ax=ax1),
             mpf.make_addplot(_data[bbu_col], ax=ax1),
             mpf.make_addplot(_data[bbl_col], ax=ax1),
             mpf.make_addplot(_data['up'], type='scatter', marker='^', color='red', markersize=50, ax=ax1),
             mpf.make_addplot(_data['down'], type='scatter', marker='v', color='yellow', markersize=50, ax=ax1) 
    ]
    ax1.clear()
    ax2.clear()
    kwargs = dict(type='candle', style=sty, addplot=add)
    mpf.plot(data=_data, ax=ax1, volume=ax2, **kwargs)

ani = animation.FuncAnimation(fig,animate,interval=10)   
mpf.show()

