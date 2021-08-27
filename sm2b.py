import mplfinance as mpf
import matplotlib.animation as animation
import pandas as pd

ticker = '2330.TW'
start = '2021-08-26'
interval = '5m'

data = pd.read_csv('data/aapl.csv', index_col='end')
data.index = pd.to_datetime(data.index)

col = mpf.make_marketcolors(up='#FF8500', down='#1b90a7',inherit=True)
sty = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=col)
kwargs = dict(type='candle', volume=True, style=sty, mav=(60,120))

fig, axes = mpf.plot(data=data, returnfig=True, **kwargs)
ax1 = axes[0] # Price
ax2 = axes[2] # Volume

def animate(i):
    data = pd.read_csv('data/aapl.csv', index_col='end')
    data.index = pd.to_datetime(data.index)
    data = data.iloc[-300:]
    ax1.clear()
    ax2.clear()
    kwargs = dict(type='candle', style=sty, mav=(60,120))
    mpf.plot(data=data, ax=ax1, volume=ax2, **kwargs)

ani = animation.FuncAnimation(fig,animate,interval=1000)   
mpf.show()

