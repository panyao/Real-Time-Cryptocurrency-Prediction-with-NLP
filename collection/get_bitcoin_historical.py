from datetime import datetime
from gdax import GDAX

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("granularity", nargs='?', default = 15)  # in minutes
parser.add_argument("startdate", nargs='?', default = "20180201")
parser.add_argument("enddate", nargs='?', default = "20180202")

args = parser.parse_args()

if __name__ == "__main__":
  """fetching candle data for a given currency pair.
  """

  startdate = datetime.strptime(args.startdate, '%Y%m%d')
  enddate = datetime.strptime(args.enddate, '%Y%m%d')
  
  data_frame = GDAX('BTC-USD').fetch(startdate, enddate, int(args.granularity)) 
  
  data_frame.head()
  data_frame.to_csv('bitcoin.csv')