# Real-Time-Cryptocurrency-Prediction-with-NLP

A real-time cryptocurrency price prediction pipeline with deep learning.

## Objective
Trying to predict highly volatile cryptocurrency (Bitcoin, ethereum, etc) price with information collected from multiple sources in real-time. 

Unlike stock market, cryptocurrency trading happens 24 hours a day. It is helpful to have a real-time analytical engine to spot potential opportunities and risks before it’s too late.

## Approach
The system collects data from multiple sources in real-time and try to find indicator for price movement.
Kafka is used to provide a message queue where multiple producer will publish streaming data to the queue.
Spark streaming is used to consume and process the data streams
Cassandra is used for data persistance.

The data sources include:
1. Historical and real-time trading information for cryptocurrency collected from [GDAX](https://www.gdax.com/)

   'low', 'high', 'open', 'close', 'volume' 

2. Keyword filtered Twitter posts collected with Twitter Streaming API(https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data)

   Perform sentiment analysis to judge the atitude of related posts. Average the sentiment score within a time period and use as additional feature for price prediction.

   Several NLP tools have been tested including [NLTK](http://www.nltk.org/), [TextBlob](http://textblob.readthedocs.io/en/dev/), and [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/).

3. Reddit 

4. Google trend (TODO)

Prediction model: LSTM-based deep learning model is used . A traditional ARIMA based model is also implemented for comparison.

# Project Structure
- `/exploratory`: iPython notebook exploratorty scripts
- `/collection`: data streaming from multi source
- `/processing`: data cleaning and aggregation
- `/prediction`: prediction engine 

## Running instructions

### Requirements
 
### How to run
