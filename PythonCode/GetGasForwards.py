
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib2

url = "https://www.cmegroup.com/markets/energy/natural-gas/natural-gas.settlements.html#tradeDate=11%2F18%2F2022"

print('test')

html = urllib2.urlopen(url)
soup = BeautifulSoup(html)