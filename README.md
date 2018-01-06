# practice
Repo of scripts 

### tweepbot
A bot built using praw and python. It picks a random post from the multi-reddit "food+shittyfoodporn+wewantplates", processes it then submits it twitter.  

Image processing is done with Pillow. Examples:  

#### Colour shifting
![Does this count? Appeared on a old school friends Instagram... Looks like steak and chips.... http://bit.ly/2lTtCju  #WeWantPlates](https://pbs.twimg.com/media/DSspbTwU8AABHMr.jpg)

#### Atkinson Dither
![Appreciate this doggo http://bit.ly/2gSzA5G  #aww](https://pbs.twimg.com/media/DNSD1AIUMAAVAG0.jpg)

#### Colourized Dither
![https://pbs.twimg.com/media/DNRio_ZVQAEUp0o.jpg](https://pbs.twimg.com/media/DNRio_ZVQAEUp0o.jpg)


### news articles
Followed the tutorial [here](https://www.quantinsti.com/blog/sentiment-analysis-news-python/) on scraping newspaper articles and performing sentiment analysis. Updated the code to work with python 3.6. Changed the webscraping code to match the changes in the website's layout. Used nltk instead of pattern to do sentiment analysis and text parsing. Used VADER and a different corpus to perform the sentiment analysis.

Sentiment analysis using [VADER](http://www.nltk.org/_modules/nltk/sentiment/vader.html) and a simple dictionary using a corpus of postive and negative words.

Corpus from: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

[Results](https://github.com/captmomo/practice/blob/master/news_articles/results.txt)

![Results](https://raw.githubusercontent.com/captmomo/practice/master/news_articles/sample_results.PNG)

### speech play
Sample script using [gTTs](https://github.com/pndurette/gTTS) to convert text to sound and using [pygame](https://www.pygame.org/wiki/GettingStarted) to play the sound file.



