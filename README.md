# hotelreviews_sentiment_analysis
Sentiment Analysis on hotel reviews from google travel using BERT transformer.

## Data collection
We used  web scraping with selenium to collect hotel reviews from google travel.<br>
The raw data collected consists of hotel names, reviews and rating.<br>
We got the reviews for hotels in Hanoi, Kuala Lumpur, Hong Kong and different cities of Madagascar.<br>
We made sure that the data collected isd balanced between good and bad reviews.

## Dataset creation
Using the data collected from different cities. We created a single cleaned dataset

## Binary Sentiment Classification
We use transformer with Pytorch to classify positive and negative reviews.

