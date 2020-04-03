import requests
import json

symbol='MSFT'
url='https://finance.yahoo.com/quote/' + symbol
resp = requests.get(url)

#parse the section from the html document containing the raw json data that we need
#you can write jsonstr to a file, then open the file in a web browser to browse the structure of the json data
r=resp.text.encode('utf-8')
i1=0
i1=r.find('root.App.main', i1)
i1=r.find('{', i1)
i2=r.find("\n", i1)
i2=r.rfind(';', i1, i2)
jsonstr=r[i1:i2]      


#load the raw json data into a python data object
data = json.loads(jsonstr)

#pull the values that we are interested in 
name=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['shortName']
price=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']
change=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketChange']['raw']
shares_outstanding=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['sharesOutstanding']['raw']
market_cap=data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['marketCap']['raw']
trailing_pe=data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['trailingPE']['raw']
earnings_per_share=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['trailingEps']['raw']
forward_annual_dividend_rate=data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['dividendRate']['raw']
forward_annual_dividend_yield=data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['dividendYield']['raw']

#print the values
print 'Symbol:', symbol
print 'Name:', name
print 'Price:', price
print 'Change:', change
print 'Shares Outstanding:', shares_outstanding
print 'Market Cap:', market_cap
print 'Trailing PE:', trailing_pe
print 'Earnings Per Share:', earnings_per_share
print 'Forward Annual Dividend Rate:', forward_annual_dividend_rate
print 'Forward_annual_dividend_yield:', forward_annual_dividend_yield