from datetime import datetime, timedelta
from time import sleep

import pandas
import requests


class GDAX(object):
  """Class for fetching candle data for a given currency pair."""

  def __init__(self, pair):
    """Create the exchange object.
    Args:
      pair (str): Examples: 'BTC-USD', 'ETH-USD'...
    """
    self.pair = pair
    self.uri = 'https://api.gdax.com/products/{pair}/candles'.format(pair=self.pair)

  @staticmethod
  def __date_to_iso8601(date):
    """Convert a datetime object to the ISO-8601 date format (expected by the GDAX API).
    Args:
      date (datetime): The date to be converted.
    Returns:
      str: The ISO-8601 formatted date.
    """
    return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=date.minute,
        second=date.second)

  def request_slice(self, start, end, granularity):
    # Allow 3 retries (we might get rate limited).
    retries = 3
    for retry_count in range(0, retries):
      # From https://docs.gdax.com/#get-historic-rates the response is in the format:
      # [[time, low, high, open, close, volume], ...]
      # The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}. 
      response = requests.get(self.uri, {
        'start': GDAX.__date_to_iso8601(start),
        'end': GDAX.__date_to_iso8601(end),
        'granularity': granularity * 60  # GDAX API granularity is in seconds.
      })

      if response.status_code != 200 or not len(response.json()):
        if retry_count + 1 == retries:
          raise Exception('Failed to get exchange data for ({}, {})!'.format(start, end))
        else:
          # Exponential back-off.
          sleep(1.5 ** retry_count)
      else:
        # Sort the historic rates (in ascending order) based on the timestamp.
        result = sorted(response.json(), key=lambda x: x[0])
        return result

  def fetch(self, start, end, granularity):
    """Fetch the candle data for a given range and granularity.
    Args:
      start (datetime): The start of the date range.
      end (datetime): The end of the date range (excluded).
      granularity (int): The granularity of the candles data (in minutes).
    Returns:
      (pandas.DataFrame): A data frame of the OHLC and volume information, indexed by their unix timestamp.
    """
    data = []

    # We will fetch the candle data in windows of maximum 100 items.
    # GDAX has a limit of returning maximum of 200, per request.
    delta = timedelta(minutes=granularity * 100)

    slice_start = start
    while slice_start != end:
      slice_end = min(slice_start + delta, end)
      data += self.request_slice(slice_start, slice_end, granularity)
      slice_start = slice_end

    data_frame = pandas.DataFrame(data=data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    data_frame.set_index('time', inplace=True)
    return data_frame