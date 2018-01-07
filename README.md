# practice
Repo of scripts 

### text generator

Created a text generator following the steps in this [guide](http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/) and this [guide from cyber omelette](http://www.cyber-omelette.com/2017/01/markov.html).  
  
Corpus are posts scrapped from a couple of letsrun forum thread.  
  
##### Example with seed word "run" using nltk:

Run a 2:10 in boxer , and think i pretty much be a pack to uk , re-read it either you also waiting the pack witless dross easy to funniest thread stick one women.my mother to weat 5k . kept thinking fishing . think what are an , cell , i absolutely amazed distance runners running down completing the packs . developed a packs can . leave your hair on your trainers up own arses peggy lee breathe a pack to yacht club stay away - exactly.best i 've , bring at an , cell , a pack , finishing it one of greatest ! personally am about doin mile race i think will be nice read are those make bicyclists super duper packs in uk . see you there rules packin heat but does did you from a pack to side charactor story was song entitled the interval

#### Example generated using cyber omelette's markov chain:

Buckle causing the mockery . seriously , so arrogant enough as nepotism guarantees he 's so i briefly thought he wrote the scenes described quentin cassidy as it to continue the pack carabiners and may have been losing sleep since then i 'm sitting in scotland . if you 're the day hahaha ... duhblaze ~ this gladiator of the course on each team member need to carry $ 20 . there was on this post.and , and lamer . surprise ! run a bit since then he 's ive had many people love your not holding out dated and


### tweepbot
A bot built using praw and python. It picks a random post from the multi-reddit "food+shittyfoodporn+wewantplates", processes it then submits it twitter.  

Image processing is done with Pillow. Examples:  

#### Colour shifting
![Does this count? Appeared on a old school friends Instagram... Looks like steak and chips.... http://bit.ly/2lTtCju  #WeWantPlates](https://pbs.twimg.com/media/DSspbTwU8AABHMr.jpg)

#### Atkinson Dither
![Appreciate this doggo http://bit.ly/2gSzA5G  #aww](https://pbs.twimg.com/media/DNSD1AIUMAAVAG0.jpg)

#### Colourized Dither
![Kurt Cobain with his baby daughter. 1992 http://bit.ly/2gSFKCR  #imagesofthe1990s](https://pbs.twimg.com/media/DNRio_ZVQAEUp0o.jpg)

#### Pixelation  
![Capt. Riley and lifeguards, Coney Island, N.Y, ca. 1900. http://bit.ly/2gRcV9T  #ColorizedHistory](https://pbs.twimg.com/media/DNO1xt0V4AAO6aP.jpg)

Complete set can be found [here](https://twitter.com/guavarilla/media)

### news articles
Followed the tutorial [here](https://www.quantinsti.com/blog/sentiment-analysis-news-python/) on scraping newspaper articles and performing sentiment analysis. Updated the code to work with python 3.6. Changed the webscraping code to match the changes in the website's layout. Used nltk instead of pattern to do sentiment analysis and text parsing. Used VADER and a different corpus to perform the sentiment analysis.

Sentiment analysis using [VADER](http://www.nltk.org/_modules/nltk/sentiment/vader.html) and a simple dictionary using a corpus of postive and negative words.

Corpus from: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

[Results](https://github.com/captmomo/practice/blob/master/news_articles/results.txt)

![Results](https://raw.githubusercontent.com/captmomo/practice/master/news_articles/sample_results.PNG)

### speech play
Sample script using [gTTs](https://github.com/pndurette/gTTS) to convert text to sound and using [pygame](https://www.pygame.org/wiki/GettingStarted) to play the sound file.



