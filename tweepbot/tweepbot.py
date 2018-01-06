#Credit to @ocultart aka /u/Klappan for the idea and contributions.
import json
import os
import random
import re
import time

import praw
import requests
import tweepy

import tweepbotconfig as config
from pixel_image import (atkinson_dither, colour_dither, generate_pixel_image,
                         image_merge, image_rgb_shift)

#Credentials for Tweepy
CONSUMER_KEY = config.data['CONSUMER_KEY']
CONSUMER_SECRET = config.data['CONSUMER_SECRET']
ACCESS_TOKEN = config.data['ACCESS_TOKEN']
ACCESS_SECRET = config.data['ACCESS_SECRET']
BITLY_KEY = config.data['BITLY_KEY']
REDDIT_ID = config.data['REDDIT_ID']
REDDIT_SECRET = config.data['REDDIT_SECRET']
REDDIT_PW = config.data['REDDIT_PW']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

Subs = ['WeWantPlates', 'shittyfoodporn', 'food']


extensionsToCheck = ['.png', '.jpeg', '.jpg', '.gif']


def main():
    reddit = login_reddit()
    generate_submission(reddit)


def get_list(filename):
    list_of_ids = []
    with open(filename) as f:
        list_of_ids = f.read().splitlines()
    return(list_of_ids)


def login_reddit():
    reddit = praw.Reddit(client_id=REDDIT_ID,
                         client_secret=REDDIT_SECRET,
                         user_agent='Test bot by u/captmomo',
                         username='nomnomrhea',
                         password=REDDIT_PW)
    return reddit

#Code to get the random pictures


def picture(reddit, submission):
    posted_ids = get_list('posted_ids.txt')
    print(posted_ids)
    if submission.id in posted_ids:
        print('already posted')
    else:
        print(submission.author)
        check(submission)  # moved check outside the for loop.
        posted_ids.append(submission.id)
        with open('posted_ids.txt', 'w') as f:
            for post_id in posted_ids:
                f.write(post_id + "\n")


def download_image(image_url, submission_id):
    #https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
    #check file size before downloading and processing
    size = requests.get(image_url, stream=True).headers['Content-length']
    print(size)
    response = requests.get(image_url)
    img_ext = re.search('\.\w+$', image_url)
    print(img_ext.group())
    #https://inventwithpython.com/blog/2013/09/30/downloading-imgur-posts-linked-from-reddit-with-python/
    if response.status_code == 200:
        img_file = submission_id + img_ext.group()
        print('Downloading %s...' % (img_file))
        with open(img_file, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)
        return img_file
    else:
        print(response.status_code)
        return 'error'


def process_submissions(submission):
    download_image(submission.url, format(submission.id))
    print("done")


def post_it(submission, filename):
    source = ("https://www.reddit.com/{}".format(submission.permalink))
    link = shorten_url(source)
    hashtag = submission.subreddit_name_prefixed[2:]
    title = strip_title(submission.title)
    try:
        api.update_with_media(
            filename, status='{0} {1} #{2}'.format(title, link, hashtag))
        print('Title: {0} - Source: {1} - {2}'.format(submission.title,
                                                      source, submission.subreddit_name_prefixed))
        time.sleep(240)
    except tweepy.error.TweepError as error:
        print(error)
    os.remove(filename)


def check(submission):
    #Checks if file extensions if .gifv (not accepted on twitter)
    if submission.url.endswith('.gifv'):
        print("error file name .gifv")

    #Checks if the file extension is accepted
    elif any(ext in submission.url for ext in extensionsToCheck):
        img_file = download_image(submission.url, submission.id)
        if img_file != 'error':
            #pixel_file = generate_pixel_image(9,img_file)
            pixel_file = random.choice(
                [image_merge, atkinson_dither, generate_pixel_image, colour_dither])(img_file)
            os.remove(img_file)

        #Checks if the file isn't larger than 5MB (max on twitter)
            if os.path.getsize(pixel_file) < 4500000:
                print(submission.url)
                post_it(submission, pixel_file)
            else:
                print("error file too large")
                os.remove(pixel_file)
        else:
            print("unable to dl image")

    else:
        print("error wrong extension / not a correct extension")
        print(submission.url)


#https://pythontips.com/2013/09/14/making-a-reddit-twitter-bot/
def strip_title(title):
    if len(title) < 100:
         return title
    else:
    	return title[:95] + "..."

#https://www.codecademy.com/courses/python-beginner-en-kZLgV/0/1


def shorten_url(url):
    query_params = {
        'access_token': BITLY_KEY,
        'longUrl': url}

    endpoint = 'https://api-ssl.bitly.com/v3/shorten'
    response = requests.get(endpoint, params=query_params, verify=True)
    data = json.loads(response.content)
    return data['data']['url']


def generate_submission(reddit):
    while True:
        submissions = reddit.subreddit(
            'food+shittyfoodporn+wewantplates').hot(limit=500)
        submission_id = random.sample(list(submissions), 1)
        submission = reddit.submission(id=submission_id[0].id)
        picture(reddit, submission)


if __name__ == '__main__':
    main()
