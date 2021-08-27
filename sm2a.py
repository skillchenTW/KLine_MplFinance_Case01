from alpaca_trade_api import StreamConn
from alpaca_trade_api.common import URL
import pandas as pd
import datetime as dt

ALPACA_API_KEY = 'PKRN44BQGUKXIXBGNOPB'
ALPACA_SECRET_KEY = 'CiLpB3NK9x7iQvBpZtMYwd2CRUIFb80bNFqjusGY'
USE_POLYGON = False
# if USE_POLYGON = True then 
# data_stream='polygon' if USE_POLYGON else 'alpacadatav1'

conn = StreamConn(
    ALPACA_API_KEY,
    ALPACA_SECRET_KEY,
    base_url=URL('https://paper-api.alpaca.markets'),
    data_url=URL('https://data.alpaca.markets'),
    data_stream='polygon'
)
class SecBar():
    def __init__(self):
        self.data = pd.DataFrame()
    def update(self, bars):
        _tmp = pd.DataFrame(bars.__dict__).T
        _tmp['end'] = dt.datetime.fromtimestamp(_tmp['end'] / 1000.0)
        _tmp.set_index('end', inplace=True)
        self.data = self.data.append(_tmp)
        self.data.to_csv('data/aapl.csv')

sec_bar = SecBar()

async def on_agg(conn, channel, bars):
    sec_bar.update(bars)

conn.run(['A.AAPL'])

