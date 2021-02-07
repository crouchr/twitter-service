# https://realpython.com/twitter-bot-python-tweepy/
# Twitter API returned a 400 (Bad Request), Image file size must be <= 5242880 bytes
import time
import traceback

from twython import Twython, TwythonError   # 3.7.0

# Twitter username = blackraintweets
APP_KEY    = 'N41qzhrygLrmxVMUXQhg'
APP_SECRET = 'Ad13vdyy5HIjBY3nsipddCrSGVeXUacIjCeyz4hjABo'
OAUTH_TOKEN      = '293023517-Aab9pQEGzECrGGj8lLjGsIqnB6CSOQGXmnlx476W'
OAUTH_TOKEN_SECRET   = 'ZmtLBKNHVlnzImahZbMUgegz0PBM9st1fx7FIngDA'


# Sun Feb  7 21:48:37 2021
def get_twitter_timestamp():
    """
    Shortened timestamp for Tweeting
    """

    tstamp = time.ctime()
    tstamp = tstamp[0:16]
    tstamp = tstamp.replace('  ', ' ')  # leading space after month

    return tstamp


# FIXME : add lat and lon to the tweet in the future
def send_tweet(tweet_text, uuid, lat=None, lon=None, hashtag_arg=None, media_type=None, media_pathname=None):
    """

    :param tweet:
    :return:
    """
    try:
        hashtag_str = ''

        start_time = time.time()

        # Authenticate to Twitter
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        # Create a tweet
        ts = get_twitter_timestamp()
        tweet_full = ts + " : " + tweet_text

        hashtags = hashtag_arg.split(' ')
        if hashtags:
            for hashtag in hashtags:
                hashtag_str += '#' + hashtag + ' '
            tweet_full = tweet_full + ' ' + hashtag_str.rstrip(' ')  # remove trailing space

        # Send tweet
        print('sending Tweet... : ' + tweet_full + ', uuid=' + uuid)
        # status = api.update_status(tweet_full, lat=lat, long=lon)

        # send Tweet
        if media_type == "tweet":
            result = twitter.update_status(status=tweet_full, lat=lat, long=lon)
            truncated = result['truncated']
        elif media_type == "photo":
            my_image = open(media_pathname, 'rb')
            response = twitter.upload_video(media=my_image, media_type='photo')
            result = twitter.update_status(status=tweet_full, lat=lat, long=lon, media_ids=[response['media_id']])
            truncated = result['truncated']
        elif media_type == "video":
            my_video = open(media_pathname, 'rb')
            response = twitter.upload_video(media=my_video, media_type='video/mp4')
            result = twitter.update_status(status=tweet_full, lat=lat, long=lon, media_ids=[response['media_id']])
            truncated = result['truncated']
    except Exception as e:
        traceback.print_exc()

    stop_time = time.time()
    send_time = round((stop_time - start_time), 2)

    if 'created_at' in result:      # basic success criteria
        flag = True
        print('Tweet sent OK, media_type=' + media_type + ', uuid=' + uuid + ', truncated=' + truncated.__str__() + ', send_time=' + send_time.__str__())
    else:
        flag = False
        print('Error: Tweet not sent, media_type=' + media_type + ', uuid=' + uuid + ', truncated=' + truncated.__str__() + ', send_time=' + send_time.__str__())

    return flag, send_time


# basic test script - not used otherwise
def main():

    lat = 0.0
    lon = 1.0

    #print(twython.__version__)  # 3.7.0
    tweet_text = 'testing from mytwython.py'

    # Tweet an image
    # image_pathname = 'test_image.png'
    # media_type = 'photo'
    # send_tweet(tweet_text + ' - a photo', hashtags=None, media_type=media_type, media_pathname=image_pathname)

    # Tweet a video
    media_pathname = '/home/crouchr/metminiwx_media/metminiwx_fri_jan_22_15_43_04_2021.mp4'
    media_type = 'video'
    send_tweet(tweet_text + ' - a video', hashtags=None, media_type=media_type, media_pathname=media_pathname)


if __name__ == '__main__':
    main()

